# Completed example: a first ticket-app plan

Read this model before filling in the templates. It is a fictional classroom plan, not a tested application. Use its structure and explain your own decisions. P01 requires no coding.

## Brief, people and scope

Claire organises a Friday concert and currently receives booking requests through messages. Separate replies make it hard to know who has a ticket. A proposed ticket app lets customers view availability, book and retrieve a saved result; Claire can inspect the entry list and support worker Daniel can investigate a booking.

Classroom assumptions: Friday has 20 unnumbered tickets; each customer has at most one confirmed booking per concert. Version one includes availability, booking and checking saved status. Payment, cancellations and a waitlist are excluded. These are teaching assumptions, not confirmed requirements from a real organiser.

Customer Alex needs an honest booking result. Claire needs an accurate list for entry. Daniel needs to look up the existing record without making another booking. Unresolved question: if cancellations are introduced later, when should a ticket become available? Claire owns that policy decision; it stays unresolved today.

## Three functional needs: complete behaviour examples

1. View availability. Start: Friday has 19 confirmed bookings for 20 tickets. Action: Emma opens Friday. Visible result: 1 ticket available. Saved data: no change; still 19. Availability is a snapshot, not a promise that Emma owns the ticket.
2. Book. Start: Friday has 19 confirmed bookings and Alex has no Friday booking. Action: Alex taps Book. Visible result: Confirmed, booking B42. Saved data: one Alex/Friday booking is added; the total becomes 20. B42 is an invented example identifier.
3. Check status. Start: B42 exists for Alex and email is pending. Action: Alex reopens Friday and checks his booking. Visible result: Confirmed B42, email pending. Saved data: no extra booking is added; the total stays 20.

## Rules and failure examples

Capacity: confirmed bookings must never exceed that concert's capacity. Start: Friday has 20 bookings for 20 tickets. Emma taps Book. Show Sold out; save no new booking; total stays 20.

Duplicate rule: each customer has at most one confirmed booking per concert. Start: Alex already has B42 for Friday. He taps Book again. Return B42; add no booking. This rule also covers a new request for the same customer and concert, not only a repeated request identifier.

Overlapping requests: start with 19 of 20 and two customers without bookings. After both request the last ticket, exactly one new booking is confirmed, the other gets Sold out, and the final count is 20. We have specified the result; we have not implemented or tested a protection mechanism.

Saved booking and lost reply: if B42 was saved but Alex did not receive the reply, show that status is being checked and retrieve B42. A missing reply does not prove no booking exists.

Email failure: keep B42 confirmed and record email pending. Retrying email must not create a booking or remove B42.

## Three quality concerns and planned checks

1. Accessibility. Condition: a customer uses only a keyboard. Required outcome: reach Book, activate it and read the result with a visible focus indicator. Proposed check: follow that path using keyboard controls in the later app; record any inaccessible step.
2. Response time. Condition: an agreed number of customers request status under a stated test setup. Required outcome: status appears within the agreed target. Proposed check: measure request-to-result time and record load and environment. Numeric load and target: to agree with the teacher/Claire; not measured today.
3. Recovery. Condition: email delivery fails after B42 is saved. Required outcome: B42 remains retrievable and email pending can be investigated. Proposed check: later simulate email failure and inspect the saved booking and delivery status. No running app is provided in this pack.

## Context sketch: complete labelled connections

Customer -> Ticket app: ask availability / book / check own status
Ticket app -> Customer: availability / Confirmed B42 / Sold out / checking status
Claire (organiser) -> Ticket app: request Friday’s confirmed entry list
Ticket app -> Claire: confirmed customers for that concert
Daniel (support) -> Ticket app: look up the reported booking
Ticket app -> Daniel: saved booking and email status, subject to an agreed access policy
Ticket app -> Email provider: send confirmation for B42
Email provider -> Ticket app: sent or failed delivery result

These arrows describe communication. They do not select a programming framework, prove safe access or demonstrate a working application.

## Five agreed business terms

- Capacity: maximum confirmed bookings allowed for a specified concert; Friday's example capacity is 20.
- Concert: one event at a stated date and time; Friday and Saturday have separate capacities and bookings.
- Confirmed booking: a saved record giving one customer entry to one concert. Email arrival is a separate status.
- Sold out: confirmed bookings have reached that concert's capacity; another booking must not be added.
- Cancellation: a possible future action removing a booking entitlement. It is excluded from version one; release and notification policy remain unresolved.

## Work, tools and feedback

Illustrative pair only: Sam drafts scope and needs; Mira checks those and drafts the context and glossary; both review the rules. Replace these names with your actual pair. Each student uses their own signed-in worksheet and writes an individual reflection. Agree shared answers, then each records them; keep one shared copy of the baseline files if you use the ZIP.

Tools example: browser and text editor available after opening a test document; Git and database tools not checked yet. Owner: Sam; next action: ask the teacher which versions later labs require. C#/.NET and PostgreSQL are planning assumptions to confirm. P01 does not require installation or coding.

Feedback before: “Booking should be fast.” Feedback after: “Under an agreed load and environment, measure request-to-result time against a target to agree.” Reason: the original claim had no conditions or way to check it. Limit: the numeric target and load still need agreement.

## Evidence: keep the labels honest

Proposed: the sold-out requirement above; planned later check starts at 20/20, sends Book and inspects the screen and saved count. Actual result: not run. Environment: not applicable yet. Limit: this plan cannot prove that an implementation works.

Simulated: the classroom unsafe sequence starts at 19, both read 19, then both save, ending at 21. This is a simplified model, not an observation from a live database.

Observed: only record an app result after running it. For today's document work you may record an actually completed peer review, with the changed sentence; that does not count as a booking-system test.

## Individual reflection example

“I checked the repeat-booking rule and added the saved-data result to the status requirement. Returning B42 prevents a second entitlement for Alex/Friday. I still do not know how to protect this rule under overlapping requests. My next goal is to explain how running requests share CPU time in P02 and later compare database protection.”

## Optional design decision

An ADR is a short architecture decision record: problem, alternatives, choice, costs, evidence and when to reconsider. If useful, fill decisions/Decision-template.md or your own notes. It is not an additional mandatory P01 worksheet field. Example proposed choice: keep booking and email as separate jobs inside one application; cost: release together; reason: small first version; evidence: brief only, not a benchmark; reconsider if independent release becomes a demonstrated need.
