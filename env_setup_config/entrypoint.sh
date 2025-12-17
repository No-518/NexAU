#!/usr/bin/env bash
set -euo pipefail

AGENT_CONFIG="${NEXAU_AGENT_CONFIG:-/opt/nexau/docker/env_setup_agent.yaml}"

if [[ -n "${NEXAU_TASK:-}" ]] || [[ "$#" -gt 0 ]]; then
  exec python /opt/nexau/docker/run_once.py "$@"
fi

exec node /opt/nexau/cli/dist/cli.js "$AGENT_CONFIG"

