#!/bin/bash

source .venv/bin/activate

python3 -m twine upload arange/dist/* --user=__token__
