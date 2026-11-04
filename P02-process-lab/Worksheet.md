# P02 individual worksheet — process evidence and runtime ADR

**Name:** ____________________  **Date:** ____________________  **Operating system:** Windows / Linux / macOS / teacher trace only

**Pair partner:** ____________________  **First role:** Operator / Observer  **Role swap completed:** yes / no

Use observations from your own computer where possible. If a command/tool is unavailable, write “unavailable” and why. Do not copy the illustrative sample as your evidence.

## 1. Before running

1. In one sentence, what is the kernel responsible for in this exercise?

   ____________________________________________________________________________

2. Which program is the parent and which is the child? What is each one’s job?

   ____________________________________________________________________________

3. Prediction before the first run: What will `wait()` make the parent do?

   ____________________________________________________________________________

### My execution-boundary diagram

Draw or write: program/runtime in user mode -> OS interface -> kernel/filesystem -> return. Add CPU, working RAM and saved file. Which calculation stays in user mode? What survives process exit?

____________________________________________________________________________

## 2. Evidence while the child waited for input

| Field | Your observation or “unavailable” |
| --- | --- |
| OS and Python versions, observation time | |
| Observed / supplied / simulated | |
| Command/tool used | |
| Child PID | |
| Parent PID or PPID | |
| Process name | |
| CPU value shown (with unit if shown) | |
| Virtual memory value, if your tool exposes it | |
| Working set/RSS (resident memory), if exposed | |
| Thread count, if exposed | |
| Handles/open resources, if exposed | |
| State/snapshot label, if exposed | |
| Why the child could not continue | |

Do not equate one display label with a complete lifecycle state. Write one sentence that distinguishes **what you observed** from **what you infer**:

____________________________________________________________________________

## 3. Lifecycle for this run

Draw arrows or complete this line with evidence labels:

```text
new → __________________ → __________________ → __________________ → __________________
```

- Creation evidence (`Popen` or `fork`): ___________________________________
- Event that made the child wait: ______________________________________________
- Event that let the child continue: ___________________________________________
- Exit result reported by parent: ______________________________________________
- What “reaped by parent” means here: __________________________________________

### Windows and POSIX comparison

Name what fork creates, what exec replaces, and what wait observes. Explain how Windows CreateProcess differs. Label a supplied POSIX trace if you did not run it.

____________________________________________________________________________

## 4. Saved synthetic output

- Path you viewed: _____________________________________________________________
- List two labels/values in the file: __________________________________________
- Why is this safe for the classroom lab? ______________________________________

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
