import os
import platform
import subprocess
from pathlib import Path

def run(command: list[str], dry_run: bool = True) -> dict:
    # Never invoke shell=True. The production executor should additionally
    # enforce an allowlist and privilege boundary.
    if dry_run:
        return {"command": command, "dry_run": True, "returncode": 0,
                "stdout": "", "stderr": ""}
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    return {
        "command": command,
        "dry_run": False,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

def host_facts() -> dict:
    return {
        "os": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "uid": os.getuid(),
    }

def validate_package(package_path: str) -> dict:
    path = Path(package_path)
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_file": path.is_file(),
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else 0,
    }
