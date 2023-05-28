#!/usr/bin/env bash

source .venv/bin/activate

pytest --cov=arranges/src --cov-report=html .
