"""
Bridge from the symbolic-regression module to the reasoning module.

Parses the "OPT CAND" candidate formulas from an SR run log (the stdout of
run_emf/emf.sh), converts them into the [keymaera_format, python_format]
pairs expected by pipeline_keymaera_3problems.py, and runs the reasoning
pipeline on them.

Usage (from reasoning/src):
    python run_from_sr.py [path/to/sr_log] [--top N] [--dry-run]

Defaults to the kepler/solar problem:
    python run_from_sr.py ../../symbolic-regression/run_emf/kepler_solar.log
"""

import argparse
import os
import re
import sys

# Per-problem config: SR dataset column names -> reasoning pipeline variable
# names (from the dataset's input.dat header; the target column never appears
# in the candidate formulas), and the pipeline function to run.
# solar input.dat:     ** m d t     exoplanet input.dat: ** M m d t1
PROBLEMS = {
    'solar':     {'var_map': {'m': 'm2N', 'd': 'dN'},
                  'runner': 'run_kepler_solar'},
    'exoplanet': {'var_map': {'M': 'm1N', 'm': 'm2N', 'd': 'dN'},
                  'runner': 'run_kepler_exoplanets'},
}

# e.g. "   1| OPT CAND   0:   58.66853    P S (0.0691226128220813*d^2)"
# REDUNDANT candidates have no " S " separator and are skipped.
OPT_CAND_RE = re.compile(r'OPT CAND\s+\d+:\s+([0-9.eE+-]+)\s+\S+\s+S\s+(\S.*)$')

TOKEN_RE = re.compile(r'\d+\.\d+(?:[eE][+-]?\d+)?|\d+(?:[eE][+-]?\d+)?'
                      r'|[A-Za-z_]\w*|\*\*|[*/+\-()^]')

NUMBER_RE = re.compile(r'^\d+(\.\d+)?([eE][+-]?\d+)?$')


def parse_log(log_path):
    """Return [(objective, expr_string)] for non-redundant candidates, best first."""
    candidates = []
    with open(log_path) as f:
        for line in f:
            m = OPT_CAND_RE.search(line)
            if m:
                candidates.append((float(m.group(1)), m.group(2).strip()))
    # the same candidate is printed both during the run and in the final
    # summary; deduplicate on the expression string
    seen = set()
    unique = []
    for obj, expr in sorted(candidates, key=lambda c: c[0]):
        if expr not in seen:
            seen.add(expr)
            unique.append((obj, expr))
    return unique


def tokenize(expr):
    tokens = TOKEN_RE.findall(expr)
    if ''.join(tokens).replace(' ', '') != expr.replace(' ', ''):
        raise ValueError(f'could not fully tokenize SR expression: {expr}')
    return tokens


def to_atoms(tokens, var_map):
    """Merge power operators into their base token and rename variables,
    returning a list of atoms to be joined with spaces."""
    atoms = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in ('^', '**'):
            # exponent: optional minus, then a number (SR prints e.g. ^2, ^-2, ^0.5)
            j = i + 1
            neg = False
            if j < len(tokens) and tokens[j] == '-':
                neg = True
                j += 1
            if j >= len(tokens) or not NUMBER_RE.match(tokens[j]):
                raise ValueError(f'unsupported exponent after ^ in: {" ".join(tokens)}')
            exp = ('-' if neg else '') + tokens[j]
            if not atoms:
                raise ValueError(f'power with no base in: {" ".join(tokens)}')
            atoms[-1] = (atoms[-1][0], atoms[-1][1], exp)
            i = j + 1
            continue
        if NUMBER_RE.match(tok):
            atoms.append(('num', tok, None))
        elif re.match(r'^[A-Za-z_]\w*$', tok):
            if tok not in var_map:
                raise ValueError(f'SR variable "{tok}" has no mapping to a pipeline '
                                 f'variable (known: {var_map})')
            atoms.append(('var', var_map[tok], None))
        else:
            atoms.append(('op', tok, None))
        i += 1
    return atoms


def render(atoms, target):
    """Render atoms as a keymaera or python formula string.

    Follows the pipeline's format rules: spaces between terms so that
    numeric constants are whitespace-delimited tokens, exponents glued to
    their base (so they are not mistaken for constants), integer constants
    written with .0, and sqrt as (expr)^(1/2) in keymaera format.
    """
    parts = []
    for kind, val, exp in atoms:
        if kind == 'num' and '.' not in val and 'e' not in val and 'E' not in val:
            val += '.0'
        if exp is not None:
            if target == 'keymaera':
                e = '(1/2)' if exp == '0.5' else (f'({exp})' if exp.startswith('-') else exp)
                val = f'{val}^{e}'
            else:
                e = f'({exp})' if exp.startswith('-') else exp
                val = f'{val}**{e}'
        parts.append(val)
    s = ' '.join(parts)
    # glue parentheses/operands so constants stay whitespace-delimited but
    # the string stays close to the documented examples
    return s


def convert(expr, var_map):
    atoms = to_atoms(tokenize(expr), var_map)
    return [render(atoms, 'keymaera'), render(atoms, 'python')]


def main():
    parser = argparse.ArgumentParser(description='Run the reasoning pipeline on '
                                     'symbolic-regression output (kepler/solar).')
    parser.add_argument('log', nargs='?',
                        default='../../symbolic-regression/run_emf/kepler_solar.log',
                        help='SR run log (stdout of emf.sh)')
    parser.add_argument('--problem', choices=sorted(PROBLEMS), default='solar',
                        help='which Kepler dataset the log comes from '
                             '(default: solar)')
    parser.add_argument('--top', type=int, default=None,
                        help='only use the N best candidates (default: all)')
    parser.add_argument('--dry-run', action='store_true',
                        help='print the converted formulas and exit without '
                             'running KeYmaeraX')
    args = parser.parse_args()

    # the pipeline uses paths relative to reasoning/src
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    log_path = os.path.abspath(args.log) if os.path.isabs(args.log) else args.log
    if not os.path.exists(log_path):
        sys.exit(f'SR log not found: {log_path}\n'
                 f'Generate it with e.g.:\n'
                 f'  cd ../../symbolic-regression/run_emf\n'
                 f'  ./emf.sh datasets/kepler/solar opts-kepler.yaml > kepler_solar.log')

    candidates = parse_log(log_path)
    if not candidates:
        sys.exit(f'No "OPT CAND" lines found in {log_path} — did the SR run finish?')
    if args.top:
        candidates = candidates[:args.top]

    problem = PROBLEMS[args.problem]
    formulas = []
    print(f'Found {len(candidates)} candidate formula(s) in {log_path}:\n')
    for obj, expr in candidates:
        pair = convert(expr, problem['var_map'])
        print(f'  SR objective {obj:g}   {expr}')
        print(f'    keymaera: {pair[0]}')
        print(f'    python:   {pair[1]}\n')
        formulas.append(pair)

    if args.dry_run:
        print('Dry run: not starting the reasoning pipeline.')
        return

    import pipeline_keymaera_3problems as pipeline
    print(f'Running reasoning pipeline (measures: {pipeline.MEASURES}, '
          f'precision: {pipeline.PRECISION}) ...\n')
    getattr(pipeline, problem['runner'])(formulas)


if __name__ == '__main__':
    main()
