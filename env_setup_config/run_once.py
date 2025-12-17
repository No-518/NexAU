from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from nexau import load_agent_config


def get_date() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _read_task_file(task_file: str) -> str:
    path = Path(task_file).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Task file not found: {path}")

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"Task file is empty: {path}")

    return content


def _default_task_file() -> Path | None:
    script_dir = Path(__file__).parent
    for filename in ("task_prompt.txt", "task_prompt.md"):
        candidate = script_dir / filename
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a NexAU agent once (non-interactive).")
    parser.add_argument(
        "--config",
        dest="config_path",
        default=os.environ.get("NEXAU_AGENT_CONFIG", "/opt/nexau/docker/env_setup_agent.yaml"),
        help="Path to agent YAML config (or set NEXAU_AGENT_CONFIG).",
    )
    parser.add_argument(
        "--task-file",
        dest="task_file",
        default=os.environ.get("NEXAU_TASK_FILE"),
        help="Read the task prompt from a file (or set NEXAU_TASK_FILE).",
    )
    parser.add_argument(
        "task",
        nargs="*",
        help="Task prompt text. If omitted, uses NEXAU_TASK, then --task-file, then env_setup_config/task_prompt.txt|.md if present.",
    )
    args = parser.parse_args()

    task: str | None = None
    if args.task:
        task = " ".join(args.task).strip()
    else:
        task = (os.environ.get("NEXAU_TASK") or "").strip() or None

    if not task:
        task_file = args.task_file
        if not task_file:
            default_file = _default_task_file()
            task_file = str(default_file) if default_file else None
        if task_file:
            try:
                task = _read_task_file(task_file)
            except Exception as exc:
                print(f"Failed to read task file: {exc}", file=sys.stderr)
                return 2

    if not task:
        print(
            "Missing task. Provide NEXAU_TASK, pass the task as CLI args, or set NEXAU_TASK_FILE/--task-file.",
            file=sys.stderr,
        )
        return 2

    agent = load_agent_config(args.config_path)
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
