"""Optional POSIX-only fork, exec, and wait demonstration for Linux/macOS."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> int:
    if os.name == "nt":
        print("This optional example needs POSIX fork(); use parent.py on Windows.")
        return 0

    child_path = Path(__file__).with_name("child.py")
    print(f"FORK-DEMO: parent PID={os.getpid()} is about to fork.", flush=True)
    child_pid = os.fork()
    if child_pid == 0:
        # This branch is the child. execv replaces this process image with Python running child.py.
        try:
            os.execv(sys.executable, [sys.executable, "-u", str(child_path)])
        except OSError as error:
            print(f"FORK-DEMO: execv failed: {error}", file=sys.stderr, flush=True)
            # Do not return into a copied parent call stack after a failed exec.
            os._exit(127)

    print(f"FORK-DEMO: parent created PID={child_pid}; waiting for it.", flush=True)
    waited_pid, status = os.waitpid(child_pid, 0)
    if os.WIFEXITED(status):
        print(f"FORK-DEMO: waited for PID={waited_pid}; exit code={os.WEXITSTATUS(status)}", flush=True)
    else:
        print(f"FORK-DEMO: waited for PID={waited_pid}; raw status={status}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
