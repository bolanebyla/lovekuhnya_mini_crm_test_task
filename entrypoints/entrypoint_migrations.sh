#!/usr/bin/env bash
set -e

python -m mini_crm.run.alembic_runner upgrade head
