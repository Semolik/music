#! /usr/bin/env bash

alembic upgrade head

python ./initial_data.py