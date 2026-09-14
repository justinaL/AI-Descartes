#!/bin/sh
# PySR entry point for the SR module (replaces the original BARON driver).
#
# Usage:
#     ./pysr.sh datasets/kepler/solar > kepler_solar.log
#
# Extra args are passed straight through to run_pysr.py, e.g.:
#     ./pysr.sh datasets/kepler/exoplanet --niterations 500 > exo.log

dir=$1
shift

python run_pysr.py "$dir" "$@"
