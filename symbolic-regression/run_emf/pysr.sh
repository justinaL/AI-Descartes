#!/bin/sh
# PySR entry point -- open-source replacement for emf.sh (BARON).
#
# Usage (same convention as emf.sh, minus the yaml arg):
#     ./pysr.sh datasets/kepler/solar > kepler_solar.log
#
# Extra args are passed straight through to run_pysr.py, e.g.:
#     ./pysr.sh datasets/kepler/exoplanet --niterations 500 > exo.log

dir=$1
shift

python run_pysr.py "$dir" "$@"
