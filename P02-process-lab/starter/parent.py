"""Start, observe, and wait for the P02 child process using portable Python."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    child_path = Path(__file__).with_name("child.py")
    command = [sys.executable, "-u", str(child_path)]
    print(f"PARENT: starting child with this Python runtime: {sys.executable}", flush=True)
    child = subprocess.Popen(command)  # stdio is inherited, so the child uses this terminal.
    print(f"PARENT: child PID is {child.pid}; waiting for it to exit.", flush=True)
    interrupted = False
    try:
        exit_code = child.wait()
    except KeyboardInterrupt:
        interrupted = True
        print("\nPARENT: Ctrl+C received. Ending only this lab child process.", flush=True)
        exit_code = None
    finally:
        # The Popen object identifies the one child this lab owns; never target other processes.
        if child.poll() is None:
            child.terminate()
            try:
                exit_code = child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("PARENT: child did not end in 5 seconds; killing it.", flush=True)
                child.kill()
                exit_code = child.wait()

    if interrupted:
        print(f"PARENT: child ended after interruption with code {exit_code}.", flush=True)
        return 0

    print(f"PARENT: wait() returned; child exit code was {exit_code}.", flush=True)
    if exit_code == 7:
        print("PARENT: non-zero is intentional in this lab; the parent reports it and exits normally.", flush=True)
    elif exit_code != 0:
        print("PARENT: unexpected child result; read the child's error above and check the lab guide.", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
