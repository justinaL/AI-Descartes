# Symbolic Regression module (PySR)

Finds candidate equations from data. This module originally drove the
commercial solver BARON; it now uses the open-source
[PySR](https://github.com/MilesCranmer/PySR) instead.

## Setup

```
pip install pysr
```

PySR builds its Julia backend on first import (a few minutes, once only).

## How to run

```
python run_pysr.py path_to_dataset > output_file.log
```

or via the shell wrapper:

```
./pysr.sh path_to_dataset > output_file.log
```

Examples:

```
python run_pysr.py datasets/kepler/solar   2>&1 | tee kepler_solar.log
python run_pysr.py datasets/swat/stage1    2>&1 | tee swat_stage1.log
```

Useful flags:

| Flag | Meaning |
|---|---|
| `--target COLNAME` | target column (default: the last column) |
| `--niterations N` | search effort (default 200; lower is faster) |

## Input format

Each dataset directory holds an `input.dat`: space-separated, the header line
starts with `**`, and by convention the **last column is the target**.

```
** m d t
0.0553 0.3870 0.0880
0.815  0.7233 0.2247
```

## Output

Written to `<dataset>/pysr/`:

| File | Contents |
|---|---|
| `pysr_equations.csv` | the Pareto front (complexity, loss, equation) |
| `hall_of_fame.csv` | PySR's own equation dump |
| `checkpoint.pkl` | PySR state |

The Pareto front is also printed to stdout, so redirecting to a log keeps a
readable record of the run.

## Next step: the reasoning module

`pysr_equations.csv` is read directly by the bridge, which converts the
formulas and runs the reasoning pipeline on them:

```
cd ../../reasoning/src
python run_from_pysr.py --snap --measures pointwiseL2,pointwiseLinf_efficient
```

`--snap` rounds PySR's continuous exponents to exact fractions
(e.g. `1.4990162` to `3/2`, rendered as `(x^3)^(1/2)`), which the symbolic
prover requires. See `run_from_pysr.py --help` for the other options.

## Notes

* PySR searches *continuous* exponents, so results need the `--snap` step
  before the reasoning module will accept them. BARON searched integer
  exponents and produced exact rationals directly.
* Results are reproducible: the script pins `random_state=0` with
  `deterministic=True` and serial execution. Dropping those runs multi-core
  and faster, at the cost of run-to-run reproducibility.
