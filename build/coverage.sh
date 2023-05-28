#!/usr/bin/env bash

source .venv/bin/activate

pytest --cov=arange/src --cov-report=html .
