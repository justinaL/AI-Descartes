"""
Bridge from the PySR symbolic-regression output to the reasoning module.

The PySR entry point (symbolic-regression/run_emf/run_pysr.py) writes a Pareto
front to <dataset_dir>/pysr/pysr_equations.csv.  This script reads the
`equation` column of that CSV, converts each formula into the
[keymaera_format, python_format] pairs expected by
pipeline_keymaera_3problems.py, and runs the reasoning pipeline on them.

It reuses the tokenizer / converter / per-problem config from run_from_sr.py
unchanged -- only the input side differs (a CSV instead of a BARON log).

Formulas PySR can produce that the reasoning converter cannot represent
(e.g. variable exponents like `1.1254 ^ m`) are skipped with a warning; the
KeYmaeraX polynomial arithmetic only supports constant exponents.

Usage (from reasoning/src):
    python run_from_pysr.py [path/to/pysr_equations.csv] [--problem solar] \
                            [--top N] [--dry-run]

Defaults to the kepler/solar Pareto front.
"""

import argparse
import csv
import os
import sys
from fractions import Fraction

import run_from_sr as rfs   # reuse PROBLEMS, convert(), tokenizer, renderer

# measures the reasoning pipeline can evaluate; `derivation` (is the formula
# derivable from the axioms?) is the fast, central AI-Descartes question, while
# interval/pointwise* run slow KeYmaeraX binary searches.
ALL_MEASURES = ['interval', 'dependencies', 'pointwiseL2', 'pointwiseLinf',
                'pointwiseLinf_efficient', 'derivation', 'weak_derivation']

# default CSV per problem, relative to reasoning/src
DEFAULT_CSV = {
    'solar':     '../../symbolic-regression/run_emf/datasets/kepler/solar/pysr/pysr_equations.csv',
    'exoplanet': '../../symbolic-regression/run_emf/datasets/kepler/exoplanet/pysr/pysr_equations.csv',
}


def parse_csv(csv_path):
    """Return [(loss, complexity, expr)] for the Pareto front, best (lowest
    loss) first, deduplicated on the equation string."""
    rows = []
    with open(csv_path, newline='') as f:
        for row in csv.DictReader(f):
            expr = (row.get('equation') or '').strip()
            if not expr:
                continue
            rows.append((float(row['loss']), int(float(row['complexity'])), expr))
    seen = set()
    unique = []
    for loss, complexity, expr in sorted(rows, key=lambda r: r[0]):
        if expr not in seen:
            seen.add(expr)
            unique.append((loss, complexity, expr))
    return unique


def snap_exponent(exp_str, tol, max_den):
    """Snap a numeric exponent string to the nearest simple fraction.

    PySR fits continuous exponents (e.g. 1.4990162), but the symbolic prover
    needs exact rationals (3/2).  If the closest fraction with denominator
    <= max_den is within `tol`, return it as a Fraction; otherwise leave the
    original string untouched (so genuinely non-rational overfit exponents are
    not forced into a clean shape).
    """
    try:
        val = float(exp_str)
    except (TypeError, ValueError):
        return exp_str
    frac = Fraction(val).limit_denominator(max_den)
    if abs(float(frac) - val) <= tol:
        return frac
    return exp_str


def _apply_fraction(inner, exp, op):
    """Apply a snapped Fraction exponent p/q to `inner`.

    Integer (q==1) -> inner^p.  Fractional (q>1) -> ( inner^p )^(1/q), the
    "integer power under a root" shape the KeYmaeraX pipeline requires (it
    handles ^(1/2) etc. but not ^(3/2) directly -- see the reference formulas
    like ( 0.1319 * dN^3 )^(1/2) ).  Numeric literals stay whitespace-delimited
    so Formula.__init__ still lifts them to existential constants.
    """
    p, q = exp.numerator, exp.denominator
    ps = f'({p})' if p < 0 else str(p)
    if q == 1:
        return f'{inner}{op}{ps}'
    return f'( {inner}{op}{ps} ){op}(1/{q})'


def _apply_string(inner, exp, op):
    """Apply an un-snapped original exponent string (rfs.render's behaviour)."""
    if op == '^':
        e = '(1/2)' if exp == '0.5' else (f'({exp})' if exp.startswith('-') else exp)
    else:
        e = f'({exp})' if exp.startswith('-') else exp
    return f'{inner}{op}{e}'


def render_snapped(atoms, target):
    """Like rfs.render, but Fraction exponents are rewritten into the pipeline's
    root form.  The exponent sits on the preceding atom -- often a ')' closing a
    parenthesised base -- so we track paren nesting to wrap the whole group."""
    op = '^' if target == 'keymaera' else '**'
    parts = []
    open_stack = []
    for kind, val, exp in atoms:
        if kind == 'num' and '.' not in val and 'e' not in val and 'E' not in val:
            val += '.0'
        if kind == 'op' and val == '(':
            open_stack.append(len(parts))
            parts.append(val)
            continue
        if kind == 'op' and val == ')':
            open_idx = open_stack.pop() if open_stack else 0
            group = ' '.join(parts[open_idx:] + [')'])   # the full ( ... )
            del parts[open_idx:]
            if exp is None:
                parts.append(group)
            elif isinstance(exp, Fraction):
                parts.append(_apply_fraction(group, exp, op))
            else:
                parts.append(_apply_string(group, exp, op))
            continue
        if exp is None:
            parts.append(val)
        elif isinstance(exp, Fraction):
            parts.append(_apply_fraction(val, exp, op))
        else:
            parts.append(_apply_string(val, exp, op))
    return ' '.join(parts)


def convert_snapped(expr, var_map, tol, max_den):
    """Convert like rfs.convert, but snap near-rational exponents first.
    Returns [keymaera_string, python_string]."""
    atoms = rfs.to_atoms(rfs.tokenize(expr), var_map)
    snapped = [(k, v, snap_exponent(e, tol, max_den) if e is not None else e)
               for (k, v, e) in atoms]
    return [render_snapped(snapped, 'keymaera'), render_snapped(snapped, 'python')]


def main():
    parser = argparse.ArgumentParser(description='Run the reasoning pipeline on '
                                     'PySR output (kepler/solar or exoplanet).')
    parser.add_argument('csv', nargs='?', default=None,
                        help='PySR pysr_equations.csv (default: the problem\'s '
                             'Pareto front)')
    parser.add_argument('--problem', choices=sorted(rfs.PROBLEMS), default='solar',
                        help='which Kepler dataset the CSV comes from '
                             '(default: solar)')
    parser.add_argument('--top', type=int, default=None,
                        help='only use the N best candidates (default: all)')
    parser.add_argument('--measures', default=None,
                        help='comma-separated subset of measures to evaluate '
                             '(default: the pipeline\'s full set). Use '
                             '"derivation" for a fast derivability-only run. '
                             f'Available: {",".join(ALL_MEASURES)}')
    parser.add_argument('--snap', action='store_true',
                        help='snap near-rational exponents to exact fractions '
                             '(e.g. 1.4990162 -> 3/2) so PySR\'s continuous fits '
                             'match the symbolic prover; pair with '
                             '--measures weak_derivation for existential constants')
    parser.add_argument('--snap-tol', type=float, default=0.02,
                        help='max distance an exponent may be snapped (default 0.02)')
    parser.add_argument('--snap-max-den', type=int, default=4,
                        help='largest denominator a snapped fraction may have '
                             '(default 4, so 3/2, 1/2, 2, 1/3 ... are allowed)')
    parser.add_argument('--dry-run', action='store_true',
                        help='print the converted formulas and exit without '
                             'running KeYmaeraX')
    args = parser.parse_args()

    measures = None
    if args.measures:
        measures = [m.strip() for m in args.measures.split(',') if m.strip()]
        unknown = [m for m in measures if m not in ALL_MEASURES]
        if unknown:
            sys.exit(f'unknown measure(s): {unknown}\nAvailable: {ALL_MEASURES}')

    # the pipeline uses paths relative to reasoning/src
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    csv_path = args.csv or DEFAULT_CSV[args.problem]
    if not os.path.exists(csv_path):
        sys.exit(f'PySR CSV not found: {csv_path}\n'
                 f'Generate it with e.g.:\n'
                 f'  cd ../../symbolic-regression/run_emf\n'
                 f'  python run_pysr.py datasets/kepler/{args.problem} '
                 f'> kepler_{args.problem}_pysr.log')

    candidates = parse_csv(csv_path)
    if not candidates:
        sys.exit(f'No equations found in {csv_path} — did the PySR run finish?')

    problem = rfs.PROBLEMS[args.problem]
    formulas = []
    skipped = 0
    print(f'Found {len(candidates)} candidate formula(s) in {csv_path}'
          f'{" (snapping exponents)" if args.snap else ""}:\n')
    for loss, complexity, expr in candidates:
        try:
            if args.snap:
                pair = convert_snapped(expr, problem['var_map'],
                                       args.snap_tol, args.snap_max_den)
            else:
                pair = rfs.convert(expr, problem['var_map'])
        except ValueError as e:
            skipped += 1
            print(f'  [skip] c{complexity} loss={loss:g}   {expr}')
            print(f'         not convertible: {e}\n')
            continue
        print(f'  c{complexity} loss={loss:g}   {expr}')
        print(f'    keymaera: {pair[0]}')
        print(f'    python:   {pair[1]}\n')
        formulas.append(pair)
        if args.top and len(formulas) >= args.top:
            break

    if not formulas:
        sys.exit('No convertible formulas — nothing to reason about.')
    if skipped:
        print(f'({skipped} formula(s) skipped as not representable in KeYmaeraX.)\n')

    if args.dry_run:
        print('Dry run: not starting the reasoning pipeline.')
        return

    import pipeline_keymaera_3problems as pipeline
    if measures is not None:
        pipeline.MEASURES = measures   # run_pipeline loops over this module global
    print(f'Running reasoning pipeline (measures: {pipeline.MEASURES}, '
          f'precision: {pipeline.PRECISION}) ...\n')
    getattr(pipeline, problem['runner'])(formulas)


if __name__ == '__main__':
    main()
