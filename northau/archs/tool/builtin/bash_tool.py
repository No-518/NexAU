"""Bash tool implementation for executing shell commands."""

import subprocess
import os
from typing import Dict, Any, Optional


def bash(
    command: str,
    working_directory: Optional[str] = None,
    timeout: int = 30,
    capture_output: bool = True
) -> Dict[str, Any]:
    """
    Execute a bash command and return the result.
    
    Args:
        command: The bash command to execute
        working_directory: Directory to run the command in (defaults to current)
        timeout: Maximum time to wait for command completion in seconds
        capture_output: Whether to capture and return stdout/stderr
    
    Returns:
        Dict containing execution results
    """
    try:
        # Set working directory
        cwd = working_directory or os.getcwd()
        
        # Execute command
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            timeout=timeout,
            capture_output=capture_output,
            text=True
        )
        
        return {
            "status": "success",
            "return_code": result.returncode,
            "stdout": result.stdout if capture_output else "",
            "stderr": result.stderr if capture_output else "",
            "command": command,
            "working_directory": cwd
        }
        
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "error": f"Command timed out after {timeout} seconds",
            "command": command,
            "working_directory": cwd
        }
        
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "return_code": e.returncode,
            "error": str(e),
            "stdout": e.stdout if capture_output else "",
            "stderr": e.stderr if capture_output else "",
            "command": command,
            "working_directory": cwd
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "command": command,
            "working_directory": cwd
        }