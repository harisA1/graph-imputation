"""A minimal job queue so runs go back to back on the single GPU.

    python -m gimpute.queue add --paper rossi2020-fp --version v1       # arguments of gimpute.run
    python -m gimpute.queue list
    nohup python -m gimpute.queue work > runs/queue/worker.log 2>&1 &   # one worker; exits when empty

State lives in runs/queue/ (git-ignored): pending.txt, done.txt, logs/. Only one worker runs
at a time (file lock). Runs are resumable, so a job that was interrupted can just be added again.
"""
from __future__ import annotations

import datetime
import fcntl
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q = ROOT / "runs" / "queue"


def _pop() -> str | None:
    """Atomically take the first pending job."""
    with open(Q / "pending.txt", "a+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        jobs = [line for line in f.read().splitlines() if line.strip()]
        if not jobs:
            return None
        f.seek(0)
        f.truncate()
        f.write("".join(j + "\n" for j in jobs[1:]))
        return jobs[0]


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "list"
    (Q / "logs").mkdir(parents=True, exist_ok=True)
    if cmd == "add":
        with open(Q / "pending.txt", "a", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(shlex.join(argv[1:]) + "\n")
        print("queued:", shlex.join(argv[1:]))
    elif cmd == "list":
        for name in ("pending.txt", "done.txt"):
            path = Q / name
            print(f"--- {name}\n{path.read_text(encoding='utf-8') if path.exists() else ''}", end="")
    elif cmd == "work":
        lock = open(Q / "worker.lock", "w")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("a worker is already running")
            return 1
        while (job := _pop()) is not None:
            stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            print(f"[{stamp}] start: {job}", flush=True)
            with open(Q / "logs" / f"{stamp}.log", "w", encoding="utf-8") as log:
                code = subprocess.run([sys.executable, "-m", "gimpute.run", *shlex.split(job)], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT).returncode
            with open(Q / "done.txt", "a", encoding="utf-8") as f:
                f.write(f"{stamp} exit={code} {job}\n")
            print(f"[{stamp}] exit={code}", flush=True)
        print("queue empty")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
