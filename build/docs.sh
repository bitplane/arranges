#!/usr/bin/bash

source .venv/bin/activate

set -e

mkdocs build
mkdocs gh-deploy
