#!/bin/bash

source .venv/bin/activate

python3 -m twine upload arranges/dist/* --user=__token__
