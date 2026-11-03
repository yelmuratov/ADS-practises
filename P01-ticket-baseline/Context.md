# System context

People and systems: Customer, Ticket app, Organiser (Claire), Support (Daniel), Email provider.

```
                 availability / book / my booking
   +----------+ ----------------------------------> +------------+
   | Customer |                                     |            |
   +----------+ <---------------------------------- |            |
                 "N available" / "Confirmed S18" /  |            |
                 "Sold out" / "Already booked"      |            |
                                                    |            |
   +-----------+   request entry list for concert   |            |   send confirmation for S18   +----------------+
   | Organiser | ---------------------------------> | Ticket app | ----------------------------> | Email provider |
   |  (Claire) | <--------------------------------- |            | <---------------------------- |                |
   +-----------+   confirmed customers (max 20)     |            |   sent / failed               +----------------+
                                                    |            |
   +-----------+   look up booking S18              |            |
   |  Support  | ---------------------------------> |            |
   | (Daniel)  | <--------------------------------- |            |
   +-----------+   saved booking + email status     +------------+
```

## Messages

| From | To | Message |
|---|---|---|
| Customer | Ticket app | ask availability / book / check my booking |
| Ticket app | Customer | N available / Confirmed S18 / Sold out / You already have S18 |
| Organiser | Ticket app | give me the confirmed list for Friday |
| Ticket app | Organiser | confirmed customers for Friday |
| Support | Ticket app | look up booking S18 |
| Ticket app | Support | saved booking and email status (access policy still to agree) |
| Ticket app | Email provider | send confirmation for S18 |
| Email provider | Ticket app | sent or failed |

The arrows only show who talks to whom. They do not choose a framework or show that access is safe.
