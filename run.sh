#!/usr/bin/env bash
set -euo pipefail
docker compose up --build --abort-on-container-exit
