# Ticket requirements and rules

Format for every example: starting situation -> customer action -> visible result -> saved-data change.

## Three functional needs

### 1. View availability

- Start: Saturday's concert has capacity 20 and 17 confirmed bookings.
- Action: Nodira opens the Saturday concert page.
- Visible result: "3 tickets available".
- Saved data: no change, still 17 bookings.

Note: the number is only a snapshot. Seeing "3 available" does not reserve anything for Nodira.

### 2. Book a ticket (ticket available)

- Start: Saturday has 17 of 20 confirmed. Nodira has no booking for Saturday.
- Action: Nodira presses Book.
- Visible result: "Confirmed. Booking S18."
- Saved data: one new booking (Nodira, Saturday) is saved. Total becomes 18.

### 3. Check booking status

- Start: booking S18 exists for Nodira. The confirmation email has not been sent yet.
- Action: Nodira opens "My booking" for Saturday.
- Visible result: "Confirmed, booking S18. Email: pending."
- Saved data: no change. Checking never creates a booking, total stays 18.

## Booking rules

### Capacity rule

Confirmed bookings for one concert must never be more than that concert's capacity.

### Duplicate rule

One customer has at most one confirmed booking per concert. If they try again, return the booking they already have.

### Sold-out example

- Start: Friday has 20 confirmed bookings for 20 tickets.
- Action: Bekzod presses Book for Friday.
- Visible result: "Sold out."
- Saved data: no new booking. Total stays 20.

### Same customer presses Book twice

- Start: Saturday has 18 of 20. Nodira already has booking S18.
- Action: Nodira presses Book for Saturday again (for example she thought the first click did not work).
- Visible result: "You already have a booking for this concert: S18."
- Saved data: no new booking. Total stays 18 and Nodira still has exactly one booking.

### Two people want the last ticket (rule only)

- Start: Saturday has 19 of 20. Nodira and Bekzod have no booking.
- Action: both press Book at almost the same time.
- Expected result: one of them gets Confirmed, the other gets Sold out. Final total is 20, never 21.
- We only wrote the expected result. How the app protects this is not designed or tested yet.

## Three quality concerns

| Concern | Condition | Required outcome | Proposed check |
|---|---|---|---|
| Accessibility | Customer uses only the keyboard | Can reach Book, press it and read the result; focus is always visible | Later, go through the booking path with Tab/Enter only and note any step that does not work |
| Response time | Agreed number of customers check status at the same time on an agreed test setup | Status shown within the agreed time | Measure time from request to shown result and write down the load and environment. Numbers: to agree, not measured |
| Recovery after email failure | Email provider fails after the booking is saved | Booking stays confirmed and can still be found; email shows as pending or failed | Later, simulate an email failure and check the saved booking and its email status |

Unknown numeric targets: to agree with the teacher/organiser. Nothing here is measured.
