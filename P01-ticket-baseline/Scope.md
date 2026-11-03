# Ticket-app project scope

Fictional brief: a concert organiser needs online reservations instead of booking through messages.

Classroom assumptions: 20 tickets per concert; no numbered seats; one ticket per customer per concert; no payment in version one.

## Problem in our words

Right now the organiser takes bookings through chat messages, so nobody has one reliable list of who actually has a ticket. Customers need to see if a concert still has tickets, book one and later check that their booking really exists. The organiser needs a correct entry list for each concert, and support needs to look up a booking when a customer complains.

## First three actions (version one)

1. View availability for a concert.
2. Book one ticket for a concert.
3. Check the status of my saved booking.

## Later decisions (not in version one)

- Payment: excluded. Version one only reserves a ticket.
- Cancellation: excluded. When a cancelled ticket becomes free again is not decided.
- Waiting list: excluded. We do not know if a sold-out concert should collect names.

## People and needs

| Person | Action | Result they need |
|---|---|---|
| Customer (e.g. Nodira) | Opens a concert, presses Book, comes back later to check | An honest answer: Confirmed with a booking number, or Sold out. Later the same saved booking, not a new one |
| Organiser (Claire) | Asks for the confirmed list for one concert | Exactly the confirmed customers for that concert, never more than capacity |
| Support (Daniel) | Looks up a booking a customer reports | The saved booking and its email status, without creating or changing a booking |

## Unanswered questions and who can answer

| Question | Who can answer |
|---|---|
| If cancellation is added later, does the ticket go back on sale immediately or after the organiser checks it? | Claire (organiser) |
| Should a sold-out concert offer a waiting list, and in what order are people taken from it? | Claire (organiser) |
| Is "one ticket per customer" checked by account, phone number or email? | Claire with the teacher |
| What is support allowed to see about a customer (name, phone, email)? | Claire and the teacher (access policy) |
