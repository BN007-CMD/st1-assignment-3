# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Online Group 4, Tuesday 17:30 tutorial
Members and responsibilities: Novica Baloski (@BN007-CMD, UG); Emilio Rojas-Terry (@ucemilio, UG); Quang Le, (@quangle330, UG); Brendan Potter (@BrendoAC11, UG)
Stage 8 integrated SHA, command, working directory and actual result: SHA: b3a3b5800276979112cf7329ac5bb08c62bbb86f, Command: python -m pytest -q, working directory: project/, result: 88 passed in 0.08s

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Required session/domain state | FR-01, FR-02, Must persist across multiple searchs and bookings  |
| Appointment history | Required session/domain state | FR-07, AC-05.2, Persistent record that must survive beyond a single request; stored in SmartCareDataStore._appointments |
| Temporary menu choice | transient state | No requirement states that this needs to be retained |
| Practitioner specialty | Required session/domain state | FR-03, Practitioners need to have a specialty and it needs to be searchable |
| Debug print output | transient state | Output will be based on the current run and should not be stored |
| Appointment status | Required session/domain state | BR-06/07/08, AC-05.1-05.3, Cancelled appointments need to be stored and other appointments need to be searchable  |

What is intentionally lost on exit? The whole session is intentionally lost as FR-10 states. Between session persistence is not to be implemented.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | tuple[datetime, str] = (appointment.date_time, appointment.appointment_id) | A read only key that returns the appointment without modifying it, no validation required as it assumes a valid appointment | Appointment.date_time and Appointment.appointment_id from domain.py |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus | list[Appointment] | Filter to the requested practitioner, restrict to the choosen AppointmentStatus, sort using appointment_sort_key, assume valid filter values | Appointment.practitioner.practitioner_id, Appointment.status  |
| Service listing | practitioner_id: str, status: AppointmentStatus | list[Appointment] | Validate the practitioner using the existing find_practitioner, validate a status from AppointmentStatus | SmartCareDataStore.find_practitioner, list_appointments |
| Console | Menu choice; Patient ID; Patient name; Practitioner ID; Practitioner Name; Specialty; Appointment ID; date and time; Status | Print next prompt/result or error message and loop | Prompt user, call existing services, display results, recover from errors and reutnr to menu. All validation should be handled by services/domains | Reuse parse_date_time and format_appointment from console.py |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: patient_id - Patient._patient_id - must be a string, not blank; name - Patient.name - must be string, not blank; practitioner_id - Practitioner._practitioner_id - must be a string, case sensitive and not blank; name - Practitioner.name - must be string, not blank; specialty - Practitioner.specialty - must be string, not blank; appointment_id - Appointment._appointment_id - must be a string, not blank, and immutable; actual participants - Appointment._patient/Appointment._practitioner - a valid patient/practitioner object; - date_time - Appointment._date_time - a valid date time using the strict parse_date_time format; status - Appointment._status -  must be an AppointmentStatus enum

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | Domain doing input | Console asks, service calls and the domain only guards transition |
| Service prints/reads the menu | Service doing print | Console controls the menu, the service should never print  |
| Query sorts its source in place | This mutates the source and returns none | inside the query return a new list that can be filtered |
| Store prints Appointment saved | Store doing print | store should only return the object and the console controls printing |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: 

source = [a3, a1, a2]
before_ids = [a.appointment_id for a in source]   
before_objs = list(source)

result = sorted(source, key=appointment_sort_key) 

assert [a.appointment_id for a in source] == before_ids
assert source == before_objs

assert result is not source
assert id(result) != id(source)

assert all(r is s for r in result for s in source if r.appointment_id == s.appointment_id)

assert [a.appointment_id for a in result] == ['A1', 'A2', 'A3']

Score-example prediction and explanation of passing the named key:

def score_key(item: tuple[str, int]) -> tuple[int, str]:
    return item[1], item[0]

scores = [('Bea', 8), ('Ali', 8), ('Chen', 5)]
ordered = sorted(scores, key=score_key)

sorted returns a new list that is different from the scores list which still is unchanged and has the original order

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: 

Cancelling doesn't remove an appointment, it just changes its status. FR-06/BR-06 say only a SCHEDULED appointment can be cancelled, so it goes from SCHEDULED to CANCELLED. FR-07/AC-05.2 say the same appointment has to stay in the history for the session, and BR-07 says cancellation changes the state and doesn't delete history. In our code, Appointment.cancel() checks the status is SCHEDULED (otherwise ValueError) and then sets _status = CANCELLED. It never removes anything from the store's _appointments. The service returns the same object, just now CANCELLED. If I deleted it instead, the history would be gone (FR-07), I couldn't find it by ID anymore (AC-06.1), a second cancel would look like an unknown ID instead of a rejected repeat (AC-05.3), and it wouldn't show up in an all-status list (QRY-02). So cancelling keeps the same object, ID and participants and only changes the status.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| FR-01/02 patient register & find | Patient ID and name | PatientService.register_patient / find_patient and SmartCareDataStore.add_patient/find_patient | Valid unused ID stored; duplicate rejected without overwrite; unknown lookup reported | |
| FR-03 practitioner register | Practitioner Id, name and specialty | PractitionerService.register_practitioner / find_practitioner and add_practitioner/find_practitioner | Unique ID/name/specialty stored; duplicate rejected | |
| FR-04/05 booking & conflict | Appointment ID, registered patient ID, registered practitioner ID, parsed datetime | AppointmentService.book_appointment and add_appointment, has_practitioner_conflict | Registered participants with unique ID and free time = SCHEDULED, otherwise reject | |
| FR-06/07 cancel & retain | Appointment ID | AppointmentService.cancel_appointment to Appointment.cancel() | Status from same object can go from SCHEDULED to CANCELLED, remains in history | |
| FR-08 find appointment | Appointment ID | AppointmentService.find_appointment store find_appointment | Known ID returns that appointment | |
| FR-09 list + query contracts | Practitioner ID, AppointmentStatus | AppointmentService.list_practitioner_appointments | List Practitioner's appointments using a filter | |
| Service listing error cases | Practitioner ID, Status | AppointmentService.list_practitioner_appointments | Unkown returns LookupError, blank or invalid returns ValueError | |
| UI-01/UI-02 menu | Menu choice | console.run_menu, calls services | Repeated menu, all commands work, recoverable errors, state preserved on rejection | |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection:

QRY-01 - select_appointments filters on appointment.practitioner.practitioner_id. Book appointments for DR1 and DR2, then list DR1: only DR1's appointments appear, and DR2's are absent (the control)
QRY-02 - status=None means every status, including CANCELLED and COMPLETED, so retained history appears. Passing an explicit AppointmentStatus restricts to that status
QRY-03 - Results are ascending by (date_time, appointment_id) using the named key, so equal times tie-break on ID. The source list order and every object's fields are unchanged
QRY-04 - The three listing outcomes are kept separate — empty, unknown and invalid
FP-01 - The query gets everything through its arguments and doesn't use a hidden store, print, read input or call services. appointment_sort_key only reads date_time and appointment_id
FP-02 - For empty, sorted and unsorted inputs it returns a new list, but the Appointment objects inside are the same references, not copies, and are never changed 
FP-03 - Pass appointment_sort_key itself as the key function, test the key on its own, and check sorting actually uses it; repeated calls give the same result.
UI-01 - The menu repeats until 0, using one store and one set of services for the whole session, not recreated each loop
UI-02 - Print a message and return to the menu. After each rejection, check the records and carry on

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| QRY-01 practitioner isolation (+ control) | smartcare/queries.py to select_appointments; test in tests/test_queries.py | Book appointments for DR1 and DR2; select_appointments(all, 'DR1') returns only DR1's, and every result has practitioner.practitioner_id == 'DR1'; DR2's appointment is absent (control) | Pass — only DR1's returned, DR2 excluded | tests/test_queries.py::test_qry01_practitioner_isolation |
| QRY-02 default all statuses | queries.py to select_appointments (status=None) | With status=None, SCHEDULED, CANCELLED and COMPLETED fixtures are all included; assert all three statuses present | Pass — all statuses included | tests/test_queries.py::test_qry02_default_all_statuses |
| QRY-02 each explicit enum status | queries.py to select_appointments (status filter) | For each of SCHEDULED, CANCELLED, COMPLETED, assert every returned appointment has that exact status and others are excluded | Pass — each filter returns only its status | tests/test_queries.py::test_qry02_each_status_filter |
| QRY-02 no-match to empty list | queries.py to select_appointments | Valid practitioner with no appointment of a given status to result == [], isinstance(result, list), no error | Pass — new empty list | tests/test_queries.py::test_qry02_no_match_empty |
| QRY-03 equal-time ID tie-break | queries.py to appointment_sort_key; select_appointments | Cancelled/completed fixtures share a date_time (A10, A2); assert exact sequence ['A10', 'A2'] by (date_time, appointment_id) lexicographic order | Pass — datetime then ID | tests/test_queries.py::test_qry03_tie_break |
| FP-03 named key tested directly / reused | queries.py to appointment_sort_key | Call key directly: returns (a.date_time, a.appointment_id) and leaves a unchanged; result ordering uses that key (keys non-decreasing) | Pass — key output correct, no mutation, used for sort | tests/test_queries.py::test_fp03_sort_key_direct |
| FP-02 empty input to fresh list | queries.py to select_appointments | select_appointments([], 'DR1') to result is not source and result == [] | Pass — distinct empty list | tests/test_queries.py::test_fp02_empty_fresh_list |
| FP-02 already-sorted input to fresh list | queries.py to select_appointments | Already-sorted source: result is not source, id(result) != id(source), same order, same objects (all(r is s ...)) | Pass — new container, same objects | tests/test_queries.py::test_fp02_sorted_fresh_list |
| FP-02 unsorted input to fresh list | queries.py to select_appointments | Unsorted source: result is not source, result sorted, source order unchanged | Pass — new sorted list, source untouched | tests/test_queries.py::test_fp02_unsorted_fresh_list |
| FP-01/FP-02 unchanged source order/fields + repeated calls | queries.py to select_appointments | Snapshot source ID order and (id, date_time, status, patient, practitioner); call twice; assert source unchanged and both calls equal-ID sequences (repeatability) | Pass — source unchanged, repeated calls equal | tests/test_queries.py::test_fp_repeat_no_mutation |
| QRY-04 known practitioner, no matches | smartcare/services.py to list_practitioner_appointments; test in tests/test_workflows.py | Registered practitioner with no appointments or no matching status to result == [], no error | Pass — empty list | tests/test_workflows.py::test_qry04_known_empty |
| QRY-04 valid unknown practitioner | services.py to list_practitioner_appointments to find_practitioner | Well-formed ID not registered to pytest.raises(LookupError) | Pass — LookupError | tests/test_workflows.py::test_qry04_unknown |
| QRY-04 blank/invalid ID | services.py; store find_practitioner to required_text | Blank or non-string ID to pytest.raises(ValueError) | Pass — ValueError | tests/test_workflows.py::test_qry04_invalid_id |
| QRY-04 non-enum status | services.py to list_practitioner_appointments (isinstance(status, AppointmentStatus)) | Known practitioner, status='scheduled' to pytest.raises(ValueError); not treated as no matches | Pass — ValueError | tests/test_workflows.py::test_qry04_non_enum_status |
| AC-05.2 / FR-07 retained history | services.py to cancel_appointment; queries.py to select_appointments | Cancel A1; same object now CANCELLED; find_appointment('A1') still returns it; all-status listing includes it; SCHEDULED-only listing excludes it | Pass — retained, in all-status, out of SCHEDULED-only | tests/test_workflows.py::test_cancel_retained_history |
| UI-01 integrated menu sequence | smartcare/console.py to run_menu; main.py | One store/services: register, find, book, reject conflict, cancel, find CANCELLED, list all then SCHEDULED-only, book freed slot, exit | Pass — session behaves as specified | stage09_evidence/ui01_transcript.txt (+ tests/test_workflows.py::test_ui01_sequence) |
| UI-02 recoverable errors, state preserved | console.py to run_menu | Invalid menu, blank/unknown ID, duplicate register, unknown participant, bad date/time, unknown appointment, repeat cancel, invalid status — each shows message and continues; records unchanged after each | Pass — errors recovered, before/after state identical | stage09_evidence/ui02_transcript.txt |
| NFR-01 unchanged state on rejection | data_store.py to add_appointment (validate-before-insert); services.py | Failed booking/cancel/duplicate leaves store contents, source order and fields unchanged; invalid booking does not reserve ID | Pass — snapshots identical after failures | tests/test_workflows.py::test_rejection_no_partial_state |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O:

select_appointments uses only its parameters (appointments, practitioner_id, status). It has no print, input, file, network or logging calls. It builds a new list via comprehension and sorts with sorted(..., key=appointment_sort_key), so the argument is never sorted in place or modified; it never assigns to appointment.***. appointment_sort_key only reads date_time and appointment_id and returns a tuple. Because both depend solely on their arguments, identical inputs give identical results, and shared Appointment objects in the result are never changed. Practitioner-registration and enum validation live in AppointmentService.list_practitioner_appointments

What the tests do and do not establish:

They establish the observed behaviours; practitioner isolation with a control, default all-status and each explicit enum filter, no-match empty list, datetime-then-ID ordering with tie-break, direct key output and reuse, fresh list containers for empty/sorted/unsorted inputs, unchanged source order/fields, repeatability, the known-empty/unknown/invalid service distinctions, retained cancelled history, and unchanged state after rejections. They support but do not prove purity: passing tests only cover the inputs exercised and cannot show the absence of hidden state or I/O on untested paths, that rests on the code inspection. They show outputs are correct for the cases tested, not that every possible input is handled, and the is-identity and snapshot assertions are only as complete as the fields snapshotted. Purity, absence of side effects and full validation coverage remain claims backed by code review plus representative tests, not exhaustive proof.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | Console session: 1 P1 Alex Example; 3 D1 Taylor Example / General practice; 3 D2 Sam Example / Cardiology; 2 P1; 4 D1; 5 A1 P1 D1 2026-10-01 09:00; 5 A2 P1 D1 2026-10-01 09:00 (conflict); 5 A2 P1 D2 2026-10-01 09:00; 6 A1; 7 A1; 8 D1 (blank); 8 D1 scheduled; 5 A3 P1 D1 2026-10-01 09:00; 8 D1; 0 | Register/find works; A1 booked SCHEDULED; conflict A2/D1 rejected; A2/D2 booked (different practitioner allowed); A1 cancelled and still found as CANCELLED; all-status list includes A1, SCHEDULED-only omits it; A3 books the freed slot; exit discards session | All as expected. After conflict rejection A2/D1 was not stored (no reserved ID); A2/D2 stored; A1 retained with CANCELLED status and still returned by find and all-status list; SCHEDULED-only list excluded A1; A3 booked at the freed time; exit message shown | stage09_evidence/ui01_transcript.txt |
| UI-02 invalid-input recovery | Console session: 9 (unknown choice); 2 with blank ID; 1 P1 Alex Example; 1 P1 Another (duplicate); 5 A1 P9 D1 2026-10-01 09:00 (unknown patient); 5 A1 P1 D1 2026-13-01 09:00 (impossible date); 3 D1 Taylor Example / General practice (forgot to do earlier); 5 A1 D1 P1 2026-10-01 09:00 (typo by me); 5 A1 P1 D1 2026-10-01 09:00 (valid); 6 A1; 6 A1 (repeat); 8 D1 badstatus; 8 D1; 0 | Each invalid input shows a message and returns to the menu; records unchanged after each rejection; subsequent valid action succeeds | Unknown choice and invalid status printed an error and menu returned; blank/unknown/duplicate IDs reported; unknown participant LookupError shown, no appointment stored; impossible date rejected by parser, no record; valid booking then succeeded; repeat cancel rejected with status still CANCELLED; listing with bad status rejected but subsequent 8 D1 worked. State checks before/after each rejection unchanged; invalid booking did not reserve A1 | stage09_evidence/ui02_transcript.txt |
| Automated service workflow | python -m pytest -q tests/test_workflows.py | Integrated sequence: register/find patient and practitioners, book, conflict rejection, different-practitioner booking, cancel, retrieve, all-status vs SCHEDULED-only listing, freed-slot booking, plus duplicate/unknown/repeat-cancel rejections leave state unchanged | All Pass | tests/test_workflows.py::test_ui01_sequence, run log at stage09_evidence/pytest_workflows.txt |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI:

smartcare/queries.py (appointment_sort_key, select_appointments), AppointmentService.list_practitioner_appointments in smartcare/services.py, and the run_menu console dispatch.

Actual prompt/context supplied:

Act as a query and console integration reviewer for SmartCare.
Review the supplied code and tests for:
1. explicit inputs, purity and source non-mutation;
2. domain, service, data-store and console responsibilities;
3. validation and recovery without partial state changes;
4. correct object identity, enum filtering and ordering;
5. retained history and integrity risks;
6. missing query, workflow and console tests.
Do not redesign the domain or add storage/frameworks.
Do not invent fields or requirements or delete cancelled history.
Separate observed evidence from optional improvements.
Rank findings as Critical, Important or Optional.
For each finding, identify the code/test evidence to check.

Actual response: 

Observed evidence

No Critical implementation defect surfaced in the reviewed paths.

select_appointments filters using enum identity and sorts a new list; the query tests cover isolation, each status, ordering, fresh lists, and source non-mutation in test_queries.py.
AppointmentService.list_practitioner_appointments validates the practitioner and status before delegating. Booking validates participants and checks duplicate IDs/conflicts before storing; cancellation delegates to the domain transition. The store preserves appointment objects, including cancelled history.
The console converts status text to enum values and catches expected ValueError/LookupError exceptions in console.py.
Findings
Rank	Finding	Evidence to check
Important	Console behavior lacks automated coverage. The menu handles registration, booking, cancellation, lookup, listing, input parsing, and recovery, but the tests contain no calls to run_menu or parse_date_time, nor input/output assertions. The workflow tests exercise services directly, not the console integration. This leaves menu wiring, status parsing, and recovery behavior unverified.	run_menu, test_workflows.py, tests/

Optional	The workflow “no partial state” assertion is a shallow snapshot. before contains references to the same mutable appointments, and a successful cancellation occurs before the final comparison. Comparing the lists therefore checks membership/order, not unchanged appointment fields or status. Other service tests cover several failure cases, so this is a weakness in this specific workflow assertion rather than evidence of a current state-mutation bug.	test_rejection_no_partial_state

Optional	README Stage 9 status is stale. It says the query/menu functions still raise NotImplementedError, although the reviewed code implements them.	README.md

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| Console behaviour lacks automated coverage — menu handles registration, booking, cancellation, lookup, listing, parsing and recovery, but no test calls run_menu or parse_date_time; workflow tests exercise services directly, leaving menu wiring, status parsing and recovery unverified | smartcare/console.py to run_menu; tests/test_workflows.py; tests/ | Important | Accept — accurate and within scope. It does not demand a new framework or persistence, just test coverage of existing console code, which the doc's Section 7 explicitly asks for (separately exercise the real console; a subprocess test is useful). Leaving it would mean menu wiring, enum conversion and error recovery are only shown by manual transcript, not automated | Modify/strengthen — add a subprocess or captured-stdio test for run_menu covering: a valid register/book/list sequence, an unknown menu choice, a blank/unknown ID, a non-enum status, and a rejected booking followed by a successful action. Also test parse_date_time directly for valid, malformed and impossible inputs. Keep the manual UI-01/UI-02 transcripts as evidence too, since the doc says not to replace menu verification with service tests alone | Re-run pytest -q; new console tests pass and the failure-then-recovery case shows the menu continuing with state unchanged; parse_date_time tests confirm ValueError on bad input |
| No partial state assertion is a shallow snapshot — before holds references to the same mutable appointments and a successful cancellation happens before the final comparison, so the check is membership/order, not unchanged fields/status | tests/test_workflows.py::test_rejection_no_partial_state | Optional | Accept — correct observation. It is a real weakness in that assertion, not a state-mutation bug (other service tests cover failures). Worth fixing because the doc asks for before/after state checks and warns that length/membership alone is not proof | Modify — move the snapshot to after the legitimate cancel and compare field tuples (appointment_id, date_time, status, patient, practitioner) before and after the remaining failed calls, so the test proves failures do not mutate fields. Keep membership check too | Re-run the test; it passes with the stricter field comparison, and deliberately mutating a field in a scratch run would make it fail (confirming it now catches field mutation) |
| README Stage 9 status is stale — it says the query/menu functions still raise NotImplementedError, though the code implements them | README.md; smartcare/queries.py; smartcare/console.py | Optional | Accept — factual and trivial to fix. The doc's Section 9 requires updating the README with working commands, scope and limitations, so a stale status contradicts that requirement | Modify — update README: list python main.py --interactive and python -m pytest -q, note session-only data (FR-10 retired), the supported menu commands, and remove the NotImplementedError status | Open README and confirm it matches actual commands and implemented scope; links to stage09_evidence/ resolve |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate:

Domain invariants (domain.py). Patient, Practitioner and Appointment validate their own fields and hold the rules: required_text rejects blank IDs/names, validate_date_time enforces naive minute-precision datetimes, and Appointment.cancel() owns the guarded SCHEDULED to CANCELLED transition, raising ValueError for illegal states. Identity fields are read-only. The domain knows nothing about the store, services, console or file I/O, so these invariants hold wherever the objects are used.

Shared-store collections (data_store.py). SmartCareDataStore owns the three in-memory dicts and the relationships between registered objects. add_patient/add_practitioner reject wrong types and duplicates; add_appointment checks with is that the participants are the actual registered objects and validates before inserting, so a failed insert changes nothing. find_* returns None for a valid absent ID; has_practitioner_conflict checks only SCHEDULED appointments at the exact time. The store holds data and lookups — it does not print, prompt or decide workflow.

Service coordination (services.py). Services sit between the console and the store/domain. AppointmentService.book_appointment looks up participants, builds the Appointment (letting the domain validate), checks duplicate ID and practitioner conflict, then stores it. cancel_appointment finds the object and delegates the transition to Appointment.cancel(). list_practitioner_appointments validates the practitioner through the store and the status is an AppointmentStatus, then calls the pure query with the registered ID. Services do coordination and validation; they never do presentation and never re-implement domain guards (they call cancel(), they don't set _status themselves).

Pure queries (queries.py). appointment_sort_key and select_appointments take explicit inputs, use no store or global state, perform no I/O and return a new list sorted with the named key; the Appointment objects inside are shared but never modified. Because the pure layer assumes valid objects/filter values, it stays independent of registration rules, which keeps it testable with plain lists and repeatable for identical inputs.

Console effects (console.py / main.py). run_menu owns all interaction: it creates one store and one set of services for the session, prompts and parses input (reusing parse_date_time and format_appointment), converts status text to AppointmentStatus at the boundary, calls services, displays results, and catches ValueError/LookupError to show a message and return to the menu. It doesn't duplicate domain guards or conflict rules and doesn't catch every exception. All side effects, reading input, printing, choosing which service to call, are confined here.

How they stay separate. Data flows one way: console to service to store/domain, with the pure query called by the service and returning a list back up. Domain rules are enforced only in domain.py; the store enforces collection integrity and object identity; services orchestrate and validate existence/status; the pure query only selects and orders; the console only does input/output and enum conversion. No layer reaches around another — the query has no store, the store has no printing, the domain has no I/O, and the console has no domain rules. This is what keeps each layer independently testable (NFR-02) and the query provably pure by inspection (FP-01), and it's why Copilot's Important finding (missing console tests) is a coverage gap rather than an architectural defect — the boundaries themselves held.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? The architectural bit was deciding which layer does what. When I integrated the listing, the hard question wasn't how to filter or sort — that's a few lines. It was: does the pure query decide if a practitioner exists, or does the service? I put that check in list_practitioner_appointments, not in select_appointments, because giving the query store access would break purity and stop it being testable with plain lists. The same split applied to the console: turning status text into an enum and catching errors belongs at the menu, not in the service or domain. Getting those boundaries right was the real integration work; the filtering and sorting were the easy part. That's what NFR-03 is for, keeping domain rules, coordination, pure queries and console effects separate.


2. Which Copilot suggestion did you reject as over-engineering, and why? I didn't reject any of the three it gave, the missing console tests (Important), the shallow no-partial-state assertion (Optional) and the stale README (Optional) were all fair and in scope, so I accepted them. What I would reject is the kind of suggestion the review prompt warns against: adding persistence (SQLite, files, a repository), new frameworks or dependencies, inventing fields, or deleting cancelled history. Those go against the requirements, FR-10 is retired so persistence is out of scope, and BR-07 says cancelled history must be kept. If Copilot had proposed any of that, I'd have rejected it as over-engineering. Its actual findings stayed inside our existing contracts, so they were accepted and verified.


3. How did you prove cancelled appointments remain retrievable and listable in the same session? After booking A1, I cancelled it and checked the returned object is the same one (cancelled is booked), now with status CANCELLED, so it was kept, not deleted. Then I showed find_appointment('A1') still returns it, the all-status listing includes it, the explicit CANCELLED filter returns it, and the SCHEDULED-only listing leaves it out. That last contrast is the proof: present in all-status, absent in SCHEDULED-only means it was retained but filtered, not removed. I also showed a repeat cancel is rejected with the status unchanged, and that the freed slot can be booked again, only possible because the record still exists. This is automated in test_cancel_retained_history and test_ui01_sequence, and shown in ui01_transcript.txt. It's all within one session; the data is lost on exit by design (FR-10 retired), which is expected, not a persistence failure.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? It uses only its arguments, has no hidden state or I/O, and returns a new list without changing the input. It's pure because identical inputs always give the same result. It would stop being pure if it sorted the caller's list in place (appointments.sort(...)), printed, read input, or reached into a global store.


2. Which explicit inputs are needed, and why avoid a global store? It needs the appointment list, the practitioner ID and an optional status. Everything must come through the arguments. A global store would hide an input, make the result depend on state outside the function, and make it hard to test or reuse. The query isn't allowed to decide if a practitioner exists, that's the service's job.


3. How can a new list reuse Appointment objects safely? The new list holds the same Appointment references, not copies. That's fine as long as the query never changes their fields. Sharing objects saves work; the rule is just "don't mutate them."


4. Why use a named key, and what breaks equal-time ties? A named key (appointment_sort_key) is reusable, testable on its own, and passed as key= (not called per item). It returns (date_time, appointment_id), so when two appointments share a time, the appointment ID decides the order (lexicographic).


5. How do default and explicit status filters differ? status=None means all statuses, including CANCELLED and COMPLETED, so history shows up. An explicit AppointmentStatus returns only that status. Both still filter by practitioner.


6. How do empty, unknown practitioner and invalid filter cases differ? Empty: practitioner exists, filter is valid, nothing matches → [], no error. Unknown: ID is valid but not registered → LookupError. Invalid: blank/non-string ID, or a status that isn't an AppointmentStatus → ValueError. A raw string like 'scheduled' is invalid, not "no matches."


7. Which console errors recover, and how is unchanged state checked? Unknown menu choice, blank/unknown ID, duplicate registration, unknown participant, bad date/time, unknown appointment, repeat cancel and invalid status all print a message and return to the menu. State is checked by snapshotting records before and after each rejection and confirming they're the same (including fields, not just count).


8. What is data integrity for registered participants, conflicts and history? Appointments must point at the actual registered patient and practitioner objects (checked with is), not copies. Only a SCHEDULED appointment at the exact same time for the same practitioner conflicts; a different practitioner at that time is allowed. Cancelling changes status but keeps the record, so history stays available in the session.


9. What is Copilot's review role, and who verifies findings? Copilot acts as a reviewer, it points out issues, ranked Critical/Important/Optional, with evidence to check. It doesn't decide what's correct. We verify each finding against the code and tests, then accept, modify or reject it with a reason.


10. How do pure functions and OOP responsibilities work together? The domain objects hold the rules (validation, guarded cancel), the store holds the collections and object identity, services coordinate and validate, the pure query only selects and orders, and the console only does input/output. The query never controls domain rules, it just processes the list the service hands it. Each layer stays separate and testable, which is what NFR-03 asks for.

## H. Review, completion and common handover

Issues and bounded branches: (https://github.com/BN007-CMD/st1-assignment-3/pull/13/changes/1dfd1e484988a5bd265c7ca1d51cd83ae323330f)
PR/diff and another-member human reviewer: PR:https://github.com/BN007-CMD/st1-assignment-3/pull/13
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: 1dfd1e484988a5bd265c7ca1d51cd83ae323330f
Full regression command, working directory, actual count/result and evidence: Working directory: project/ Command: python -m pytest -q Result: 124 passed in 0.12s
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: No critical issues
UG common candidate / PG future branch plan: The Stage 9 SHA above is protected as the common candidate. We will proceeds to Stage 12 preparation

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
