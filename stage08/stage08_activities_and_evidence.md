# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Online Group 4, Tuesday 17:30 tutorial
Members and UG/PG cohorts: Novica Baloski (@BN007-CMD, UG); Emilio Rojas-Terry (@ucemilio, UG); Quang Le, (@quangle330, UG); Brendan Potter (@BrendoAC11, UG)
Record owner / contribution links for each member: Quang Le, stage 8 lead, for contribution links, see I.

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
- Minimal synthetic reproduction steps: fresh SmartCareDataStore; register P1 "Dame Example", P2 "Giannis Example", D1 "Lebron Example" (General), D2 "Chris Example" (Physio). (a) Book A1 = P1/D1 at 2026-10-10 09:00, then A2 = P2/D1 at 09:00 → expected ValueError and list_appointments() == [A1]; observed: A2 is stored. (b) In a fresh store, book A1 = P1/D1 at 09:00, then A2 = P2/D2 at 09:00 → expected both stored; observed: ValueError.
- Meaningful failing test path/name and exact relevant failure: project/tests/test_services.py::test_same_practitioner_same_time_conflicts (test-26), Failed: DID NOT RAISE class 'ValueError'; and ::test_different_practitioner_same_time_is_allowed (test-27), ValueError: Practitioner already has a SCHEDULED appointment at this time, raised from services.py after data_store.has_practitioner_conflict(...) returned True. Also detected by test-32, test-33 and test_starter.py::test_conflict_rule_and_different_practitioner. Focused regression test: project/tests/test_regressions.py::test_f8_01_conflict_is_per_practitioner_at_exact_time. Focused regression test: project/tests/test_regressions.py::test_f8_01_conflict_is_per_practitioner_at_exact_time. Before repair, at 02cffab: tests\test_regressions.py:47: Failed: DID NOT RAISE class 'ValueError', so the same-practitioner booking was accepted.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.has_practitioner_conflict (project/smartcare/data_store.py, line 110) tests appointment.practitioner.practitioner_id != practitioner_id where AC-04.1 requires ==, so a conflict is reported only for other practitioners. Runtime check (fresh store, A1 booked for D1 at 2026-10-01 09:00, store called directly): has_practitioner_conflict('D1', 09:00) → False (expected True); has_practitioner_conflict('D2', 09:00) → True (expected False). The store alone gives the inverted answers, and the TEST-27 traceback shows the service passed practitioner_id = 'D2', which rules out the competing explanation that the service passes the wrong ID.
- Smallest justified fix / diff / why other behaviour is preserved: in has_practitioner_conflict, change appointment.practitioner.practitioner_id != practitioner_id to == practitioner_id; one operator on one line, nothing else. The faulty decision matched appointments belonging to other practitioners; == restricts the check to the requested practitioner, as AC-04.1 states. The other three conditions are untouched (the excluded appointment ID, the exact date_time match and SCHEDULED-only status), so one-minute-later bookings (TEST-28), rebooking a cancelled slot and AC-04.2 different-practitioner bookings behave as before. No service or test code changed. Confirmed by the record owner with git show 2ef8a3a --stat: only project/smartcare/data_store.py changed.
- Repair SHA / focused verification result: 2ef8a3a092d8784bdffdc2f445d4d15c499103ba; python -m pytest tests/test_regressions.py::test_f8_01_conflict_is_per_practitioner_at_exact_time -q from project/ → 1 passed in 0.01s.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: after a SCHEDULED appointment is cancelled, it can no longer be found. AppointmentService.find_appointment('A1') raises LookupError: Appointment not found, because data_store.find_appointment('A1') returned None. A second cancellation therefore raises LookupError instead of the expected ValueError. In the same run, the first cancellation succeeds and returns the booked object with status CANCELLED. Tests that check list_appointments() after cancelling still pass, and a COMPLETED appointment is still found.
- Expected behaviour and requirement: FR-06/BR-07: cancellation is a guarded SCHEDULED → CANCELLED transition. FR-07/aC-05.2: the same object stays in current-session history and is still found and listed. FR-08 supports lookup. AC-05.3: a repeated cancellation raises ValueError and leaves the status CANCELLED. Store lookup returns None only for a valid missing ID; the service maps that to LookupError.
- Minimal synthetic reproduction steps: fresh SmartCareDataStore; register P1 "Dame Example" and D1 "Lebron Example". Book A1 = P1/D1 at 2026-10-11 09:00; check data_store.find_appointment('A1') is booked (expected and observed: True). Call cancel_appointment('A1'). Then check: booked.status (expected CANCELLED); booked in data_store.list_appointments() (expected True); data_store.find_appointment('A1') (expected booked, observed None); appointments.find_appointment('A1') (expected booked, observed LookupError); a second cancel_appointment('A1') (expected ValueError, observed LookupError).
- Meaningful failing test path/name and exact relevant failure: project/tests/test_services.py::test_cancelled_appointment_is_retained_as_history, line 201 (assert clinic.appointments.find_appointment('A1') is booked) → LookupError: Appointment not found at services.py:138. Also ::test_repeated_cancellation_is_rejected_without_change, line 225 → LookupError via services.py:148 (cancel_appointment → find_appointment). Focused regression test: project/tests/test_regressions.py::test_f8_02_cancelled_appointment_is_still_found. Before repair, at 02cffab: the status and list assertions passed, then tests\test_regressions.py:74: AssertionError: assert None is smartcare.domain.Appointment from data_store.find_appointment('A1').
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.find_appointment (project/smartcare/data_store.py, lines 92–95) skips any appointment whose status.value is "cancelled", so a stored, cancelled appointment returns None. That breaks the store contract (None only for a valid missing ID) and FR-07/AC-05.2. Runtime check after booking and cancelling A1 in a fresh store: status: AppointmentStatus.CANCELLED, still listed: True, store find: None. The record is retained and the transition happened, so the competing explanation that cancellation removes or re-keys the record is ruled out, and only lookup fails. The regression test shows the same order: the status and list assertions pass, and the store lookup fails.
- Smallest justified fix / diff / why other behaviour is preserved: in find_appointment, delete the condition and appointment.status.value != "cancelled", so the match is if appointment.appointment_id == appointment_id.strip():; nothing else. The faulty decision treated a CANCELLED status as "not found", contradicting the store contract (None only for a valid missing ID) and FR-07/AC-05.2. Removing only that filter returns every stored appointment by ID regardless of status. Unchanged: blank, whitespace-only and non-text IDs still raise ValueError from the existing guard; a missing ID still returns None; IDs are still trimmed and case-sensitive; the service still maps None to LookupError; and repeated cancellation now reaches Appointment.cancel(), which raises ValueError and leaves the status CANCELLED (AC-05.3). The remaining string comparison and hand-written guard are left for H rather than changed during repair. Confirmed by the record owner with git show afb89ad --stat: only project/smartcare/data_store.py changed.
- Repair SHA / focused verification result: afb89ad9e9287c7f0f836fedf8b93640a527ac1b; python -m pytest tests/test_regressions.py::test_f8_02_cancelled_appointment_is_still_found -q from project/ → 1 passed in 0.01s.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: in SmartCareDataStore.has_practitioner_conflict, the practitioner condition compares appointment.practitioner.practitioner_id != practitioner_id where AC-04.1 needs ==. The method would then report a conflict only for other practitioners' SCHEDULED appointments at that time, and never for the same practitioner. That explains every F8-01 observation: same practitioner at the same time accepted (TEST-26, TEST-32, starter test); different practitioner at the same time rejected (TEST-27, TEST-33); D1 one minute later still accepted (TEST-28), because the time condition is unaffected. Secondary observation, not claimed as the cause: status is compared with the string "scheduled" rather than AppointmentStatus.SCHEDULED. Because TEST-27 does raise, that string comparison must currently match some SCHEDULED appointments.
Evidence intended to inspect / competing explanation / discriminating check: lines 108–113 against the AC-04.1 wording; git diff main -- project/smartcare/data_store.py to compare with the Stage 7 version; the AppointmentStatus values in domain.py. Competing explanation: AppointmentService.book_appointment passes the wrong practitioner ID to the store.
Discriminating check: the traceback for TEST-27 already shows practitioner_id = 'D2' was passed for A2, and git diff --stat shows services.py unchanged. Confirm by calling the store directly in a fresh store: book A1 for D1 at 09:00, then data_store.has_practitioner_conflict('D1', NINE_AM) (expected True) and ('D2', NINE_AM) (expected False). If the store alone gives the inverted answers, the store condition is the cause, not the service.
Member and saved sequence/time or commit showing this preceded consultation: Quang Le - Commit SHA fc1dac86ab195fa15c26666bf334e95d33644657

### F8-02 human entry
Likely cause and why plausible: SmartCareDataStore.find_appointment has been rewritten as a loop with an extra filter, appointment.status.value != "cancelled". A cancelled appointment would then be skipped and None returned even though it is still stored. The contract says store lookup returns None only for a valid missing ID, and FR-07/AC-05.2 require the cancelled appointment to remain findable. find_patient and find_practitioner have no such filter. That explains: found while SCHEDULED (so the first cancel works); not found after CANCELLED (LookupError in the service); repeated cancel giving LookupError instead of ValueError, because lookup fails before Appointment.cancel() can reject it; a COMPLETED appointment still found; list-based tests still passing. Secondary observations: the method no longer uses required_text and compares statuses with a string rather than the enum.
Evidence intended to inspect / competing explanation / discriminating check: lines 89–96 compared with the other find_* methods and with git diff main -- project/smartcare/data_store.py; Appointment.cancel() in domain.py; AppointmentStatus.CANCELLED.value.
Competing explanation: cancellation removes or re-keys the record, so it is genuinely missing.
Discriminating check: after cancelling A1, check booked in data_store.list_appointments() and booked.status. If the object is still listed with status CANCELLED while data_store.find_appointment('A1') is None, the record was retained and the lookup filter is the cause. If it is absent from the list, removal is the cause. Also confirm that non-text and blank IDs (None, 101, '', '   ') still raise ValueError from the rewritten method.
Member and saved sequence/time or commit showing this preceded consultation: Quang Le - Commit SHA fc1dac86ab195fa15c26666bf334e95d33644657

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: Quang Le. Handout prompt structure, filled with the F8-01 observed and expected behaviour, reproduction, failing test, hypothesis from E and the has_practitioner_conflict https://github.com/BN007-CMD/st1-assignment-3/pull/7#pullrequestreview-5816888074
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Inverted practitioner comparison (!= instead of ==) in has_practitioner_conflict. Evidence check Copilot proposed: inspect the comparison against the same- and different-practitioner cases. Observed evidence: line 110 reads != practitioner_id; direct store check gives has_practitioner_conflict('D1', 09:00) → False and ('D2', 09:00) → True with only A1 (D1) stored; the regression test fails with DID NOT RAISE. Correct. Accept: it matches the code, the runtime results and all five failing conflict tests, and it is the same as our E hypothesis.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: The booking service passes an unexpected practitioner ID. Evidence check: compare the ID passed to has_practitioner_conflict in services.py with the stored practitioner ID. Observed evidence: the TEST-27 traceback shows practitioner_id = 'D2' passed for a D2 booking; git diff --stat shows services.py unchanged by preparation; the direct store calls bypass the service and still give inverted results. Wrong as a cause. Reject: the evidence contradicts it, which Copilot itself acknowledged ("much weaker fit"). The check it proposed was useful and matches our E competing explanation.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: A1's stored time or status differs from what the reproduction assumes. Evidence check: inspect A1's date_time and status before calling the predicate. Observed evidence: A1 was booked at 2026-10-01 09:00 and is SCHEDULED (TEST-07 and TEST-21 pass); the ('D2', 09:00) → True result is only possible if the time and status conditions matched A1. Wrong as a cause. Reject: as Copilot noted, the D2 result already rules it out. Its reasoning about the time and status checks is correct. Final human conclusion and comparison with initial hypothesis: the root cause is the inverted practitioner comparison on line 110, as hypothesised in E. Copilot's top-ranked cause agreed with our hypothesis and added no new cause; its two alternatives were ones we had already ruled out with the traceback, the unchanged services.py and the direct store checks. The decision rests on our own runtime evidence, not on Copilot's ranking. Repair: change != to == on that line only (see C).

### F8-02 Copilot review
Actual prompt / output reference and member: Quang Le. Handout prompt structure, filled with the F8-02 observed and expected behaviour, reproduction, failing test, hypothesis from E and the find_appointment https://github.com/BN007-CMD/st1-assignment-3/pull/7#pullrequestreview-5816897930
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Store lookup explicitly excludes cancelled records (Copilot's leading hypothesis). Evidence check: inspect the status condition in data_store.py against the stored object's ID and status. Observed evidence: the condition and appointment.status.value != "cancelled" is on line 94; Copilot cited line 89, which is the def line, so its reference was slightly imprecise. After cancelling: status: AppointmentStatus.CANCELLED, still listed: True, store find: None; the regression test fails at the store lookup assertion after its status and list assertions pass. Correct. Accept: it matches the code and the runtime results, and it is our E hypothesis.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: The service turns the store's None into LookupError, so a second cancel never reaches the domain guard. Evidence check: the call sequence cancel_appointment → find_appointment and the guard in domain.py (Appointment.cancel(), around line 129). Observed evidence: the tracebacks show exactly that sequence (services.py:148 → services.py:138 raising LookupError), and services.py was unchanged by preparation. Partly correct. Modify: it accurately explains why the symptom appears in the service and why AC-05.3 gives LookupError instead of ValueError. But it is a downstream effect of the store returning None, not a cause. The service mapping is the required contract (store None → service LookupError), so changing the service would hide the defect rather than repair it. Kept as an explanation of the symptom chain; rejected as a repair location.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: The lookup receives a different ID or a different store from the one holding A1. Evidence check: compare the lookup argument with the stored ID; confirm the same store instance is used. Observed evidence: the reproduction and the regression fixture use one SmartCareDataStore instance throughout; find_appointment('A1') with the identical string succeeds before cancellation (the first cancel works) and returns None only after; A1 is still in that store's list. Wrong as a cause. Reject: the before/after lookup with the same ID and the same store rules it out, as Copilot itself conceded ("much weaker fit"). Final human conclusion and comparison with initial hypothesis: the root cause is the status filter in SmartCareDataStore.find_appointment (line 94), which treats a retained, cancelled appointment as missing, as hypothesised in E. Copilot's leading cause agreed. Its second suggestion described a real mechanism, but one downstream of the cause. Copilot did not raise our E competing explanation, that cancellation removes the record; the still listed: True result ruled that out. Repair: delete that status condition only (see D).

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | 02cffab4e2b8d07b911e7f7169a69db2805567ca (prepared faults + regression tests) | python -m pytest tests/test_regressions.py -q from project/ | test_f8_01_conflict_is_per_practitioner_at_exact_time failed: DID NOT RAISE <class 'ValueError'> at line 47 (2 failed in 0.05s for the file) |
| F8-01 after repair | 2ef8a3a092d8784bdffdc2f445d4d15c499103ba | python -m pytest tests/test_regressions.py::test_f8_01_conflict_is_per_practitioner_at_exact_time -q from project/ | 1 passed in 0.01s |
| F8-02 before repair | 02cffab4e2b8d07b911e7f7169a69db2805567ca | same run as F8-01 before repair | test_f8_02_cancelled_appointment_is_still_found failed: assert None is <Appointment> at line 74; status and list assertions passed first |
| F8-02 after repair | afb89ad9e9287c7f0f836fedf8b93640a527ac1b | python -m pytest tests/test_regressions.py::test_f8_02_cancelled_appointment_is_still_found -q from project/ | 1 passed in 0.01s |
| Full suite after both repairs, before refactor | afb89ad9e9287c7f0f836fedf8b93640a527ac1b | python -m pytest -q from project/ | 88 passed in 0.06s (86 retained + 2 regression tests; all 7 plus the 2 regression test failures now pass) |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour:
- F8-01: pytest.raises(ValueError) on the second D1 booking at 09:00 fails if a same-practitioner conflict is accepted (this is what failed before repair). list_appointments() == [first] and find_appointment('A2') is None fail if a rejected booking is stored anyway. The D2 booking at the same time, followed by list_appointments() == [first, other], covers the other half of the inverted defect (AC-04.2): it would fail if the check over-matched other practitioners. Before repair this part did not run, because the test stopped at the pytest.raises on line 47. The AC-04.2 failure before repair is shown instead by TEST-27 and TEST-33 (see B). After repair, this test protects both directions. The retained TEST-26/27/28/32/33 and starter tests protect the surrounding conflict behaviour, including the exact-time boundary.
- F8-02: booked.status is CANCELLED and list_appointments() == [booked] show the transition and retention. data_store.find_appointment('A1') is booked (the assertion that failed before repair) and appointments.find_appointment('A1') is booked check store and service lookup separately, by identity, so None and LookupError are not confused and a replacement copy would fail. The repeated-cancel pytest.raises(ValueError), with status and list unchanged afterwards, protects AC-05.3. The retained Stage 6 cancellation tests protect unknown/invalid ID handling, COMPLETED rejection and rebooking.
Unrelated failures investigated / resolution: Not applicable. All 7 failures in the initial prepared run are conflict tests (F8-01) or cancelled-lookup tests (F8-02); see B.

## H. Refactoring decision and before/after verification

Smell and exact location: magic status string in SmartCareDataStore.has_practitioner_conflict (project/smartcare/data_store.py, the last condition of the loop): appointment.status.value == "scheduled". It compares the enum's raw string value instead of the AppointmentStatus member that is already imported and used everywhere else. It duplicates knowledge of the enum's internal value, a typo would silently disable conflict detection, and it is inconsistent with the domain and tests, which compare members with is. Also seen but deliberately not changed: find_appointment re-implements ID validation and scans a list instead of self._appointments.get(required_text(...)) like the other find_* methods. Changing it would alter the ValueError message text and enlarge the diff, so it is out of scope for one small refactor.

Small proposed structural change / why justified: replace appointment.status.value == "scheduled" with appointment.status is AppointmentStatus.SCHEDULED; one condition on one line, no other edit. Justified because it removes a magic string using the existing enum (the A.4 example), with no new abstraction or dependency. It is behaviour-preserving because the conflict tests (TEST-26, TEST-32) pass at afb89ad, which is only possible if "scheduled" currently equals AppointmentStatus.SCHEDULED.value. Each appointment's status is always an AppointmentStatus member (TEST-15), so both forms select exactly the same appointments.

External behaviour to preserve / relevant tests: a conflict is reported only for the same practitioner, at the exact same date_time, with a SCHEDULED appointment that is not the excluded ID. CANCELLED and COMPLETED appointments never block a booking; a rejected booking raises ValueError and leaves the store unchanged; no records are mutated. Protected by test_regressions.py::test_f8_01_conflict_is_per_practitioner_at_exact_time, TEST-26, 27, 28, 32, 33, test_cancelled_slot_can_be_booked_again (CANCELLED does not block), test_starter.py::test_conflict_rule_and_different_practitioner, and the full suite (88 passed at afb89ad).
Before result: see G, full passing suite.

Actual change / diff / separate refactor SHA: 3a1b4265e38eac3512e1cbfdbf5d4a7c11523f2f, a separate commit after both repairs. One line in project/smartcare/data_store.py (has_practitioner_conflict)
Focused and full after-refactor commands / working directory / results / evidence: from project/: python -m pytest tests/test_regressions.py tests/test_services.py tests/test_starter.py -q → 61 passed in 0.05s; python -m pytest -q → 88 passed in 0.06s, the same as before the refactor (88 passed at afb89ad, see G).

Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: Accepted. The magic string is replaced by the existing enum member, matching how the domain and tests compare statuses and removing the risk that a mistyped string silently disables conflict detection. Behaviour is preserved: the same 88 tests pass before and after, with no test changed, including the F8-01 regression test, the AC-04.1/04.2 conflict tests, the exact-time boundary and the cancelled-slot rebooking test. That shows the same appointments still count as conflicts. Return values, exception types and non-mutation are unchanged, because only the comparison expression changed.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners (owner for all three: Quang (Jay), @quangle330):

- #8: practitioner conflict check matches the wrong practitioner (F8-01, FR-05; AC-04.1/04.2). Scope: has_practitioner_conflict plus a regression test.
- #9: cancelled appointments cannot be found after cancellation (F8-02, FR-07; AC-05.2/05.3). Scope: find_appointment plus a regression test.
- #10: replace the magic status string in the conflict check with the AppointmentStatus enum (refactor only; one condition in data_store.py). Branch / prepared, repair and refactor checkpoints: see B (prepared), C and D (repairs), H (refactor). PR link and another member's reviewer identity: https://github.com/BN007-CMD/st1-assignment-3/pull/11#issue-6268736524. Reviewers: Emilio (F8-01, #8), Brendan (F8-02, #9), Novica (refactor and record, #10). Key human feedback, difference from Copilot findings and response/outcome:
- Novica (#10): [review;](https://github.com/BN007-CMD/st1-assignment-3/pull/11#pullrequestreview-5817138689) confirmed 3a1b426 is a one-line structural change, edits no test and is a separate commit after both repairs. She checked B and G against the history (b05c79a 86 passed → dec5a44 7 failed → 02cffab 9 failed → afb89ad 88 passed); her run gave 88 passed in 0.13s on 3a1b426. She requested changes: section H was still placeholders in the repository, and commit 90b26fd (before the refactor) did not contain the H plan its message implied. Response: H completed in 27cd375, and a process note added to H recording that the plan was not committed before the refactor. She rechecked (88 passed in 0.13s on 27cd375) and approved. Difference from Copilot: Copilot was asked only about causes. It never checked commit order, the consistency between the record and the history, or whether a commit message matched its content. Only the human review found the process gap.
- Emilio (#8): [review](https://github.com/BN007-CMD/st1-assignment-3/pull/11#pullrequestreview-5817136201). Branch run 88 passed in 0.12s on 3a1b426; before-repair check at 02cffab gave 2 failed in 0.09s, with the F8-01 test failing at line 47 (DID NOT RAISE ValueError) as recorded. He confirmed the fix is the one-line != → == change, the regression test checks both directions with unchanged state, and the F8-01 Copilot decisions match the evidence. He requested record-only changes: (1–2) C fix-field wording and a duplicated sentence, which were not present in the current record (likely an older pushed copy) and which he was asked to recheck; (3) reconcile 7 vs 9 failures in G, fixed; (4) say the AC-04.2 half of the regression test did not run before repair and that TEST-27/33 show that failure, fixed; minor: align the specialty wording in C with the fixture, fixed. Difference from Copilot: he independently reran the before-repair state and checked the record's internal consistency and the test's execution path; Copilot did neither. His approval was given in this same review, submitted as a comment rather than through GitHub's formal Approve option.
- Brendan (#9): [post-merge review](https://github.com/BN007-CMD/st1-assignment-3/pull/11#issuecomment-6720219065) (see the process deviation under approval/merge evidence). He confirmed the fix removes only the status.value != "cancelled" condition; the regression test checks store and service lookup separately and a repeated cancellation raises ValueError; and blank or non-text IDs still raise ValueError through the existing isinstance/strip() guard in find_appointment. He agreed with marking Copilot's "service turns None into LookupError" point as Modify rather than Accept. His run: 88 passed in 0.13s on 27cd375 (the PR branch head). No changes requested; he stated he was happy to approve. Difference from Copilot: he checked that invalid-ID validation survived the repair, which none of Copilot's F8-02 suggestions addressed. His before-repair check at 02cffab gave 2 failed in 0.06s, with the F8-02 test failing on AssertionError: assert None is <smartcare.domain.Appointment ...> as recorded. Actual review approval / merge evidence:
- Quang, Stage 8 lead: safe preparation of debug/stage08 with the tutor; reproduced both defects and recorded observed and expected behaviour (B, C, D); wrote and ran the direct store checks; added project/tests/test_regressions.py (02cffab); recorded hypotheses before Copilot (E); ran and evaluated both Copilot consultations (F); made the two minimal repairs (2ef8a3a, afb89ad) and the refactor (3a1b426); opened issues #8–#10 and PR #11; wrote the reviewer instructions; responded to review feedback (27cd375 and later record commits); merged and retested (88 passed on b3a3b58); maintained this record.
- Novica: reviewed the refactor and the record (#10); checked commit order and the B/G SHAs against the history; found that the H plan had not been committed before the refactor, which led to 27cd375 and the H process note; rechecked and approved; after-merge run 88 passed on b3a3b58. Artefact: [review.](https://github.com/BN007-CMD/st1-assignment-3/pull/11#pullrequestreview-5817138689)
- Emilio: reviewed the F8-01 fix and regression test (#8); independently reran the before-repair state at 02cffab (2 failed); requested record corrections in C and G (7 vs 9 reconciliation, the AC-04.2 execution path, specialty wording); after-merge run 88 passed on b3a3b58. Artefact: [review.](https://github.com/BN007-CMD/st1-assignment-3/pull/11#pullrequestreview-5817136201)
- Brendan: post-merge review of the F8-02 fix and regression test (#9), confirming the minimal diff, separate store and service lookup checks, retained invalid-ID validation and the Copilot Modify decision; independently reran the before-repair state at 02cffab (2 failed, F8-02 failing at the store lookup); branch run 88 passed on 27cd375; after-merge run 88 passed on b3a3b58. Artefact: [review.](https://github.com/BN007-CMD/st1-assignment-3/pull/11#issuecomment-6720219065)

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? 
- F8-02 suggestion 2: "the service turns the store's None into LookupError". It looked convincing because the traceback ends in services.py:138, where the LookupError is actually raised, so it would be easy to "fix" the service there. But no evidence showed the service behaving incorrectly. services.py was unchanged by preparation, and mapping store None to service LookupError is the required contract. Our direct store call returning None for a still-listed appointment showed the service was only reporting a miss that happened earlier in the store. The suggestion described where the failure was observed, not where it was caused. For F8-01, Copilot's alternatives (wrong ID from the service; mismatched time or status) were less convincing and were already ruled out by the traceback and the direct store results.
2. What evidence changed your group's view?
- Our hypotheses did not change, but specific evidence moved them from plausible to supported. For F8-01, calling has_practitioner_conflict directly on the store (D1 → False, D2 → True) removed the service from suspicion. For F8-02, still listed: True with store find: None ruled out the "cancellation removes the record" explanation we had listed as a competitor, and ruled out Copilot's ID/store-mismatch alternative. The regression test failing after its status and list assertions passed confirmed it. That evidence, rather than Copilot agreeing with us, is what justified editing only data_store.py.
3. How did regression tests protect the refactoring?
- We refactored only after both repairs gave a fully passing suite (88 passed at afb89ad), so any change in result would point to the refactor. The same 88 tests then passed at 3a1b426 with no test edited. The tests that would have caught a behaviour change were the F8-01 regression test (same practitioner rejected and store unchanged; different practitioner allowed), TEST-26/32 (a conflict is detected, which would fail if the enum comparison never matched), TEST-27/33 (other practitioners not blocked), TEST-28 (exact-time boundary) and test_cancelled_slot_can_be_booked_again (CANCELLED does not count as a conflict). Because these assert specific outcomes and unchanged state rather than "not None", a passing run is real evidence the refactor kept behaviour. Keeping the change to one line made any failure easy to trace.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Reproduce the failure reliably and in the smallest form. Record the observed behaviour and the expected behaviour, justified by a requirement. Check whether the test itself is correct. Form a hypothesis and decide what evidence would confirm or rule it out. Only then make the smallest change that addresses the supported cause.

2. Where should expected behaviour come from during debugging?

Response: From the agreed requirements and contracts. For us that is the SmartCare A3 Requirements Baseline revision 2 (FRs, ACs, BRs and the ID, time and status contracts). It should not come from what the current code does, what a test happens to assert, or what Copilot suggests.

3. What is a debugging hypothesis?

Response: A specific, testable explanation of what is causing an observed failure, stated so that a particular check could confirm or refute it. For example: "cancel removes A1 from the store", which a list_appointments() check after cancelling would confirm or rule out.

4. What is a regression test and why is it retained?

Response: A test that captures behaviour that must keep working, often added when a defect is fixed so it fails on the faulty code and passes after the repair. It stays in the suite so the defect cannot quietly return, and so later changes such as refactoring or Stage 9 features are checked against everything that already worked.

5. What is meant by root cause?

Response: The underlying fault that, when corrected, removes the failure, as opposed to the point where the failure was detected or a symptom that a workaround could hide. It is supported by evidence that rules out the competing explanations.

6. What is refactoring?

Response: Changing the internal structure of code to make it clearer or easier to change without changing its external behaviour. It is done in small steps, with the same tests passing before and after, and kept separate from repairs and features.

7. What is a swallowed exception?

Response: An exception that is caught and then ignored, for example with except Exception: pass or by returning a default. The failure is hidden, the caller is not told, and the program carries on in a possibly invalid state. That makes defects harder to detect and diagnose.

8. What is a code smell?

Response: A surface sign in code that suggests a deeper design or maintainability problem, such as a long method, duplicated logic, magic strings, deep nesting or mixed responsibilities. It is not a bug in itself, but a prompt to look closer and possibly refactor.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: As candidate hypotheses, recorded only after the group's own hypothesis. Each one is checked against the requirements, the actual code and runs we performed ourselves, then accepted, modified or rejected with a reason. Copilot cannot run our tests and may invent requirements or causes, so a convincing explanation is not evidence.

10. What is the Stage 8 engineering rule?

Response: Do not change code until the failure is reproduced, the expected behaviour is traced to a requirement, and a hypothesis has been tested with evidence. Repair the supported root cause with the smallest change, prove it with a failing-then-passing regression test and a full-suite run, and refactor only separately under passing before/after tests. Copilot output stays a checked suggestion, never the diagnosis.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [x] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [x] Human PR review, feedback resolution and integrated retest recorded.
- [x] Tutorial, three reflections and ten formative responses complete.
- [x] Local recovery metadata excluded from submitted source.
- [x] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: verified integrated code SHA b3a3b5800276979112cf7329ac5bb08c62bbb86f (88 passed for all four members). The submitted SHA will be the merge of the docs/stage08-evidence PR, which adds only this record and no executable changes. As in Stage 6, a file cannot contain its own future commit SHA, so that SHA is reported at submission.
Unresolved issues or incomplete checks / owner / next action: no unresolved code defects; both are repaired and the suite passes.
The project is now ready for stage 9 using the main branch.
