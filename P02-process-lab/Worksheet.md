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
- New value: `EXIT_CODE = 0` (was 7) and `CPU_SECONDS = 1.50` (was 0.75)
- My prediction: the parent reports exit code 0 and no longer prints the "non-zero is intentional" line. The CPU phase takes about twice as long, so the loop count should be roughly double.
- Visible result: `CHILD: CPU phase for 1.5 seconds...`, `CHILD: exiting with code 0.`, `PARENT: wait() returned; child exit code was 0.` with no extra line. Loop count 17,899,620 vs 8,988,250 in run 1 (about 1.99x). Parent exit status 0. (`evidence/run2-exit0-terminal.txt`)
- Did the output file agree with the result? Yes: `child_pid=28187`, `cpu_iterations=17899620`, `requested_exit_code=0`.

## 6. Runtime ADR — provisional project runtime

**Title:** Runtime choice for the future lab-seat enrollment project

- **Decision.** Provisional choice: C#/.NET / lecturer-agreed Java:

  C#/.NET, provisional until the lecturer confirms.

- **Context and evidence.** How do mixed developer laptops affect this? What toolchain/support/portability evidence do you have?

  The team uses different laptops (Windows, Linux, macOS), so the runtime has to work the same on all three with the same commands. The .NET SDK runs on all three and the `dotnet` CLI is the same everywhere. The course baseline from P01 already assumes C#/.NET, and the later practice starters include C#. On my laptop: .NET SDK 6.0.400 (runtime 6.0.8) is installed; Java has only a runtime (OpenJDK 25), `javac` is not installed. I have not tested Windows or macOS myself.

- **Unknowns to check before committing:**

  Which .NET version the later labs need (6.0 is out of support, probably 8 or newer); whether the lab PCs in rooms 230/231 have the SDK; editor support on Linux (no Visual Studio, so VS Code/Rider/CLI); whether the lecturer prefers Java for this group.

- **Consequence and trade-off of the provisional choice:**

  Easier: one toolchain and the same build/run commands on every laptop, and it matches the C# starter code in later practices. Trade-off: I need to install a newer SDK; teammates who know Java better have to learn C#; if the lecturer decides on Java we have to switch early, before there is much code.

- **Supporting mini decision:** Why does this parent wait for its child before reporting the synthetic result?

  The parent can only report the result after the child has exited and written the file, and `wait()` gives it the real exit code and reaps the child so it does not stay a zombie. For one short helper there is nothing else for the parent to do, so a synchronous wait is the simplest correct choice.

## 7. Exit check

Tick each item you can show the teacher:

- [x] I identified a PID and the parent/child relationship.
- [x] I explained why `input()` causes the child to wait.
- [x] I used an observation or honestly marked a tool unavailable.
- [x] I identified the intentional exit code and synthetic output file.
- [x] I completed the boundary diagram, lifecycle, Windows/POSIX comparison and ADR.
- [x] I explained ready versus blocked and why saved output survives exit.
- [ ] I saved this worksheet in the location the teacher specified.
