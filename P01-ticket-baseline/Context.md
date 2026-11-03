# System context

Customer -> Ticket app: booking request
Ticket app -> Customer: booking result
Ticket app -> Email provider: send confirmation for B42
Email provider -> Ticket app: sent or failed

Organiser Claire -> Ticket app: request Friday’s confirmed entry list
Ticket app -> Claire: confirmed customers for Friday
Support Daniel -> Ticket app: look up B42
Ticket app -> Daniel: saved booking and email status, with access policy to agree

These are fictional example messages, not a tested access design. Our own context sketch: [draw and label the same people and messages]
