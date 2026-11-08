# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason:
1. "Appointment disappears after cancellation."
- Symptom: Describes what a user sees, and now how it was measured. 'Disappears' could mean the lookup returns None, it is missing from list_appointments(), or it shows the wrong status, it needs turning into a precise observation.
2. "The data-store removal path is probably being called."
- Hypothesis: the use of "Probably" marks it as a guess of the cause. It must be tested against the code. SmartCareDataStore doesn't have a public delete or remove method and only has add_* , find_* , list_* and has_practitioner_conflict. So the hypothesis will only hold if something is writing to _appointments directly or replaces the collection itself and makes it weaker than it sounds.
3. "The failing test shows store.find_appointment('A1') returns None."
- Evidence: It is a specific observation that is repeatable from a run, the exact call and exact value and says what happened and not why. None could come from the record itself being removed, store under another key or looked up with a different ID.
4. "The service layer is badly designed."
- Opinion: No behaviour, requirement or lines are being named, and no test is able to prove or disprove that. It would only be useful if rewritten as a specific smell with a location.
5. "Traceback points to smartcare/services.py line 42."
- Evidence: This is evidence of where the failure first surfaced but not evidence of the cause. The faulty line may be earlier in the call path or data store or domain code. In our run we would inspect the actual line reported and not the line illustrated.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: Scenario, Cancelled history
- Expected: after cancel_appointment('A1'), find_appointment('A1') will return the same object with the status CANCELLED, and list_appointments() still contains the appointment with participants and time unchanged. FR-07 states retain cancelled appointments as current-session history and AC-05.2 and FR06/AC-05.1 mentions the status change.
- Observed: After cancellation, store.find_appointment('A1') returns None.
- Minimal reproduction:Register patient P1 "Dame Example" and practitioner D1 "Lebron Example". Book A1 for P1/D1 at 2026-10-10 09:00; call cancel_appointment('A1'); call data_store.find_appointment('A1').
- Hypothesis: The cancellation path removes from the store or stores the record under a different key instead of only changing status with Appointment.cancel().
- Evidence to inspect: Check if AppointmentService.cancel_appointment does anything besides calling appointment.cancel(), check if there are any writes to _appointments beside the add.appointment, after cancelling I can check list_appointments() and if A1 is absent then it was removed, if it is present but still returning None, the key or lookup may be wrong. Lastly check if Appointment.cancel() does anything besides change _status.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: 
- Deletion test: test a defect. Change the test and not product. The expected behaviour comes from the requirements baseline, and FR-07 requires for the cancelled appointment to stay findable and listed. A test asserting deletion encodes an invented rule. Making a "fix" for the code in order for it to pass would break a requirement and any retained-history tests. Correct the test to assert the retention with the same object, cancelled and in the list and record any changes and reasons in the PR.
- Different-practitioner conflict test: This does not reflect AC-04.2 and is also a test defect. AC-04.2 states that a booking at the same date/time may be done when it is done for a different practitoner and the conflict rule, BR-05 is per practitioner, exact time and SCHEDULED only. Our test-27 and 33 already assert the behaviour and the defected test should be rewritten to expect that both bookings are stored.
- From both cases, a failing test can be used as a signal to check the test against the requirement before playing with any product code.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:
| Smell | Smell Refactoring |
| --- | --- |
| Long method | Extract small, named private steps so the public method reads as a sequence |
| Duplicated magic status strings | Using exisiting AppointmentStatus enum and compare with is, as the data store is alreadying doing that |
| Direct collection manipulation in the service | Going through the SmartCareDataStore boundary, find_appointment, add_appointmnet, list_appointments, has_practitioner_conflict. No new layer needed for the repository |
| Printing inside the service | Return values or raise ValueError or LookupError. User messages will belong the console in stage 9. |
| Duplicated Validation | Relying on the domain constructors and required_text that are already trimming and rejecting blank/non-text values. |
| Four nested conditionals | Guard clauses that raise early and flatten the nesting without changing the order of which checks happen |

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason:
- Failure used: test_cancelled_appointment_is_retained_as_history.
- Exception/assertion: LookupError: Appointment not found, raised while evaluating assert clinic.appointments.find_appointment('A1') is booked
- Expected / observed values: expected find_appointment('A1') to return the booked A1 object (status CANCELLED); observed: no object returned, LookupError raised instead.
- Test line: tests\test_services.py:201.
- Application call path: test line 201 → AppointmentService.find_appointment('A1') (services.py) → self.data_store.find_appointment('A1') returns None → raise LookupError at services.py:138. The traceback stops in services.py; it does not show inside SmartCareDataStore.find_appointment.
- Supporting requirement: FR-07/AC-05.2 (cancelled appointment retained and still found), with FR-08 lookup.
- Ranked causes and discriminating checks:
| Rank | Possible causes | checks |
| --- | --- | --- |
| 1 | the record is found while SCHEDULED, COMPLETED is still found, and list-based tests pass | after cancelling, booked in data_store.list_appointments() is True while data_store.find_appointment('A1') is None. |
| 2 | the store has no delete operation, and test_cancel_changes_only_the_requested_appointment still passes its list check | the same list-membership check. Absent from the list would support this cause. |
| 3 | lookup of the same 'A1' works before cancellation | call data_store.find_appointment('A1') before and after cancelling with the identical string. Success before and failure after rules out an ID mismatch. |
- Why a traceback alone does not establish the cause: it shows where an exception was raised or an assertion failed, and the call stack at that moment. It does not show where the bad state was created. A wrong value can be produced earlier (in another method, an earlier call or the test arrangement) and only detected later. The traceback can also point into a test that is itself wrong. The cause is established only when a check confirms one hypothesis and rules out the others, and the minimal fix makes the failing test pass without breaking others.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason:
The first visible line is usually where the problem was detected, not where it was caused. Editing there tends to hide the symptom (a guard, a special case, a swallowed exception) while the root cause stays. It can also "fix" product code to match a test that is itself wrong. Without a recorded expectation, reproduction and hypothesis, there is no way to show the change was correct, and unrelated edits can break other requirements. Reproduce first, state the expected behaviour from the requirement, form and test a hypothesis, then make the smallest justified change and verify with the full suite.

Classification responses (1–5, each with reason): see A.1
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: See A.2.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: See A.5

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: Ready 11068b432586eb0c6ad9b90b357780da5aeb32f1
- Baseline test command / working directory / observed result / evidence: python -m pytest from project/. Stage 7 records 86 passed on 11068b432586eb0c6ad9b90b357780da5aeb32f1.
- Clean preparation SHA if a record-only commit followed Stage 7: b05c79aaaba0babb25dea1d8f09a19484f952d33.
- Branch and preparer / how teammates obtained this branch: debug/stage08; Quang Le obtained this branch from tutor Pranav Gupta.
- Downloaded tool version, source SHA256 and --check outcome: Version 1.1; SHA256 b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375; check passed.
- --apply and --verify output summaries / artefact references: Both outputs passed and verified exactly two expected failures.
- Bounded diff inspected and recovery location (not committed): Changes inspected and recovery data in .stage08_faults not committed.
- Prepared faulty-state commit SHA: dec5a4477ce031555ac462759f100b577384d48e
- Preparation or recovery issues and resolution, if any: Preperation was done directly in our GitHub repository by our tutor.
- Initial prepared full-suite command / result / key failures: python -m pytest -q from project/ on debug/stage08, 7 failed from 79 passed in 0.18s

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: the conflict rule behaves the wrong way round for practitioners. Booking the same practitioner (D1) at the same time twice is accepted (no ValueError). Booking a different practitioner (D2) at a time D1 already holds is rejected with ValueError: Practitioner already has a SCHEDULED appointment at this time. In the same run, D1 one minute later (TEST-28) and rebooking a cancelled slot still pass.
- Expected behaviour and requirement: FR-05/AC-04.1: a booking is rejected with ValueError when the same practitioner already has a SCHEDULED appointment at the same date/time, and stored state is unchanged. AC-04.2: a booking at the same date/time for a different practitioner is allowed. No patient-conflict or duration-overlap rule exists.
- Minimal synthetic reproduction steps: fresh SmartCareDataStore; register P1 "Dame Example", P2 "Giannis Example", D1 "Lebron Example" (General practice), D2 "Chris Example" (Physiotherapy). (a) Book A1 = P1/D1 at 2026-10-10 09:00, then A2 = P2/D1 at 09:00 → expected ValueError and list_appointments() == [A1]; observed: A2 is stored. (b) In a fresh store, book A1 = P1/D1 at 09:00, then A2 = P2/D2 at 09:00 → expected both stored; observed: ValueError.
- Meaningful failing test path/name and exact relevant failure: project/tests/test_services.py::test_same_practitioner_same_time_conflicts (test-26), Failed: DID NOT RAISE class 'ValueError'; and ::test_different_practitioner_same_time_is_allowed (test-27), ValueError: Practitioner already has a SCHEDULED appointment at this time, raised from services.py after data_store.has_practitioner_conflict(...) returned True. Also detected by test-32, test-33 and test_starter.py::test_conflict_rule_and_different_practitioner.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: after a SCHEDULED appointment is cancelled, it can no longer be found. AppointmentService.find_appointment('A1') raises LookupError: Appointment not found, because data_store.find_appointment('A1') returned None. A second cancellation therefore raises LookupError instead of the expected ValueError. In the same run, the first cancellation succeeds and returns the booked object with status CANCELLED. Tests that check list_appointments() after cancelling still pass, and a COMPLETED appointment is still found.
- Expected behaviour and requirement: FR-06/BR-07: cancellation is a guarded SCHEDULED → CANCELLED transition. FR-07/aC-05.2: the same object stays in current-session history and is still found and listed. FR-08 supports lookup. AC-05.3: a repeated cancellation raises ValueError and leaves the status CANCELLED. Store lookup returns None only for a valid missing ID; the service maps that to LookupError.
- Minimal synthetic reproduction steps: fresh SmartCareDataStore; register P1 "Dame Example" and D1 "Lebron Example". Book A1 = P1/D1 at 2026-10-11 09:00; check data_store.find_appointment('A1') is booked (expected and observed: True). Call cancel_appointment('A1'). Then check: booked.status (expected CANCELLED); booked in data_store.list_appointments() (expected True); data_store.find_appointment('A1') (expected booked, observed None); appointments.find_appointment('A1') (expected booked, observed LookupError); a second cancel_appointment('A1') (expected ValueError, observed LookupError).
- Meaningful failing test path/name and exact relevant failure: project/tests/test_services.py::test_cancelled_appointment_is_retained_as_history, line 201 (assert clinic.appointments.find_appointment('A1') is booked) → LookupError: Appointment not found at services.py:138. Also ::test_repeated_cancellation_is_rejected_without_change, line 225 → LookupError via services.py:148 (cancel_appointment → find_appointment).
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: in SmartCareDataStore.has_practitioner_conflict, the practitioner condition compares appointment.practitioner.practitioner_id != practitioner_id where AC-04.1 needs ==. The method would then report a conflict only for other practitioners' SCHEDULED appointments at that time, and never for the same practitioner. That explains every F8-01 observation: same practitioner at the same time accepted (TEST-26, TEST-32, starter test); different practitioner at the same time rejected (TEST-27, TEST-33); D1 one minute later still accepted (TEST-28), because the time condition is unaffected. Secondary observation, not claimed as the cause: status is compared with the string "scheduled" rather than AppointmentStatus.SCHEDULED. Because TEST-27 does raise, that string comparison must currently match some SCHEDULED appointments.
Evidence intended to inspect / competing explanation / discriminating check: lines 108–113 against the AC-04.1 wording; git diff main -- project/smartcare/data_store.py to compare with the Stage 7 version; the AppointmentStatus values in domain.py. Competing explanation: AppointmentService.book_appointment passes the wrong practitioner ID to the store.
Discriminating check: the traceback for TEST-27 already shows practitioner_id = 'D2' was passed for A2, and git diff --stat shows services.py unchanged. Confirm by calling the store directly in a fresh store: book A1 for D1 at 09:00, then data_store.has_practitioner_conflict('D1', NINE_AM) (expected True) and ('D2', NINE_AM) (expected False). If the store alone gives the inverted answers, the store condition is the cause, not the service.
Member and saved sequence/time or commit showing this preceded consultation: [complete]

### F8-02 human entry
Likely cause and why plausible: SmartCareDataStore.find_appointment has been rewritten as a loop with an extra filter, appointment.status.value != "cancelled". A cancelled appointment would then be skipped and None returned even though it is still stored. The contract says store lookup returns None only for a valid missing ID, and FR-07/AC-05.2 require the cancelled appointment to remain findable. find_patient and find_practitioner have no such filter. That explains: found while SCHEDULED (so the first cancel works); not found after CANCELLED (LookupError in the service); repeated cancel giving LookupError instead of ValueError, because lookup fails before Appointment.cancel() can reject it; a COMPLETED appointment still found; list-based tests still passing. Secondary observations: the method no longer uses required_text and compares statuses with a string rather than the enum.
Evidence intended to inspect / competing explanation / discriminating check: lines 89–96 compared with the other find_* methods and with git diff main -- project/smartcare/data_store.py; Appointment.cancel() in domain.py; AppointmentStatus.CANCELLED.value.
Competing explanation: cancellation removes or re-keys the record, so it is genuinely missing.
Discriminating check: after cancelling A1, check booked in data_store.list_appointments() and booked.status. If the object is still listed with status CANCELLED while data_store.find_appointment('A1') is None, the record was retained and the lookup filter is the cause. If it is absent from the list, removal is the cause. Also confirm that non-text and blank IDs (None, 101, '', '   ') still raise ValueError from the rewritten method.
Member and saved sequence/time or commit showing this preceded consultation: [complete]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
