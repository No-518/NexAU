from __future__ import annotations

import os
import sys
from datetime import datetime

from nexau import load_agent_config


def get_date() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main() -> int:
    config_path = os.environ.get("NEXAU_AGENT_CONFIG", "/opt/nexau/docker/env_setup_agent.yaml")
    task = os.environ.get("NEXAU_TASK")
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:]).strip()

    if not task:
        print("Missing task. Provide NEXAU_TASK or pass the task as CLI args.", file=sys.stderr)
        return 2

    agent = load_agent_config(config_path)
    response = agent.run(
        task,
        context={
            "date": get_date(),
            "working_directory": os.getcwd(),
        },
    )
    print(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

