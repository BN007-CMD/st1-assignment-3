# SmartCare application

Requirements baseline: SmartCare A3 2026 revision 2. Python 3.13 and pytest 8.3.5 verified by the teaching team; Python 3.10 or newer is needed because the code uses `X | None` type hints. Runtime uses only the standard library.

From this directory, using a Python environment with the development dependency installed:

```sh
python -m pip install -r requirements-dev.txt
python main.py
python -m pytest
```

The demo registers synthetic records and books/finds an appointment. Data exists only in this session and is lost on exit; FR-10 restart persistence is retired. Use synthetic information only.

## Current status: Stage 8 complete

Stage 8 (Debugging and Refactoring) diagnosed and repaired two prepared defects in smartcare/data_store.py, added a focused regression test for each, and made one behaviour-preserving refactor. The Stage 8 record, with the diagnosis, Copilot decisions and before/after test evidence, is in stage08/.

| Change | Type | Requirement |
|---|---|---|
| `has_practitioner_conflict` compared practitioner IDs with `!=`; now `==`, so only the same practitioner at the exact time with a SCHEDULED appointment conflicts | Repair (F8-01) | FR-05, AC-04.1/04.2 |
| `find_appointment` skipped cancelled appointments; the status filter is removed, so retained history is found again | Repair (F8-02) | FR-07, AC-05.2/05.3 |
| The conflict check compares status with `AppointmentStatus.SCHEDULED` instead of the string `"scheduled"` | Refactor, no behaviour change | — |

Earlier stages: Stage 6 completed the service operations below; Stage 7 added our domain and service tests, traced to requirements (stage07/).

| Operation | Status | Contract |
|---|---|---|
| `PatientService.find_patient` | Stage 6, done | Returns the registered `Patient`. ID trimmed and case-sensitive; blank/non-text ID → `ValueError`; valid unknown ID → `LookupError`. |
| `PractitionerService.find_practitioner` | Stage 6, done | Same contract for registered practitioners. |
| `AppointmentService.cancel_appointment` | Stage 6, done | Calls `Appointment.cancel()` and returns the same stored object as `CANCELLED`; history is kept. Repeated or COMPLETED cancellation → `ValueError` with no change; unknown ID → `LookupError`. |
| `appointment_sort_key`, `select_appointments`, `list_practitioner_appointments`, `run_menu` | Stage 9 TODO | Still raise `NotImplementedError` by design. `python main.py --interactive` reports the incomplete menu. |

Tests (88 in total; python -m pytest from this directory gives 88 passed): tests/test_starter.py holds the 8 supplied scaffold checks (unchanged). tests/test_services.py holds our Stage 6 service tests and Stage 7 additions (TEST-16 to TEST-33), built on a fresh-store fixture. tests/test_domain.py holds our Stage 7 domain tests (TEST-01 to TEST-15). tests/test_regressions.py holds the two Stage 8 regression tests, one per repaired defect; both failed before the repairs and must be kept. Requirement and acceptance-criterion IDs are in each test's docstring.

## Responsibilities

`domain.py` contains the entities, status and guarded cancellation. `data_store.py` holds three dictionaries through add/find/list methods. The three services share that store and coordinate workflows without bypassing domain rules. Properties provide read-only identity/appointment state; changes go through domain methods.

Service booking accepts IDs and a `datetime` (local, minute precision). The console parser accepts exactly `YYYY-MM-DD HH:MM`. Store lookups return None when absent; service lookups raise LookupError. Invalid values, duplicates, conflicts and illegal transitions raise ValueError. Lists are new containers holding the stored objects. No age, duration, patient-conflict or past-date rules apply.
