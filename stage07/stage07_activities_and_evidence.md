# Stage 7 Testing and Verification Record

- Group/tutorial: Online Group 4, Tuesday 17:30 tutorial 
- Members, GitHub usernames and cohorts: Novica Baloski (@BN007-CMD, UG); Emilio Rojas-Terry (@ucemilio, UG); Quang Le,  (@quangle330, UG); Brendan Potter (@BrendoAC11, UG)
- Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register P3 through the service; find it in the store. | Register a duplicate ID (`P1`, or ` P1 ` after trimming); expect ValueError. | `find_patient('P3') is new_patient`; after a duplicate, `find_patient('P1') is clinic.alex`, its name is unchanged, and the patient list is unchanged. |
| FR-05 Prevent practitioner conflict | Same practitioner at a different time, or a different practitioner at the same time, is allowed. | Same practitioner at the same time is rejected with ValueError. | Existing booking stays SCHEDULED and `list_appointments() == [first]` after the rejection. |
| FR-06 Cancel appointment | Cancel a SCHEDULED appointment. | Cancel it again, or cancel a COMPLETED one; expect ValueError. | Cancel returns the same object with status CANCELLED; after a rejection the status is unchanged. |
| FR-07 Retain cancelled history | Cancel, then find and list the appointment. | Cancel an unknown ID; expect LookupError and other appointments untouched. | `find_appointment('A1') is booked` and `list_appointments() == [booked]`, with participants and time unchanged. |


### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: It can never fail, so it checks no behaviour at all.
 
`assert appointment is not None`
Judgement: Weak/unclear  Why: It only shows something was returned, not that it is the right appointment or in the right state. It is strong only if "an object is returned" is the stated behaviour.
 
`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: It checks the exact outcome of cancel. Limit: it does not show the appointment is retained in the store or that other fields are unchanged (those need separate assertions, as in TEST-08 and the retained-history test).
 
`assert len(results) > 0`
Judgement: Weak/unclear  Why: Any non-empty result passes, including wrong or extra items. It does not say what or how many results are expected.
 
`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: Identity proves the store holds and returns that exact object, not a copy. Limit: it says nothing about status, and it does not show there are no duplicates (that needs a list check).


### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 
- Blank, whitespace-only or non-text IDs (`''`, `'   '`, `None`, `101`) for patient, practitioner, appointment: ValueError, store unchanged - revision 2 ID contract (TEST-02, 05, 12, 30; Stage 6 invalid-ID tests).
- Whitespace-only name or specialty: ValueError (TEST-03, TEST-05). Padded valid values are accepted and trimmed (TEST-01, 04; padded IDs in TEST-18).
- IDs differing only by case (`p1` vs `P1`): distinct, case-sensitive (TEST-19).
- Same practitioner, same time: ValueError, first booking kept - AC-04.1 (TEST-26). One minute later, or a different practitioner at the same time: allowed - AC-04.2 and the exact-time rule (TEST-27, 28).
- Cancelled appointment: cancelling again raises ValueError and status stays CANCELLED - AC-05.3 (TEST-09, Stage 6 test). A cancelled slot can be rebooked because only SCHEDULED appointments occupy time - BR-05 (Stage 6 test).
- Invalid transitions: cancelling COMPLETED raises ValueError (TEST-10, BR-06); direct status assignment raises AttributeError (TEST-11); plain-string status is rejected (TEST-15).


### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Asserts only that the object is not None; passes even if fields or status are wrong. | After booking, assert status is SCHEDULED, patient and practitioner are the registered objects, and the time matches (TEST-21). |
| 2 | Same weak not-None check; proves existence only. | After registering, assert the store returns that same Patient and the patient list contains it (TEST-16). |
| 3 | `assert True` can never fail. | Cancel an appointment and assert CANCELLED; cancel again and assert ValueError with status unchanged (TEST-08, 09). |
| 4 | Assumes SMS notifications, which are not in the revision 2 baseline - an invented requirement. | Replace with a baseline behaviour: a cancelled appointment is retained and listed (FR-07, AC-05.2). |
| 5 | Also assumes SMS notification; nothing to trace to. | Replace with: a conflicting booking is rejected and the store is unchanged (TEST-26). |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
Coverage only shows which lines ran, not whether anything checked the results. A test with no meaningful assertion, or one that misses requirements, boundaries and error cases, still reaches 100% while proving very little.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| Patient validation | Rev 2 contract | TEST-01 | Unit | test_patient_stores_trimmed_id_and_name / project/tests/test_domain.py | Trimmed ID and name | [record] | Student-authored |
| Patient validation | Rev 2 contract (blank ID is not AC-01.2) | TEST-02 | Unit | test_blank_or_non_text_patient_id_is_rejected | ValueError | [record] | Student-authored |
| Patient validation | Rev 2 contract | TEST-03 | Unit | test_blank_or_non_text_patient_name_is_rejected | ValueError | [record] | Student-authored |
| Practitioner validation | Rev 2 contract | TEST-04 | Unit | test_practitioner_stores_trimmed_fields | Trimmed fields | [record] | Student-authored |
| Practitioner validation | Rev 2 contract | TEST-05 | Unit | test_practitioner_requires_id_name_and_specialty | ValueError per blank field | [record] | Student-authored |
| Patient identity | Rev 2 contract | TEST-06 | Unit | test_patient_id_cannot_be_reassigned | AttributeError, ID unchanged | [record] | Student-authored |
| Appointment construction | Rev 2 contract | TEST-07 | Unit | test_new_appointment_is_scheduled_with_given_participants | SCHEDULED, same objects | [record] | Student-authored |
| FR-06 | AC-05.1 | TEST-08 | Unit | test_cancel_changes_status_to_cancelled | CANCELLED | [record] | Student-authored |
| FR-06 | AC-05.3 | TEST-09 | Unit | test_repeated_cancel_is_rejected_and_status_kept | ValueError, status kept | [record] | Student-authored |
| FR-06 | BR-06 | TEST-10 | Unit | test_completed_appointment_cannot_be_cancelled | ValueError, COMPLETED kept | [record] | Student-authored |
| Appointment status guard | Rev 2 contract | TEST-11 | Unit | test_appointment_status_cannot_be_set_directly | AttributeError, unchanged | [record] | Student-authored |
| Appointment validation | Rev 2 contract | TEST-12 | Unit | test_blank_appointment_id_is_rejected | ValueError | [record] | Student-authored |
| Appointment validation | Rev 2 contract | TEST-13 | Unit | test_appointment_requires_participant_objects | ValueError | [record] | Student-authored |
| Appointment validation | Rev 2 contract | TEST-14 | Unit | test_appointment_time_must_be_naive_minute_precision | ValueError | [record] | Student-authored |
| Appointment validation | Rev 2 contract | TEST-15 | Unit | test_appointment_status_must_be_an_enum_member | ValueError | [record] | Student-authored |
| FR-01 | AC-01.1 | TEST-16 | Service | test_register_patient_stores_the_returned_object / project/tests/test_services.py | Stored and listed | [record] | Student-authored |
| FR-01 | AC-01.2 | TEST-17 | Service | test_duplicate_patient_id_keeps_the_original | ValueError, original kept | [record] | Student-authored |
| FR-01 | Rev 2 ID contract (trim) | TEST-18 | Service | test_duplicate_patient_id_after_trimming_is_rejected | ValueError, list unchanged | [record] | Student-authored |
| FR-01 | Rev 2 ID contract (case) | TEST-19 | Service | test_ids_differing_only_by_case_are_distinct | `p1` registered separately | [record] | Student-authored |
| Practitioner registration | BR-01/02 (unique IDs per entity type) | TEST-20 | Service | test_duplicate_practitioner_id_keeps_the_original | ValueError, original kept | [record] | Student-authored |
| FR-03 | AC-03.1, AC-06.1 | TEST-21 | Service | test_book_appointment_stores_a_scheduled_appointment | SCHEDULED, stored | [record] | Student-authored |
| FR-03 | AC-03.2 | TEST-22 | Service | test_booking_unknown_patient_is_rejected | LookupError, nothing stored | [record] | Student-authored |
| FR-03 | AC-03.2 | TEST-23 | Service | test_booking_unknown_practitioner_is_rejected | LookupError, nothing stored | [record] | Student-authored |
| FR-03 | Rev 2 time contract | TEST-24 | Service | test_booking_with_invalid_time_is_rejected | ValueError, nothing stored | [record] | Student-authored |
| FR-03 | Rev 2 unique-ID contract (appointments) | TEST-25 | Service | test_duplicate_appointment_id_keeps_the_original | ValueError, original kept | [record] | Student-authored |
| FR-05 | AC-04.1 | TEST-26 | Service | test_same_practitioner_same_time_conflicts | ValueError, first kept | [record] | Student-authored |
| FR-05 | AC-04.2 | TEST-27 | Service | test_different_practitioner_same_time_is_allowed | Both stored | [record] | Student-authored |
| FR-05 | Exact-time rule (boundary) | TEST-28 | Service | test_same_practitioner_one_minute_later_is_allowed | Both stored | [record] | Student-authored |
| Appointment lookup | Rev 2 ID contract | TEST-29 | Service | test_find_unknown_appointment_raises_lookup_error | LookupError | [record] | Student-authored |
| Appointment lookup | Rev 2 ID contract | TEST-30 | Service | test_find_appointment_invalid_id_raises_value_error | ValueError | [record] | Student-authored |
| Store integrity | Rev 2 registered-object contract | TEST-31 | Service | test_store_rejects_appointment_with_lookalike_patient | ValueError, nothing stored | [record] | Student-authored |
| FR-05 | AC-04.1 | TEST-32 | Service | test_exact_time_conflict_is_rejected_with_multiple_existing_appointments / project/tests/test_services.py | ValueError; both existing appointments unchanged | [record after adding and running] | Student-authored (Copilot idea, human-modified) |
| FR-05 | AC-04.2 | TEST-33 | Service | test_different_practitioner_same_time_allowed_in_populated_schedule / project/tests/test_services.py | All four bookings stored | [record after adding and running] | Student-authored (Copilot idea, human-modified) |
| FR-02, FR-03 lookup, FR-06, FR-07 | AC-02.1, AC-02.2, AC-05.1 to 05.3, BR-05, BR-06 | (Stage 6, no TEST IDs) | Service | Find patient/practitioner, cancel, retain, rebook tests / project/tests/test_services.py | As in docstrings | [record: 38 passed at a74ea06 before Stage 7] | Student-authored (Stage 6) |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-01 | Patient validation | Rev 2 | Positive | Valid input trimmed | Trimmed values | Trimming rule |
| TEST-02 | Patient validation | Rev 2 | Negative/Boundary | Blank/non-text IDs rejected | ValueError | Non-text as well as blank |
| TEST-03 | Patient validation | Rev 2 | Negative/Boundary | Name required | ValueError | Name rule separate from ID |
| TEST-04 | Practitioner validation | Rev 2 | Positive | Valid fields trimmed | Trimmed fields | Specialty covered |
| TEST-05 | Practitioner validation | Rev 2 | Negative/Boundary | Each field required | ValueError | One failing field at a time |
| TEST-06 | Patient identity | Rev 2 | Negative | ID read-only | AttributeError, unchanged | Immutability with state check |
| TEST-07 | Appointment construction | Rev 2 | Positive | Initial status and storage | SCHEDULED, same objects | Identity of participants |
| TEST-08 | FR-06 | AC-05.1 | Positive | Cancel changes status | CANCELLED | Domain-level evidence |
| TEST-09 | FR-06 | AC-05.3 | Negative | Repeat cancel rejected | ValueError, kept | State after rejection |
| TEST-10 | FR-06 | BR-06 | Negative | COMPLETED not cancellable | ValueError, kept | Non-SCHEDULED start state |
| TEST-11 | Status guard | Rev 2 | Negative | No direct status set | AttributeError | Cannot bypass cancel() |
| TEST-12 | Appointment validation | Rev 2 | Negative/Boundary | Blank ID rejected | ValueError | ID rule |
| TEST-13 | Appointment validation | Rev 2 | Negative | Wrong participant types | ValueError | IDs and swapped objects |
| TEST-14 | Appointment validation | Rev 2 | Boundary | Naive, minute precision | ValueError | Four bad-time forms |
| TEST-15 | Appointment validation | Rev 2 | Negative | Enum status only | ValueError | String lookalike |
| TEST-16 | FR-01 | AC-01.1 | Positive | Register via service | Stored object returned | Checks the store list, not just the return value |
| TEST-17 | FR-01 | AC-01.2 | Negative | Duplicate ID rejected | ValueError, original kept | Original name and list unchanged |
| TEST-18 | FR-01 | Rev 2 ID contract | Boundary | Trimmed duplicate | ValueError | Whitespace cannot create a second P1 |
| TEST-19 | FR-01 | Rev 2 ID contract | Boundary | Case-sensitive IDs | Both patients kept | Counterpart to TEST-18 |
| TEST-20 | Practitioner registration | BR-01/02 (unique IDs per entity type) | Negative | Duplicate practitioner ID | ValueError, original kept | Covers practitioners, not only patients |
| TEST-21 | FR-03 | AC-03.1, 06.1 | Positive | Book with real objects | SCHEDULED, stored | Full field and store check |
| TEST-22 | FR-03 | AC-03.2 | Negative | Unknown patient | LookupError, empty store | Nothing partially stored |
| TEST-23 | FR-03 | AC-03.2 | Negative | Unknown practitioner | LookupError, empty store | Second half of AC-03.2 |
| TEST-24 | FR-03 | Rev 2 time contract | Boundary | Seconds in time | ValueError, empty store | Validation reached through the service |
| TEST-25 | FR-03 | Rev 2 unique-ID contract | Negative | Reused appointment ID | ValueError, original kept | No overwrite |
| TEST-26 | FR-05 | AC-04.1 | Negative | Practitioner conflict | ValueError, first kept | Existing booking untouched |
| TEST-27 | FR-05 | AC-04.2 | Positive | Different practitioner same time | Both stored | Rule is per practitioner |
| TEST-28 | FR-05 | Exact-time rule | Boundary | One minute later | Both stored | No duration-overlap rule invented |
| TEST-29 | Appointment lookup | Rev 2 | Negative | Unknown ID | LookupError | Absence vs invalid |
| TEST-30 | Appointment lookup | Rev 2 | Negative/Boundary | Invalid ID | ValueError | Distinct from absence |
| TEST-31 | Store integrity | Rev 2 registered-object contract | Negative | Lookalike patient object | ValueError, empty store | Store only accepts registered objects |
| TEST-32 | FR-05 | AC-04.1 | Negative | Exact-time conflict when the practitioner already has several bookings | ValueError; list is exactly the two originals; both SCHEDULED, first's fields unchanged | Conflict detection across several stored appointments, with full state check after rejection |
| TEST-33 | FR-05 | AC-04.2 | Positive | Different practitioner at times already taken by D1, in a populated schedule | Four appointments stored | AC-04.2 with every D2 booking coinciding with a D1 booking |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TEST-01 | Padded strings | Construct Patient | Trimmed equality | Equality shows trimming happened |
| TEST-02 | Bad IDs | Construct Patient | `raises(ValueError)` | Specific exception shows the rule fired |
| TEST-03 | Bad names | Construct Patient | `raises(ValueError)` | Isolates the name rule |
| TEST-04 | Padded fields | Construct Practitioner | Three equality asserts | Every field checked |
| TEST-05 | One blank field per case | Construct Practitioner | `raises(ValueError)` | Each field enforced |
| TEST-06 | Patient P1 | Assign `patient_id` | AttributeError; still P1 | Rejection and no change |
| TEST-07 | Patient, practitioner | Construct Appointment | SCHEDULED; `is` participants; time equal | Initial state and stored data |
| TEST-08 | SCHEDULED appointment | `cancel()` | `status is CANCELLED` | Direct criterion outcome |
| TEST-09 | Already cancelled | `cancel()` | ValueError; CANCELLED | Rejection with state kept |
| TEST-10 | COMPLETED appointment | `cancel()` | ValueError; COMPLETED | Only SCHEDULED may cancel |
| TEST-11 | Fresh appointment | Assign `status` | AttributeError; SCHEDULED | Status guarded |
| TEST-12 | Valid participants, bad ID | Construct | ValueError | ID required |
| TEST-13 | Wrong participant types | Construct | ValueError x3 | Each participant type-checked |
| TEST-14 | Four invalid times | Construct | ValueError | Each time boundary |
| TEST-15 | Status `'scheduled'` | Construct | ValueError | Enum enforced |
| TEST-16 | Fixture clinic | `register_patient('P3', ...)` | Store `find_patient` is the object; list has 3 | Proves stored, not just returned |
| TEST-17 | Fixture clinic | Register duplicate P1 | ValueError; P1 is alex, name unchanged, list unchanged | Rejection leaves state intact |
| TEST-18 | Fixture clinic | Register ` P1 ` | ValueError; list unchanged | Trimming applies to duplicates |
| TEST-19 | Fixture clinic | Register `p1` | New object; both IDs resolve separately | Case-sensitive IDs |
| TEST-20 | Fixture clinic | Register duplicate D1 | ValueError; taylor kept | Original not overwritten |
| TEST-21 | Fixture clinic | Book A1 | Status, patient, practitioner, time, lookup, list | Every observable outcome |
| TEST-22 | Fixture clinic | Book unknown patient | LookupError; list empty | Nothing stored on failure |
| TEST-23 | Fixture clinic | Book unknown practitioner | LookupError; list empty | Same |
| TEST-24 | Fixture clinic | Book with seconds | ValueError; list empty | Invalid time stopped |
| TEST-25 | A1 booked | Book A1 again | ValueError; original kept | No overwrite |
| TEST-26 | A1 at 9:00 for D1 | Book A2 for D1 at 9:00 | ValueError; A1 SCHEDULED; list `[first]` | Conflict rejected, state unchanged |
| TEST-27 | A1 at 9:00 for D1 | Book A2 for D2 at 9:00 | List `[first, second]` | Conflict is per practitioner |
| TEST-28 | A1 at 9:00 for D1 | Book A2 for D1 at 9:01 | List `[first, later]` | Boundary of exact-time rule |
| TEST-29 | Fixture clinic | Find A404 | LookupError | Absence reported |
| TEST-30 | Fixture clinic | Find invalid ID | ValueError | Invalid distinct from absent |
| TEST-31 | Lookalike P1 Patient | `data_store.add_appointment` | ValueError; list empty | Store integrity |
| TEST-32 | A1 (P1, D1, 9:00) and A2 (P2, D1, 10:00) booked | Book A3 (P2, D1, 10:00) | ValueError; list == [first, second]; both SCHEDULED; first's patient, practitioner, time unchanged | Conflict matches only one of several existing bookings and nothing else changes |
| TEST-33 | A1 (D1, 9:00) and A2 (D1, 10:00) booked | Book A3 (D2, 9:00) and A4 (D2, 10:00) | List == [first, second, third, fourth] | Both new bookings clash on time with D1 but are allowed because the practitioner differs |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| TEST-01 | Patient construction, trimming | project/tests/test_domain.py::test_patient_stores_trimmed_id_and_name | [record] |
| TEST-02, 03 | Patient validation | test_blank_or_non_text_patient_id/name_is_rejected | [record] |
| TEST-04, 05 | Practitioner construction and validation | test_practitioner_stores_trimmed_fields, test_practitioner_requires_id_name_and_specialty | [record] |
| TEST-06 | Patient ID read-only | test_patient_id_cannot_be_reassigned | [record] |
| TEST-07 | Appointment construction, initial status | test_new_appointment_is_scheduled_with_given_participants | [record] |
| TEST-08 | Cancellation | test_cancel_changes_status_to_cancelled | [record] |
| TEST-09, 10 | Repeated/illegal transitions | test_repeated_cancel_is_rejected_and_status_kept, test_completed_appointment_cannot_be_cancelled | [record] |
| TEST-11 | Status guard | test_appointment_status_cannot_be_set_directly | [record] |
| TEST-12 to 15 | Appointment validation | test_blank_appointment_id..., participants, time, status | [record] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TEST-16 | Register patient, stored | FR-01 / AC-01.1 | project/tests/test_services.py::test_register_patient_stores_the_returned_object | [record] |
| TEST-17 | Duplicate patient rejected | FR-01 / AC-01.2 | test_duplicate_patient_id_keeps_the_original | [record] |
| TEST-18 | Trimmed duplicate rejected | FR-01 / ID contract | test_duplicate_patient_id_after_trimming_is_rejected | [record] |
| TEST-19 | Case-sensitive IDs | FR-01 / ID contract | test_ids_differing_only_by_case_are_distinct | [record] |
| TEST-20 | Duplicate practitioner rejected | BR-01/02 (unique IDs per entity type) | test_duplicate_practitioner_id_keeps_the_original | [record] |
| TEST-21 | Booking stores SCHEDULED appointment | FR-03 / AC-03.1, 06.1 | test_book_appointment_stores_a_scheduled_appointment | [record] |
| TEST-22 | Unknown patient rejected | FR-03 / AC-03.2 | test_booking_unknown_patient_is_rejected | [record] |
| TEST-23 | Unknown practitioner rejected | FR-03 / AC-03.2 | test_booking_unknown_practitioner_is_rejected | [record] |
| TEST-24 | Invalid time rejected | FR-03 / time contract | test_booking_with_invalid_time_is_rejected | [record] |
| TEST-25 | Duplicate appointment ID rejected | FR-03 / unique-ID contract | test_duplicate_appointment_id_keeps_the_original | [record] |
| TEST-26 | Practitioner conflict rejected | FR-05 / AC-04.1 | test_same_practitioner_same_time_conflicts | [record] |
| TEST-27 | Different practitioner allowed | FR-05 / AC-04.2 | test_different_practitioner_same_time_is_allowed | [record] |
| TEST-28 | One minute later allowed | FR-05 / boundary | test_same_practitioner_one_minute_later_is_allowed | [record] |
| TEST-29 | Unknown appointment lookup | ID contract | test_find_unknown_appointment_raises_lookup_error | [record] |
| TEST-30 | Invalid appointment ID | ID contract | test_find_appointment_invalid_id_raises_value_error | [record] |
| TEST-31 | Store rejects lookalike patient | Registered-object contract | test_store_rejects_appointment_with_lookalike_patient | [record] |
| TEST-32 | Conflict rejected with several existing bookings | FR-05 / AC-04.1 | test_exact_time_conflict_is_rejected_with_multiple_existing_appointments | [record] |
| TEST-33 | Different practitioner allowed in populated schedule | FR-05 / AC-04.2 | test_different_practitioner_same_time_allowed_in_populated_schedule | [record] |
| (Stage 6) | Cancel, retain, rebook, lookups | FR-02, FR-06, FR-07 / AC-02.x, 05.x | Stage 6 tests in project/tests/test_services.py | [record] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Patient creation | Blank, whitespace, None, non-text ID | ValueError | TEST-02 |
| Patient creation | Blank/None name | ValueError | TEST-03 |
| Practitioner creation | Blank ID, name or specialty | ValueError | TEST-05 |
| Appointment creation | Blank ID | ValueError | TEST-12 |
| Appointment creation | IDs or swapped objects as participants | ValueError | TEST-13 |
| Appointment time | Seconds, microseconds, timezone, string | ValueError | TEST-14 |
| Appointment status | Plain string | ValueError | TEST-15 |
| Cancel | Already cancelled | ValueError, status kept | TEST-09 |
| Cancel | COMPLETED | ValueError, status kept | TEST-10 |
| Status assignment | Direct set | AttributeError, unchanged | TEST-11 |
| Register patient | Duplicate ID, trimmed duplicate | ValueError, original kept | TEST-17, 18 |
| Register practitioner | Duplicate ID | ValueError, original kept | TEST-20 |
| Booking | Unknown patient / practitioner | LookupError, nothing stored | TEST-22, 23 |
| Booking | Time with seconds | ValueError, nothing stored | TEST-24 |
| Booking | Reused appointment ID | ValueError, original kept | TEST-25 |
| Booking | Same practitioner same time | ValueError, first kept | TEST-26 |
| Booking | Same practitioner same time with several existing bookings | ValueError, existing list unchanged | TEST-32 |
| Booking | Same practitioner +1 minute | Allowed | TEST-28 |
| Booking | Different practitioner at times already taken, populated schedule | Allowed | TEST-33 |
| Find appointment | Unknown ID / invalid ID | LookupError / ValueError | TEST-29, 30 |
| Store | Lookalike patient object | ValueError, nothing stored | TEST-31 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-05 Prevent practitioner conflict
Acceptance criterion:
- AC-04.1: A booking must be rejected when the same practitioner already has a SCHEDULED appointment at the same date/time.
- AC-04.2: A booking at the same date/time is allowed when it is for a different practitioner.
Behaviour to test: Conflict checking is based on practitioner + exact appointment time. Rejected bookings must not alter existing stored appointments. The rule applies to existing SCHEDULED appointments only.
Human-first test idea/categories (written before using Copilot): Positive (bookings that should succeed); Negative (bookings that should be rejected); Boundary (exact-time comparison only); State preservation after rejection.
Prompt and purpose: Asked Copilot for additional FR-05 test ideas that trace directly to AC-04.1 or AC-04.2, do not duplicate TEST-26, TEST-27 or TEST-28, use the real services and data store (no mocks), name the expected exception type, and state the unchanged state after rejection. [paste or link the exact prompt]
 
### Candidate 1
- Copilot test idea/candidate: Conflicting booking where the existing appointment belongs to a different patient but the same practitioner and time.
- What it claims to verify: The conflict rule depends on practitioner availability, not patient identity.
- Requirement trace: FR-05 / AC-04.1
- Assertion quality: Strong (`pytest.raises(ValueError)` and original booking remains), but identical to an existing test.
- Human critique: TEST-26 already books P1 first, then P2, with the same practitioner and time.
- Decision: Reject
- Reason: Exact behavioural duplicate of TEST-26.
- Final test reference if accepted/modified: Not retained
- Actual verification result: Not run
### Candidate 2
- Copilot test idea/candidate: Two appointments for the same practitioner at different times, then a third booking that conflicts with only one of them.
- What it claims to verify: Conflict detection checks all of the practitioner's SCHEDULED appointments and rejects an exact match.
- Requirement trace: FR-05 / AC-04.1
- Assertion quality: Good: `pytest.raises(ValueError)` and `list_appointments() == [first, second]`.
- Human critique: Not covered by TEST-26, 27 or 28. It verifies rejection when several appointments exist and that nothing extra is stored.
- Decision: Accept (with the Candidate 4 post-rejection assertions added)
- Reason: Tests AC-04.1 in a richer state and checks the store is unchanged.
- Final test reference if accepted/modified: TEST-32, test_exact_time_conflict_is_rejected_with_multiple_existing_appointments in project/tests/test_services.py
- Actual verification result: [record only after adding and running]
### Candidate 3
- Copilot test idea/candidate: A cancelled appointment at a time slot should not create a practitioner conflict.
- What it claims to verify: Only SCHEDULED appointments occupy a practitioner's time.
- Requirement trace: FR-05 / AC-04.1
- Assertion quality: Checks the replacement is SCHEDULED only; does not check the cancelled record is retained.
- Human critique: Already covered by test_cancelled_slot_can_be_booked_again, which is stronger because it also verifies retained history.
- Decision: Reject
- Reason: Behaviour already exercised in the suite.
- Final test reference if accepted/modified: Not retained
- Actual verification result: Not run
### Candidate 4
- Copilot test idea/candidate: After a rejected conflicting booking, verify every property of the existing appointment is unchanged.
- What it claims to verify: Rejection does not mutate existing appointment data.
- Requirement trace: FR-05 / AC-04.1
- Assertion quality: Specific field checks (status, patient, practitioner, date_time, list), but they are not a separate behaviour.
- Human critique: TEST-26 already checks the rejection, the original remains and no new appointment is added. Extra field checks add little as a stand-alone test.
- Decision: Modify
- Reason: Useful as stronger post-rejection assertions inside another conflict-rejection test.
- Final test reference if accepted/modified: Merged into TEST-32
- Actual verification result: Not run
### Candidate 5
- Copilot test idea/candidate: Different practitioners at the same time when several appointments are already stored. As generated: A1 (D1, 9:00), A2 (D2, 9:00), A3 (D2, 10:00), then assert all three are listed.
- What it claims to verify: Conflict scope stays practitioner-specific in a populated schedule.
- Requirement trace: FR-05 / AC-04.2
- Assertion quality: Weak as generated. A1 and A2 repeat TEST-27, and A3 is D2 at a time D2 is free, so it does not test AC-04.2 at all.
- Human critique: Looked convincing as "populated schedule" but only the first two bookings exercise AC-04.2, and they duplicate TEST-27.
- Decision: Modify
- Reason: Rewritten so every new D2 booking coincides with an existing D1 booking: book D1 at 9:00 and 10:00, then D2 at 9:00 and 10:00, and assert all four are stored in order.
- Final test reference if accepted/modified: TEST-33, test_different_practitioner_same_time_allowed_in_populated_schedule in project/tests/test_services.py
- Actual verification result: [record only after adding and running]
### Best accepted ideas
- Idea A (TEST-32): Multiple existing appointments, then an exact-time conflict. Verifies AC-04.1, ValueError, list == [first, second], both still SCHEDULED, first's patient, practitioner and time unchanged.
- Idea B (TEST-33): Different practitioner remains allowed in a populated schedule. Verifies AC-04.2 and that all four appointments are retained.
Both trace to FR-05, add no business rules, use no mocks, and do not duplicate TEST-26, 27 or 28.
 
Before accepting checks (traces to a criterion; can fail for the right reason; asserts required behaviour; no invented rule; no private implementation dependence): applied to each candidate above.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? Candidate 5 (different practitioners in a populated schedule).
Why was it weak? It read as a richer version of TEST-27, but its first two bookings were exactly TEST-27 and its third booking (D2 at a free time) never exercised AC-04.2. Asserting that all three appear in the list would pass even if the conflict rule ignored practitioner identity for later bookings.
How did you strengthen it? Rebuilt it as TEST-33 so each D2 booking sits at a time already held by D1; the test now only passes if the conflict check is scoped to practitioner and time together. Candidate 4 was also strengthened by merging its field checks into TEST-32 rather than keeping it as a stand-alone test.
Accepted / modified / rejected test decisions and evidence: Rejected 1 and 3 (duplicates of TEST-26 and the Stage 6 rebooking test); accepted 2 (TEST-32); modified 4 (merged into TEST-32) and 5 (TEST-33). See H.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| python -m pytest | project/ | [git rev-parse HEAD] | [N] | [N] | [none / summary] | [none / classify] | [paste summary line. Before Stage 7: 38 passed at a74ea06. Stage 7 adds about 29 domain cases, 19 service cases and the 2 new FR-05 tests (TEST-32, 33) by my count, so roughly 88 if none overlap - confirm from real output] |
 
Individual test runs and changed-order independence evidence: [e.g. `python -m pytest path::test_name`; a reordered or random-order run; the shared `clinic` fixture builds a fresh store per test]
Optional tutor-led demonstration notes:
Requirement -> test -> failure/observation -> diagnosis -> change -> verification: [links if applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove?
It does not prove persistence (data is in memory), behaviour with large volumes or concurrent bookings, time-zone or daylight-saving handling, or any user interface. It only checks cases we thought of, and COMPLETED appointments are only created as test fixtures, so no workflow for completing appointments is verified.
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? Coverage shows lines ran, not that assertions checked the right outcome, so a high percentage can still miss wrong results.
Optional fixtures/parametrisation used and why, if any: The `clinic` fixture gives every service test a fresh store with registered synthetic patients and practitioners, keeping tests independent of order. Parametrisation (TEST-02, 03, 05, 12, 14, 30 and the invalid-ID tests) runs many invalid inputs through one rule without copy-pasted tests.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| Stage07 | /feature/stage07-testing-and-evidence | https://github.com/BN007-CMD/st1-assignment-3/pull/6 | Emilio took the lead on Stage07 and as below every other member assisted with evidence | N/A | Stage07 has been completed, and Jay will continue with Stage08 |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| Emilio (Stage 7 lead) | Test design, traceability, implementation, integration | 11068b432586eb0c6ad9b90b357780da5aeb32f1, 86 passed in 0.18s, 78 passed in 0.11s &  78 passed in 0.14s, 1 passed in 0.03s |
| Novica | 11068b432586eb0c6ad9b90b357780da5aeb32f1, 86 passed in 0.18s, 78 passed in 0.11s &  78 passed in 0.14s, 1 passed in 0.03s | Stage 7 Test-26.png |
| Jay | 11068b432586eb0c6ad9b90b357780da5aeb32f1, 86 passed in 0.24s, 78 passed in 0.08s & 78 passed in 0.08s, 1 passed in 0.03s | Stage 7 Test-32.png |
| Brendan | 11068b432586eb0c6ad9b90b357780da5aeb32f1, 86 passed in 0.23s, 78 passed in 0.09s & 78 passed in 0.09s, 1 passed in 0.04s | Stage 7 Test-33.png |

## N Formative Questions

1. What question does verification answer?
Did we build the product right - does it meet its specification and requirements?

2. What question does validation answer?
Did we build the right product - does it meet what the client and users actually need?

3. What is a unit test?
A small automated test that checks one unit of behaviour (such as one method or class) in isolation, with a clear expected result.

4. What is a pytest fixture?
A reusable setup function (marked with `@pytest.fixture`) that gives tests fresh, consistent data, like our `clinic` store with registered patients and practitioners.

5. What is parametrisation in pytest?
Using `@pytest.mark.parametrize` to run one test with several input sets, so each case is reported separately without copy-pasted tests.

6. What is regression testing?
Rerunning the accumulated tests after a change to confirm that previously working behaviour has not broken.

7. What does code coverage tell us, and what does it not prove?
It tells us which code ran during tests. It does not prove the assertions are meaningful, the requirements are met, or the behaviour is correct.

8. What makes an assertion weak?
It would still pass when the behaviour is wrong - for example `assert True`, a not-None check, or `len(x) > 0` - because it does not check the specific required outcome.

9. What is the appropriate role of GitHub Copilot as a test assistant?
A source of draft ideas only. A human decides what to test from the requirements first, then critiques, modifies or rejects each suggestion and only claims results from tests actually run.

10. What is the Stage 7 engineering rule?
Tests must trace to a requirement or contract, assert the required observable behaviour, be able to fail for the right reason, and be recorded honestly with what was actually run.

## O Stage Completion

Tested Stage 7 main SHA: 11068b432586eb0c6ad9b90b357780da5aeb32f1, 86 passed in 0.18s, 78 passed in 0.11s &  78 passed in 0.14s, 1 passed in 0.03s
Full-suite result: Confirmed
Unresolved defects and effect on baseline: Confirmed
Clean working tree and integration evidence: Confirmed - nothing to commit, working tree clean
Stage 8 handover status: Complete;  Stage 8 work assigned to Jay
All tutorial/formative responses and traceability/Copilot decisions complete: Confirmed