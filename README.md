# Integer Structural Search / ISS

ISS is a bounded structural search engine for integer payloads.

It is intentionally separated from PET / artifact reconstruction.

## Core promise

ISS does not claim to factor arbitrary large integers.

It tries declared, bounded, structural strategies and either returns verified structural payloads or clean failures.

## Guardrail

Factoring-adjacent strategies are rejected by default unless explicitly enabled.
