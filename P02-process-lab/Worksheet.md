# P02 individual worksheet — process evidence and runtime ADR

**Name:** ____________________  **Date:** 2026-11-04  **Operating system:** Linux (Kali rolling, kernel 7.1.5)

**Pair partner:** ____________________  **First role:** Operator / Observer  **Role swap completed:** yes / no

Use observations from your own computer where possible. If a command/tool is unavailable, write “unavailable” and why. Do not copy the illustrative sample as your evidence.

## 1. Before running

1. In one sentence, what is the kernel responsible for in this exercise?

   The kernel creates the child process and gives it a PID, shares the CPU between the processes, puts the child to sleep while it waits for the terminal and the parent while it waits in `wait()`, and does the actual file write for `output/child-result.txt`.

2. Which program is the parent and which is the child? What is each one’s job?

   `parent.py` is the parent: it starts `child.py` with `Popen`, prints the child PID, waits for it and reports the exit code. `child.py` is the child: it prints its PID/PPID, does a short CPU loop, waits for Enter, writes the synthetic file and exits with `EXIT_CODE`.

3. Prediction before the first run: What will `wait()` make the parent do?

   The parent will stop at `child.wait()` and print nothing more until the child exits. Then it will print that the exit code was 7 and finish normally.

### My execution-boundary diagram

```text
 USER MODE                                   KERNEL MODE
 ---------                                   -----------
 python3 child.py (PID 25627)
   bounded_cpu_work()  <- runs on the CPU, stays in user mode
   text string built in working RAM
   write_text()
     -> open() / write() / close()  ------>  system call entry
                                              VFS -> filesystem (ext4)
                                              page cache -> disk later
     <- bytes written / ok          <------  return to user mode
   return EXIT_CODE -> exit()       ------>  kernel frees the process memory,
                                              keeps exit status for the parent
```

- CPU: runs the counting loop (user mode) and the kernel code during system calls.
- Working RAM: holds `iterations` and the text before it is written. It is freed when the process exits.
- Saved file: `output/child-result.txt` stays on disk after the process is gone.

The counting loop stays in user mode, it needs no system call. What survives exit is the saved file (and the exit status until the parent collects it), not the process memory. Note: a successful `write()` can still be sitting in the page cache, so it does not prove the data would survive a power cut.

## 2. Evidence while the child waited for input

| Field | Your observation or “unavailable” |
| --- | --- |
| OS and Python versions, observation time | Kali Linux rolling, kernel 7.1.5, Python 3.14.7; 2026-11-04 18:36:54 +05 |
| Observed / supplied / simulated | Observed on my own laptop (`evidence/run1-*.txt`) |
| Command/tool used | `ps -o pid,ppid,stat,%cpu,vsz,rss,nlwp,comm -p 25627`, plus `ps ... wchan`, `ls -l /proc/25627/fd`, `/proc/25627/status` |
| Child PID | 25627 |
| Parent PID or PPID | PPID 25619 (`parent.py`); the parent's own PPID is 25590, the shell |
| Process name | python3 |
| CPU value shown (with unit if shown) | %CPU 9.4 (ps average over the process lifetime, mostly the 0.75 s loop); TIME 00:00:00 (rounded to whole seconds) |
| Virtual memory value, if your tool exposes it | VSZ 21840 KiB |
| Working set/RSS (resident memory), if exposed | RSS 12964 KiB (VmRSS 12964 kB in /proc) |
| Thread count, if exposed | NLWP 1 |
| Handles/open resources, if exposed | 3 file descriptors: 0, 1, 2 all point to /dev/pts/2 (the terminal) |
| State/snapshot label, if exposed | STAT `S+` (interruptible sleep, foreground); /proc: `S (sleeping)`; WCHAN `wait_woken`. Parent at the same moment: `S+`, WCHAN `do_wait` |
| Why the child could not continue | It is inside `input()`, reading from the terminal on fd 0. No line was typed yet, so the read cannot return. |

I observed that the child was in state `S` with WCHAN `wait_woken` while the prompt was on the screen; from the code (`input()`) and the open fd 0 -> /dev/pts/2 I infer that it was blocked on the terminal read, because `S` by itself only means sleeping on some event.

## 3. Lifecycle for this run

```text
new --Popen--> runnable/running --CPU phase 0.75 s--> waiting for terminal input --Enter--> runnable/running --return 7--> exited --wait()--> reaped by parent
```

- Creation evidence (`Popen` or `fork`): parent printed `child PID is 25627`, child printed `PID=25627 PPID=25619` (Popen). In the fork demo, `fork()` created PID 27164 from parent 27162.
- Event that made the child wait: `input()` reading stdin from /dev/pts/2 with nothing typed (STAT S, WCHAN wait_woken).
- Event that let the child continue: I pressed Enter in terminal A.
- Exit result reported by parent: `wait() returned; child exit code was 7.` The parent itself exited with status 0.
- What “reaped by parent” means here: the parent collected the child's exit status with `wait()`, so the kernel could remove the child's entry from the process table. Until then an exited child stays as a zombie. After the run `ps -p 25627` showed no process.

The loop can move between runnable and running many times; the print order in the terminal does not show the real scheduling order.

### Windows and POSIX comparison

Observed on Linux with `fork_exec_wait.py` (`evidence/fork-exec-wait-terminal.txt`):

- `fork()` creates a copy of the calling process with a new PID (27164). The copy gets the same memory contents and open file descriptors as the parent.
- `execv()` replaces the program in that same process with `python3 -u child.py`. The PID stays 27164; `ps` showed the command line had changed to `child.py`.
- `waitpid()` in the parent (27162, WCHAN `do_wait`) blocks until 27164 exits, returns the status (exit code 7) and reaps it.

Windows has no `fork()`. `CreateProcess` creates a new process and loads the given program in one call, so there is no copy step. The parent waits on the process handle (`WaitForSingleObject`) and reads the result with `GetExitCodeProcess`. The portable `Popen` route hides this difference; on Linux it may use `posix_spawn` or fork+exec internally, I did not check which.

## 4. Saved synthetic output

- Path you viewed: `P02-process-lab/output/child-result.txt` (copy in `evidence/run1-child-result.txt`)
- List two labels/values in the file: `child_pid=25627`, `requested_exit_code=7` (also `cpu_iterations=8988250`)
- Why is this safe for the classroom lab? It only holds made-up lab values (PIDs, platform name, loop count, exit code), no student records or personal data, it is written only inside the lab folder and needs no admin rights.

## 5. Controlled change

- I changed: `EXIT_CODE` / `CPU_SECONDS`
- New value: ____________________
- My prediction: ______________________________________________________________
- Visible result: _____________________________________________________________
- Did the output file agree with the result? ___________________________________

## 6. Runtime ADR — provisional project runtime

**Title:** Runtime choice for the future lab-seat enrollment project

- **Decision.** Provisional choice: C#/.NET / lecturer-agreed Java:

  ____________________________________________________________________________

- **Context and evidence.** How do mixed developer laptops affect this? What toolchain/support/portability evidence do you have?

  ____________________________________________________________________________

- **Unknowns to check before committing:**

  ____________________________________________________________________________

- **Consequence and trade-off of the provisional choice:**

  ____________________________________________________________________________

- **Supporting mini decision:** Why does this parent wait for its child before reporting the synthetic result?

  ____________________________________________________________________________

## 7. Exit check

Tick each item you can show the teacher:

- [ ] I identified a PID and the parent/child relationship.
- [ ] I explained why `input()` causes the child to wait.
- [ ] I used an observation or honestly marked a tool unavailable.
- [ ] I identified the intentional exit code and synthetic output file.
- [ ] I completed the boundary diagram, lifecycle, Windows/POSIX comparison and ADR.
- [ ] I explained ready versus blocked and why saved output survives exit.
- [ ] I saved this worksheet in the location the teacher specified.
