#!/usr/bin/bash

source .venv/bin/activate

set -e

pushd arranges/src
pydoc-markdown -p arranges > ../../docs/pydoc.md
popd

mkdocs build
mkdocs gh-deploy
