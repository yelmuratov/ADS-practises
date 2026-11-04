# P02 - OS, kernels and process lifecycle

Lab for the fictional lab-seat enrollment project: `parent.py` starts `child.py`, waits for it and reports the child's exit code.

## Run

```
cd P02-process-lab
python3 starter/parent.py
```

Press Enter when the child asks. Optional POSIX demo:

```
python3 starter/fork_exec_wait.py
```

The child writes synthetic data only, to `output/child-result.txt`.

## Contents

- `starter/` - lab programs
- `Worksheet.md` - my answers
- `evidence/` - terminal output and process inspection from my runs
