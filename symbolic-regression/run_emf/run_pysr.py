"""
PySR entry point for the SR module -- an open-source replacement for BARON.

The dataset directory is passed
in as an argument, and everything is printed to stdout so it can be redirected
to a log file.

Usage (from run_emf/):
    python run_pysr.py datasets/kepler/solar > kepler_solar.log

The dataset directory must contain an input.dat file whose first line is the
"** col1 col2 ... target" header.  By convention the LAST column is the target
(as in the BARON pipeline); override with --target COLNAME if needed.
"""

import argparse
import sys

import numpy as np
from pysr import PySRRegressor


def load(path):
    with open(path) as f:
        header = f.readline().split()          # e.g. ["**", "m", "d", "t"]
    names = header[1:] if header and header[0] == "**" else header
    data = np.loadtxt(path, skiprows=1)
    if data.ndim == 1:                          # single row -> keep 2D
        data = data.reshape(1, -1)
    cols = {n: data[:, i] for i, n in enumerate(names)}
    return names, cols


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset_dir", help="dir containing input.dat (e.g. datasets/kepler/solar)")
    ap.add_argument("--target", default=None, help="target column name (default: last column)")
    ap.add_argument("--niterations", type=int, default=200)
    args = ap.parse_args()

    dataset_dir = args.dataset_dir.rstrip("/")
    input_path = f"{dataset_dir}/input.dat"

    names, cols = load(input_path)
    target = args.target or names[-1]
    if target not in names:
        sys.exit(f"target column '{target}' not found in {names}")
    feature_names = [n for n in names if n != target]
    X = np.column_stack([cols[n] for n in feature_names])
    y = cols[target]

    print(f"dataset : {input_path}")
    print(f"features: {feature_names}")
    print(f"target  : {target}")
    print(f"points  : {len(y)}")
    sys.stdout.flush()

    model = PySRRegressor(
        niterations=args.niterations,
        binary_operators=["+", "-", "*", "/", "^"],   # ^ lets it find powers (d^1.5)
        unary_operators=[],                           # keep axiom-friendly
        maxsize=20,
        model_selection="best",
        random_state=0,
        deterministic=True,
        parallelism="serial",     # required for reproducibility with random_state
        progress=False,           # progress bar deadlocks when stdout is redirected to a file
        output_directory=dataset_dir,   # PySR writes artifacts to <dir>/<run_id>/
        run_id="pysr",                  # -> the "pysr" output folder (replaces tmp/)
    )
    model.fit(X, y, variable_names=feature_names)   # names must be passed here, not to the ctor

    print("\n=== Pareto front (complexity vs loss) ===")
    print(model.equations_[["complexity", "loss", "equation"]].to_string(index=False))

    out_csv = f"{dataset_dir}/pysr/pysr_equations.csv"
    model.equations_.to_csv(out_csv, index=False)
    print(f"\nSaved -> {out_csv}")
    print("Best (sympy):", model.sympy())


if __name__ == "__main__":
    main()
