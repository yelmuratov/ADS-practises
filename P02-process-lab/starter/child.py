"""A small child process for P02. It writes only synthetic lab data."""

from __future__ import annotations

import os
import platform
import sys
import time
from pathlib import Path

EXIT_CODE = 7
CPU_SECONDS = 0.75
LAB_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = LAB_ROOT / "output" / "child-result.txt"


def bounded_cpu_work(seconds: float) -> int:
    """Use CPU for a short, fixed time; the count is only a visible result."""
    deadline = time.perf_counter() + seconds
    count = 0
    while time.perf_counter() < deadline:
        count += 1
    return count


def main() -> int:
    print("CHILD: started", flush=True)
    print(f"CHILD: PID={os.getpid()} PPID={os.getppid()}", flush=True)
    print(f"CHILD: platform={platform.system()} Python={platform.python_version()}", flush=True)
    print(f"CHILD: CPU phase for {CPU_SECONDS} seconds...", flush=True)
    iterations = bounded_cpu_work(CPU_SECONDS)
    print(f"CHILD: CPU phase complete ({iterations} loop iterations).", flush=True)

    try:
        input("CHILD: press Enter to continue and write synthetic lab output: ")
    except EOFError:
        print("CHILD: no terminal input was available. Run in a terminal and press Enter; no new output was written.", file=sys.stderr, flush=True)
        return 1

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(
        "P02 synthetic lab output\n"
        f"child_pid={os.getpid()}\n"
        f"parent_pid={os.getppid()}\n"
        f"platform={platform.system()}\n"
        f"cpu_iterations={iterations}\n"
        f"requested_exit_code={EXIT_CODE}\n",
        encoding="utf-8",
    )
    print(f"CHILD: wrote synthetic data to {OUTPUT_FILE.relative_to(LAB_ROOT)}", flush=True)
    print(f"CHILD: exiting with code {EXIT_CODE}.", flush=True)
    return EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
