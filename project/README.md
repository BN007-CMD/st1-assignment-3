# SmartCare v1.0 (course release)

SmartCare is a small console application that clinic staff use to register patients and practitioners, book and cancel appointments, and list a practitioner's appointments. It was built by Online Group 4 for Software Technology 1, Assignment 3, against the **SmartCare A3 Requirements Baseline 2026 revision 2**, UG/common scope.

This is a course release. It makes no claim of production, clinical or security readiness. Use synthetic records only, never real patient information.

## Included capabilities (common scope)

| Requirement | Capability |
|---|---|
| FR-01, FR-02 | Register a patient (unique ID, required name); find a patient by ID |
| FR-03 | Register a practitioner (unique ID, name, specialty); find a practitioner by ID |
| FR-04, FR-05 | Book an appointment for a registered patient and practitioner; reject another SCHEDULED booking for the same practitioner at exactly the same time (a different practitioner at that time is allowed) |
| FR-06, FR-07, FR-08 | Cancel only a SCHEDULED appointment; the same appointment stays in session history as CANCELLED and can still be found by ID |
| FR-09, QRY-01–04, FP-01–03 | List a practitioner's appointments: all statuses by default or one status filter, ordered by date/time then appointment ID, through a pure query function |
| UI-01, UI-02 | Interactive menu over one session store, recovering from invalid menu, ID, date/time and status input |

**Out of scope:** FR-10 persistence is retired, so records last only for the current program session. Also out of scope: PG rescheduling (Stages 10–11), authentication and roles, notifications, billing, clinical rules, patient conflicts, durations and timezones.

## Environment

- Python **3.10 or newer** (the code uses `X | None` type hints). The release was verified on Python 3.13. Use your teaching team's confirmed environment.
- Runtime uses only the standard library. The only development dependency is `pytest==8.3.5` (`requirements-dev.txt`).

## Run and test

From the repository root:

```sh
cd project
python --version
python -m pip install -r requirements-dev.txt
python main.py                  # scripted synthetic demo
python main.py --interactive    # menu; enter 0 to exit
python -m pytest -q             # full suite: 124 passed
cd ..
```

Dates are entered as `YYYY-MM-DD HH:MM` (local time, minute precision). Status filters are blank (all), `scheduled`, `cancelled` or `completed`.

## Structure and responsibilities

```
project/
  main.py                 entry point: demo or --interactive menu
  smartcare/
    domain.py             Patient, Practitioner, Appointment, AppointmentStatus; validation and the guarded cancel() transition
    data_store.py         SmartCareDataStore: the session's three collections (add/find/list) and the practitioner-conflict check
    services.py           PatientService, PractitionerService, AppointmentService: coordinate use cases over one shared store
    queries.py            appointment_sort_key, select_appointments: pure functions over explicit inputs
    console.py            run_menu: input parsing, messages and error recovery; delegates to services
  tests/                  124 pytest tests (starter, domain, services, regressions, queries, workflows, console)
```

- **Lookups:** store lookups return `None` when an ID is absent. Service lookups raise `LookupError`.
- **Errors:** invalid values, duplicates, conflicts and illegal transitions raise `ValueError`.
- **On rejection:** a rejected operation leaves the stored state unchanged.
- **Status changes:** cancellation belongs to `Appointment`, so status changes only through `cancel()`.

## Tests

| File | Covers |
|---|---|
| `test_starter.py` | the 8 supplied scaffold checks (unchanged) |
| `test_domain.py` | entity validation and state rules (Stage 7) |
| `test_services.py` | lookups, booking/conflict and cancellation contracts (Stages 6–7) |
| `test_regressions.py` | the two Stage 8 defects (F8-01 conflict, F8-02 cancelled lookup) |
| `test_queries.py` | QRY and FP query contracts (Stage 9) |
| `test_workflows.py` | service listing and end-to-end UI-01/UI-02 sequences (Stage 9) |
| `test_console.py` | console input handling (Stage 9) |

Requirement IDs are given in test names and docstrings.

## AI use

- **Assistant:** GitHub Copilot was the nominated assistant.
- **Reviews:** each stage's reviewers recorded their own review before running Copilot, then accepted, modified or rejected its suggestions with evidence. Examples: Stage 6 rejected Copilot's claim that list ordering was "only implied"; in Stage 8, Copilot's alternative causes were rejected or modified after runtime checks.
- **Where it's recorded:** details are in each stage record.

## Known limitations

- **Session-only data:** everything is lost on exit.
- **Time handling:** local naive minute-precision times, with no timezone policy.
- **Single user:** one operator, with no concurrency control or authentication.
- **Error messages:** lookup error messages don't include the requested ID.
- **Code style:** some PEP 8 and docstring gaps remain in the code and tests (cosmetic only; listed as debt).

See the Stage 12 record, section G, for the full list and technical debt.
