# Evidence index

Labels: proposed / simulated / observed.

| # | Label | Requirement | Actions | Expected outcome | Actual outcome | Environment | Limitation |
|---|---|---|---|---|---|---|---|
| E1 | Proposed | Sold out (Requirements.md) | Start Friday at 20/20, Bekzod presses Book, check screen and saved count | "Sold out", total stays 20 | Not run | Not applicable yet | A plan cannot prove an implementation works |
| E2 | Proposed | Duplicate rule | Nodira has S18, presses Book again | "You already have S18", total unchanged | Not run | Not applicable yet | Does not cover two requests arriving at the same moment |
| E3 | Simulated | Last ticket with two customers | On paper: both read 19, both save, total becomes 21 | Shows why a check-then-save without protection is unsafe | 21 on paper | Paper model from class | Not an observation from a real database |
| E4 | Observed | Tool access | Ran version commands for git, dotnet, psql | Tools respond | git 2.53, .NET SDK 6.0.400, psql 18.6; PostgreSQL service inactive | Kali Linux laptop | Only checks the tools exist, not that the labs run |

No executable booking application or tested concurrency lab is included in this baseline.
