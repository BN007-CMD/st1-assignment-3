# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Online Group 4, Tuesday 17:30 tutorial 
- Members, GitHub usernames and cohorts: Novica Baloski (@BN007-CMD, UG); Emilio Rojas-Terry (@ucemilio, UG); Quang Le,  (@quangle330, UG); Brendan Potter (@BrendoAC11, UG)
- Repository URL: https://github.com/BN007-CMD/st1-assignment-3
- Starting SHA: `5ad6f803fe04665237f8405284bc2dddf3bd007b`. This was main when Stage 6 work began: the supplied starter commit `044fe2ec25184bb505c0d154564eb1679c0dcc43` plus two group-index README edits.

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Find a registered patient by patient ID (FR-02)
- Context: `PatientService.find_patient` raises `NotImplementedError`, so clinic staff can register a patient but cannot retrieve that record again. The store already returns `None` for a valid absent ID and rejects blank IDs, but the service contract is different: absence must be reported as an error, not a silent `None`.
- Requirement: FR-02 Find a patient by patient ID, with the revision 2 ID contract (IDs are strings, trimmed, non-blank and case-sensitive).
- Acceptance criteria:
  1. AC-02.1: after registering P1, `find_patient('P1')` returns that same registered object (`is`), not a copy.
  2. Surrounding whitespace is trimmed: `find_patient('  P1  ')` returns the P1 object.
  3. Case-sensitive: `find_patient('p1')` raises `LookupError` when only P1 is registered.
  4. AC-02.2: a valid unregistered ID such as P404 raises `LookupError`.
  5. Blank, whitespace-only or non-text IDs raise `ValueError` (not `LookupError`).
  6. A failed lookup creates no patient and leaves the stored patients unchanged.
- Scope: `PatientService.find_patient` in `project/smartcare/services.py` and new tests in `project/tests/test_services.py`. Out of scope: name or fuzzy search, practitioner lookup (separate issue), console menu (Stage 9), any change to `domain.py` or `data_store.py`.
- Definition of Done: all six criteria have passing assertions; the eight supplied tests still pass; the full suite has been run from `project/` with the result recorded; a member other than the author has reviewed the actual diff, with human observations recorded before the Copilot comparison; feedback is resolved; the PR is merged to main and every member has pulled and rerun the suite.
- Owner: (@BN007-CMD)
- Actual issue link: https://github.com/BN007-CMD/st1-assignment-3/issues/1

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Cancel a scheduled appointment and keep it as session history (FR-06, FR-07)
- Context: `AppointmentService.cancel_appointment` raises `NotImplementedError`. `Appointment.cancel()` already guards the transition (only SCHEDULED can move to CANCELLED). The service has to coordinate lookup and that domain method without deleting or replacing the record.
- Requirement: FR-06 Cancel only a SCHEDULED appointment; FR-07 Retain the same appointment with CANCELLED status in current-session history; BR-06/07.
- Acceptance criteria:
  1. AC-05.1: cancelling scheduled A1 returns the same stored object with status `CANCELLED`.
  2. AC-05.2: after cancellation, `find_appointment('A1')` and `list_appointments()` still return that same object, with participants and time unchanged.
  3. AC-05.3: cancelling A1 again raises `ValueError` and the status stays `CANCELLED`.
  4. Cancelling an appointment stored as `COMPLETED` raises `ValueError` and it stays `COMPLETED`.
  5. A valid unknown ID raises `LookupError`; a blank or invalid ID raises `ValueError`; in both cases no appointment changes.
  6. Cancelling A1 does not change any other appointment, and existing booking/conflict behaviour still works (a cancelled slot no longer blocks the practitioner).
- Scope: `AppointmentService.cancel_appointment` and cancellation tests. The service must call `Appointment.cancel()`; it must not assign `_status`, delete from the store or create a replacement. No rescheduling, completion workflow or listing (Stage 9).
- Definition of Done: as for FR-02, plus evidence that history is retained (lookup and listing after cancellation) and that failed cancellations leave state unchanged.
- Owner: (@BN007-CMD)
- Actual issue link: https://github.com/BN007-CMD/st1-assignment-3/issues/4

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | Weak | Every commit is a change, so it says nothing about what changed or why. A reviewer can't check the diff against an intention, and it is useless when searching history for when a behaviour changed. |
| final version | Weak | It describes the author's view of timing, not the code. "Final" goes out of date with the next commit and names no behaviour, file or requirement. |
| Add patient search by ID | Strong | Imperative, specific and limited to one behaviour that traces to FR-02. A reviewer knows the diff should contain the lookup and its tests and nothing else. It would only become weak if the commit also contained unrelated edits. |
| fix stuff | Weak | It doesn't say what was broken, what the fix was or which requirement it restores, so nobody can tell whether the fix is correct or complete. |
| Prevent cancellation of completed appointments | Strong | It states the behavioural rule being enforced (FR-06/BR-06: only SCHEDULED can be cancelled), so the reviewer can check for a guard plus a test that a COMPLETED appointment is rejected unchanged. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR mixes one requirement (FR-06/07) with three unrelated changes. The reviewer can no longer tell which lines are needed for cancellation, the linked issue's acceptance criteria don't cover the extra work, and if one part is wrong the whole PR has to be held back or reverted.
- Responsibility and architecture concerns: Renaming patient fields changes the `Patient` public interface that the store, services, console formatter and tests depend on, so it risks breaking working code outside the issue. Restructuring unrelated code may move rules away from their owners (for example, state rules belong in `Appointment`, not the service). A new dependency goes against the starter's standard-library-only runtime and adds a supply-chain and licence question nobody asked for.
- Testing and review concerns: A green run only shows that the existing assertions still pass. The tests might not touch the renamed fields or restructured paths at all. Cancellation evidence (status, same object, retained lookup and listing, rejection without change) is harder to find among unrelated diff lines. The dependency also needs checking for origin, version pinning and whether anything actually uses it.
- Changes to remove or separate, with reasons: Keep only `cancel_appointment` and its tests in this PR. Remove the field renames; if a rename is genuinely needed, raise its own issue with the reason, the affected callers and tests. Remove the restructuring, or open a separate refactoring issue later with before/after tests (that is Stage 8 work). Remove the dependency unless an issue justifies it and the team agrees; cancellation needs none. Small, separate PRs can be reviewed properly and reverted independently.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: No link to the requirement or acceptance criteria, no reference to specific diff lines, and no statement of which tests ran, from which directory, on which commit or with what result. Copilot cannot run our tests in the chat, so "tests pass" is an unverified claim. It also doesn't say whether the tests check the right things.
- Follow-up review question 1: Which acceptance criteria in the linked issue does each changed line satisfy, and is any criterion (for example AC-05.2 retained history) not covered by the diff?
- Follow-up review question 2: Does `cancel_appointment` change status only through `Appointment.cancel()`, and could any line delete the appointment from the store or return a different object?
- Follow-up review question 3: Which test asserts that the returned object `is` the stored appointment and that it is still found and listed after cancellation, rather than just asserting it is not `None`?
- Follow-up review question 4: What happens, and which test proves it, when the ID is blank, valid but unknown, already CANCELLED or COMPLETED? Are `ValueError` and `LookupError` kept distinct, and is state unchanged afterwards?
- Follow-up review question 5: Which exact command, working directory and commit SHA produced the "tests pass" claim, and how many tests ran, including the eight supplied checks?
- Additional questions if useful: Does the diff touch any file outside the issue scope or add a dependency? Could a broken implementation, such as one that deleted the record, still pass the current tests?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | `feature/<short-topic>` for new behaviour (e.g. `feature/stage06-service-operations`), `fix/<topic>` for defects, `test/<topic>` for test-only work, `docs/<topic>` for records/README. Always created from freshly pulled main. |
| Commit message convention | Imperative summary of 72 characters or fewer that names the behaviour, with the requirement ID where one applies, e.g. "Implement patient lookup by trimmed case-sensitive ID (FR-02)". One coherent change per commit; no "changes", "final" or "fix stuff". |
| PR size | A PR covers one issue, touching only the files the issue names, with a diff another member can review properly in one sitting. Exception agreed for Stage 6: issues #1, #3 and #4 are delivered in one PR because the three methods are small (about 40 changed lines in services.py, mostly docstrings) and share one new test file. Splitting them would only create artificial merge conflicts. Each issue still has its own acceptance criteria and its own named reviewer. Unrelated improvements become new issues. |
| Another-member review requirement | Every PR needs an approving review on GitHub from a member who did not author it, and is not merged until every assigned reviewer has approved. Each reviewer records their own observations before running the Copilot comparison. Self-review is preparation only. For the Stage 6 code PR, Emilio reviews the patient lookup (#1), Quang the practitioner lookup (#3) and Brendan the cancellation (#4). |
| Merge rule | Merge only when: the acceptance criteria are met, the author has recorded a full-suite pass from `project/`, feedback is resolved and rechecked by the reviewer, approval is given, and the diff has no unrelated changes. Use a merge commit (not squash) so the review history stays traceable. After merging, everyone pulls main and reruns the full suite. |
| Ownership and rotation | Novica set up the shared repository. Each stage has one stage lead who authors that stage's issues, code, tests and record PRs. Every other member reviews at least one of the lead's PRs, including the Copilot comparison for that PR, and everyone pulls and reruns the suite after each merge. The lead rotates every stage - 6: Novica, 7: Emilio, 8: Quang, 9: Brendan, 12: shared, so everyone authors code and everyone reviews across the assignment.|
| Significant Copilot disclosure rule | Any Copilot output that shaped code, tests or a review decision is declared in the PR description ("AI assistance") and recorded in section H with prompt, output summary, human check, Accept/Modify/Reject and verification. Trivial autocompletion is not logged. Only synthetic data and the necessary diff are shared with Copilot; no credentials or personal information. |
| Timing note | This agreement was written into the record after the Stage 6 code commit (25/10). From Stage 7, the stage lead records any workflow change in the record before coding begins. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [#1](https://github.com/BN007-CMD/st1-assignment-3/issues/1) Find a registered patient by patient ID (FR-02) | FR-02; AC-02.1, AC-02.2; revision 2 ID contract | Novica; reviewer Emilio | Six criteria in section A (FR-02) and in the issue body |  Closed by PR #2 on merge |
| [#3](https://github.com/BN007-CMD/st1-assignment-3/issues/3) Find a registered practitioner by practitioner ID (FR-03 supporting operation) | FR-03 supporting operation; BR-02; revision 2 ID contract | Novica; reviewer Quang | Known lookup returns the registered object; trimmed; case-sensitive; unknown raises LookupError; invalid raises ValueError; patient IDs are not practitioner IDs; no change to stored practitioners | TO RECORD: Closed by PR #2 on merge |
| [#4](https://github.com/BN007-CMD/st1-assignment-3/issues/4) Cancel a scheduled appointment and keep it as session history (FR-06, FR-07) | FR-06, FR-07; AC-05.1 to 05.3; BR-06/07 | Novica; reviewer Brendan | Six criteria in section A (FR-06/07) and in the issue body |  Closed by PR #2 on merge |

The three requirements were first drafted as a single issue (#1). We split them into three focused issues so each could be linked, reviewed and closed on its own. #2 is the code PR, which is why the issues are numbered 1, 3 and 4.

## G Pull request evidence
Repeat this block per PR. Record actual events, not planned approvals.
### Code PR: Stage 6 service operations
- PR link and title: [#2](https://github.com/BN007-CMD/st1-assignment-3/pull/2) Implement Stage 6 patient lookup, practitioner lookup and appointment cancellation
- Linked issue and requirement: Closes #1, #3 and #4; FR-02 (AC-02.1, AC-02.2), FR-03 supporting lookup, FR-06/FR-07 (AC-05.1 to 05.3), BR-06/07
- Feature branch: `feature/stage06-service-operations`
- Changed behaviour:
  - `PatientService.find_patient` and `PractitionerService.find_practitioner` return the registered object for a trimmed, case-sensitive ID. A valid unknown ID raises `LookupError`; blank or non-text IDs raise `ValueError` through the store's existing validation.
  - `AppointmentService.cancel_appointment` reuses `find_appointment`, calls `Appointment.cancel()` (the domain guard) and returns the same stored object. Nothing is deleted or replaced.
  - New `tests/test_services.py`: one fresh-store fixture and 30 test cases (9 patient, 9 practitioner, 12 cancellation).
- Meaningful commits:
  - [`562097f`](https://github.com/BN007-CMD/st1-assignment-3/commit/562097fbdffd0d59472806f4ad7f70ca2acd12a3): implementation and tests
  - [`9c6a7a2`](https://github.com/BN007-CMD/st1-assignment-3/commit/9c6a7a2388c6d970e31a8e725dda9f7936f69c8c): review response, unchanged-state checks in both case-sensitivity tests
- Test command, directory and observed result: `python -m pytest` from `project/` → 38 passed in 0.07s on `562097f`; after the review change, 38 passed in 0.11s on `9c6a7a2`
- Another-member reviewers: Emilio (#1 patient lookup), Quang (#3 practitioner lookup), Brendan (#4 cancellation)
- Human observations recorded before Copilot:
  - Emilio: [review](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5649797680), then [Copilot output](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5649880865), then [comparison](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5649918854)
  - Quang: [review](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5662674181), then [Copilot output](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5662774349), then [comparison](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5663264066)
  - Brendan: [review](https://github.com/BN007-CMD/st1-assignment-3/pull/2#issuecomment-6465382803), then [Copilot output](https://github.com/BN007-CMD/st1-assignment-3/pull/2#issuecomment-6465411622), then [comparison](https://github.com/BN007-CMD/st1-assignment-3/pull/2#issuecomment-6465849371)
  - Each reviewer's own review was posted before their Copilot output, as GitHub's timestamps on the PR show.
- Requirement, responsibilities, test assertions and unrelated-scope checks:
  - Emilio confirmed every FR-02 criterion has a test, identity is checked with `is`, invalid IDs raise `ValueError` separately from `LookupError`, trimming and blank rejection come from `required_text` via the store, and only `services.py` and `test_services.py` changed. Branch run: 38 passed in 0.08s on `562097f`.
  - Quang confirmed the same for FR-03, plus the patient-ID-as-practitioner test, and that `list_practitioners()` returns a new list, so the unchanged-state checks are meaningful. Branch run: 38 passed in 0.09s on `562097f`.
  - Brendan confirmed `cancel_appointment` neither creates nor deletes, relies on the domain `ValueError` for non-SCHEDULED appointments, and that every cancellation criterion has a test. Branch run: 38 passed in 0.09s on `562097f`.
- Key feedback (all non-blocking):
  1. Emilio and Quang: the case-sensitivity tests (`p1`, `d1`) do not check that stored records are unchanged after the failed lookup.
  2. Emilio and Quang: the "not found" messages do not include the requested ID.
  3. Quang: no explicit check that `find_practitioner('D1')` is not Morgan.
  4. Brendan: the rebooking test frees the slot for a different patient, not the same patient.
- Author response/change and verification: [response comment](https://github.com/BN007-CMD/st1-assignment-3/pull/2#issuecomment-6487710885)
  1. Accepted: unchanged-state assertions added to both case-sensitivity tests in `9c6a7a2`. Full suite rerun: 38 passed in 0.11s.
  2. Deferred to Stage 9: the revision 2 contract defines the exception types, not message text. Showing the requested ID is a console concern for the Stage 9 menu.
  3. No change: `found is clinic.taylor` already proves D1 returns Taylor's object, which cannot also be Morgan's; the D2 assertion in the same test checks Morgan separately.
  4. Carried to Stage 7: FR-05/BR-05 is a practitioner rule and no patient-conflict rule exists, so the same patient rebooking a freed slot is a Stage 7 boundary test under FR-05/AC-04.2, not a Stage 6 cancellation criterion.
- Reviewer recheck and approval:
  - Emilio rechecked `9c6a7a2` (38 passed in 0.05s) and [approved](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5693363903)
  - Quang rechecked `9c6a7a2` (38 passed in 0.09s) and [approved](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5692848501)
  - Brendan [approved](https://github.com/BN007-CMD/st1-assignment-3/pull/2#event-34460316220). The review fix does not touch the cancellation tests.
- Merge outcome and SHA: merged with a merge commit after all three approvals; [`a74ea06a5fcdca236f1f220fa1219ebc98a7ca95`](https://github.com/BN007-CMD/st1-assignment-3/commit/a74ea06a5fcdca236f1f220fa1219ebc98a7ca95)
- Significant AI assistance: the implementation and tests were drafted with Claude (Anthropic), as declared in the PR description. The author read every changed line, checked each method against the acceptance criteria and the existing domain/store behaviour, and ran the full suite before opening the PR. Each reviewer used GitHub Copilot for the required review comparison after their own review (see H and I).
- Linked issue closure: #1, #3 and #4 closed automatically by "Closes" on merge, confirmed on the Issues tab
- Each member updated main (all on `a74ea06`):
  - Novica: 38 passed in 0.10s
  - Emilio: 38 passed in 0.07s
  - Quang: 38 passed in 0.09s
  - Brendan: 38 passed in 0.06s
- Integrated verification after merge: `python -m pytest` from `project/` on main → 38 passed in 0.10s on `a74ea06a5fcdca236f1f220fa1219ebc98a7ca95`

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

### Emilio: patient lookup (#1)

- Member and task: Emilio; Copilot review comparison for the patient lookup part of PR #2
- Prompt/purpose and relevant issue/diff: Stage 6 Part H review prompt with issue #1 criteria and the PR diff. [Output](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5649880865)
- Summary of output:
  - Important: the PR also implements `find_practitioner` and `cancel_appointment`, outside the FR-02 scope.
  - Optional: `match='Patient not found'` tests message text that the criteria don't specify.
  - All six FR-02 criteria covered; delegation to the store and the `None` → `LookupError` mapping match the contract.
  - It could not verify that tests ran.
- Human check against actual code, requirements and tests: compared each point with the diff, the issue criteria, the section E agreement and his own branch run (38 passed, `562097f`).
- Decision: Scope concern: Modify. Message matching: Accept as Optional, no change. Coverage, responsibility and missing-evidence points: Accept.
- Reason: the scope observation is correct, but the single PR is the group's agreed plan (section E) and his review covers FR-02 only. Message matching is optional. The missing run evidence is supplied by his own test run.
- Verification/evidence: [comparison](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5649918854); branch run 38 passed in 0.08s, `562097f`

### Quang: practitioner lookup (#3)

- Member and task: Quang; Copilot review comparison for the practitioner lookup part of PR #2
- Prompt/purpose and relevant issue/diff: Stage 6 Part H review prompt with issue #3 criteria and the PR diff. [Output](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5662774349)
- Summary of output:
  - Optional: no blocking defect.
  - Important: the services rely entirely on `SmartCareDataStore` for trimming and validation, so that store contract should be confirmed.
  - Suggestions: add service-layer validation; standardise error messages.
  - Several points about cancellation, outside his issue.
- Human check against actual code, requirements and tests: read `required_text` in `domain.py` and the store's find methods to confirm trimming, blank/non-text rejection and `None` for absence. Checked his own branch run (38 passed, `562097f`).
- Decision: No blocking defect: Accept. Store dependency: Modify (valid, but resolved by reading `required_text`). Service-layer validation: Reject. Standardise messages: Reject. Cancellation points: Reject for this review. "Approve once the store contract is confirmed": Accept, since he confirmed it.
- Reason: service-layer validation would duplicate `required_text`, and the requirements don't ask for it. The messages already follow one pattern. The cancellation points belong to Brendan's review.
- Verification/evidence: [comparison](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5663264066); branch run 38 passed in 0.09s, `562097f`

### Brendan: cancellation (#4)

- Member and task: Brendan; Copilot review comparison for the cancellation part of PR #2
- Prompt/purpose and relevant issue/diff: Stage 6 Part H review prompt with issue #4 criteria (FR-06/FR-07) and the PR diff. [Output](https://github.com/BN007-CMD/st1-assignment-3/pull/2#issuecomment-6465411622)
- Summary of output:
  - Critical: no blocking issue; the service delegates to `Appointment.cancel()` and does not delete or replace.
  - Important: verify `Appointment.cancel()` is the only place state changes.
  - Important: list ordering after cancellation with several appointments is "only implied".
  - Optional: test file size and repetition.
  - Scope clean.
- Human check against actual code, requirements and tests: compared with the diff and his own branch run (38 passed, `562097f`).
- Decision: No blocking issue: Accept. Domain method is the only place state changes: Accept. List-ordering invariant: Modify (only the multi-appointment ordering needs checking).
- Reason: the domain object owns the status rules. The ordering point narrows to one case.
- Verification/evidence: [comparison](https://github.com/BN007-CMD/st1-assignment-3/pull/2#issuecomment-6465849371); branch run 38 passed in 0.09s, `562097f`
- Author follow-up checks:
  - `Appointment.cancel()` (`domain.py`, lines 129–137) raises `ValueError` before any assignment and changes only `_status`, so the "only place state changes" point holds.
  - `test_cancel_changes_only_the_requested_appointment` already asserts `list_appointments() == [first, second]` after cancelling the first of two appointments. The ordering Copilot called "only implied" is asserted directly, so that Copilot claim was inaccurate and no change was needed.

## I Human versus Copilot review comparison

Each block summarises the reviewer's own "Copilot comparison" comment on PR #2.

### Emilio: patient lookup (#1)

- Human reviewer noticed before consulting Copilot: every criterion has a matching test; identity is checked with `is`; invalid IDs raise `ValueError` separately from `LookupError`; the contract chain through `data_store.py` and `required_text` in `domain.py`; only `services.py` and `test_services.py` changed.
- Copilot noticed: the PR also contains `find_practitioner` and `cancel_appointment`, and the tests match on exact message text.
- Overlap: full criteria coverage, correct delegation and `LookupError` mapping, and the message matching.
- What did the human reviewer notice that Copilot did not: the case-sensitivity test has no unchanged-state check. He also checked the validation in the code and ran the full suite himself.
- What did Copilot identify that the human reviewer initially missed: that three issues' work is in one PR. He hadn't recorded that in his review.
- Unsupported or incorrect Copilot suggestion: none.
- Human judgement accepted, modified or rejected, and why: scope concern modified (correct, but the single PR is the agreed plan and his review covers FR-02); message matching accepted as optional with no change; coverage, responsibility and missing-evidence points accepted, with his own test run as the evidence.
- Which evidence justified merge approval: all FR-02 criteria met by the code and meaningful tests, his branch run (38 passed in 0.08s, `562097f`), and nothing blocking.

### Quang: practitioner lookup (#3)

- Human reviewer noticed before consulting Copilot: the service delegates to the store and `required_text`, which trims and raises `ValueError`; identity is checked with `is`; `ValueError` and `LookupError` are kept separate; `list_practitioners()` returns a copy, so unchanged-state checks are meaningful; the patient-ID test; no blocking issue.
- Copilot noticed: no blocking defect; reliance on the store for validation; asked for confirmation of the store contract; suggested service-layer guards and standardised error messages; raised cancellation points.
- Overlap: the service does no validation itself and depends on the store; coverage of identity, trimming, case sensitivity, unknown and invalid IDs and the patient-ID case.
- What did the human reviewer notice that Copilot did not: no explicit check that D1 is not Morgan, no unchanged-state check in the case-sensitivity test, and the error message doesn't include the missing ID.
- What did Copilot identify that the human reviewer initially missed: nothing for #3; its extra points related to cancellation (#4).
- Unsupported or incorrect Copilot suggestion: service-layer validation would duplicate `required_text` and isn't required. The cancellation points were outside this review's scope.
- Human judgement accepted, modified or rejected, and why: as in section H. The store-contract concern was resolved by reading `required_text` rather than left as a risk.
- Which evidence justified merge approval: every `find_practitioner` criterion has a test, the implementation matches the contract, and his branch run gave 38 passed in 0.09s on `562097f`. Only non-blocking suggestions remained.

### Brendan: cancellation (#4)

- Human reviewer noticed before consulting Copilot: every criterion has a test; `is` is used rather than "not None"; a valid ID with no booking raises `LookupError` while an invalid ID raises `ValueError`; the rebooking test uses a different patient for the freed slot.
- Copilot noticed: the domain method is the key authority for status changes; list ordering with several appointments is "only implied".
- Overlap: a failed cancellation must not change status, and the domain object is responsible for the status rules.
- What did the human reviewer notice that Copilot did not: whether the same patient can rebook the freed time.
- What did Copilot identify that the human reviewer initially missed: nothing major, in his assessment.
- Unsupported or incorrect Copilot suggestion: he recorded none. The author's follow-up (section H) found that the list-ordering claim was inaccurate, because `test_cancel_changes_only_the_requested_appointment` already asserts `[first, second]` after cancellation.
- Human judgement accepted, modified or rejected, and why: no-blocking-issue and domain-authority points accepted; the ordering point modified to a single check, which the existing test already covers.
- Which evidence justified merge approval: all criteria met and his branch run gave 38 passed in 0.09s on `562097f`.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.
- Member: Novica, Stage 6 lead
- Implementation: `PatientService.find_patient`, `PractitionerService.find_practitioner` and `AppointmentService.cancel_appointment` (PR #2, `562097f`)
- Testing: baseline on main 8 passed in 0.09s; `project/tests/test_services.py` (30 new test cases; 38 in the full suite); added the unchanged-state checks requested in review (`9c6a7a2`, 38 passed in 0.11s); after merge 38 passed in 0.10s on `a74ea06`
- Review: responded to all four review points on PR #2 ([comment](https://github.com/BN007-CMD/st1-assignment-3/pull/2#issuecomment-6487710885)); checked Copilot's list-ordering and domain-method claims against `domain.py` and the existing tests
- Issue refinement: wrote issues #1, #3 and #4 and their acceptance criteria; split the original combined issue into three focused issues
- Design and responsibility discussion: cancellation reuses `find_appointment` and delegates the state rule to `Appointment.cancel()`, so the service never touches `_status` or deletes records
- Debugging or integration: corrected the PR's issue links after the split; merged PR #2 after three approvals and verified the integrated main
- Documentation or team support: repository setup; Stage 6 record; root and project READMEs; reviewer instructions and Copilot prompts for the team
- Member: Emilio
- Implementation: not applicable for Stage 6 (Stage 7 lead)
- Testing: baseline on main 8 passed in 0.11s; PR branch 38 passed in 0.08s on `562097f`; recheck 38 passed in 0.05s on `9c6a7a2`; after merge 38 passed in 0.07s on `a74ea06`
- Review: reviewed patient lookup (#1) with human-first observations and the Copilot comparison ([review](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5649797680)); identified the missing unchanged-state check in the case-sensitivity test, which led to `9c6a7a2`; rechecked and re-approved
- Issue refinement: not applicable
- Design and responsibility discussion: traced the validation contract through `data_store.py` and `domain.py`; raised the single-PR grouping with the group
- Debugging or integration: verified the integrated main after merge
- Documentation or team support: not applicable
- Member: Quang
- Implementation: not applicable for Stage 6 (Stage 8 lead)
- Testing: baseline on main 8 passed in 0.09s; PR branch 38 passed in 0.09s on `562097f`; recheck 38 passed in 0.09s on `9c6a7a2`; after merge 38 passed in 0.09s on `a74ea06`
- Review: reviewed practitioner lookup (#3) with human-first observations and the Copilot comparison ([review](https://github.com/BN007-CMD/st1-assignment-3/pull/2#pullrequestreview-5662674181)); independently raised the same case-sensitivity gap; resolved Copilot's store-dependency concern by reading `required_text`; rechecked and re-approved
- Issue refinement: not applicable
- Design and responsibility discussion: rejected Copilot's service-layer validation as duplication of the store contract
- Debugging or integration: verified the integrated main after merge
- Documentation or team support: not applicable
- Member: Brendan
- Implementation: not applicable for Stage 6 (Stage 9 lead)
- Testing: baseline on main 8 passed in 0.10s; PR branch 38 passed in 0.09s on `562097f`; after merge 38 passed in 0.06s on `a74ea06`
- Review: reviewed cancellation (#4) with human-first observations and the Copilot comparison ([review](https://github.com/BN007-CMD/st1-assignment-3/pull/2#issuecomment-6465382803)); raised the same-patient rebooking question carried into Stage 7; approved
- Issue refinement: not applicable
- Design and responsibility discussion: confirmed the domain object, not the service, owns the cancellation rule
- Debugging or integration: verified the integrated main after merge
- Documentation or team support: not applicable

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?
A commit count measures how often someone saved a snapshot, not what the snapshot was worth. Our own history shows both sides of this.
- **Commits that added little:** two of our early commits on main were small README edits that reused the starter's commit message. They added to the count but tell a reader nothing about what changed.
- **Value with no commits:** Emilio's and Quang's reviews of PR #2 produced no commits of their own, yet both caught that the case-sensitivity tests didn't check for unchanged state, which led directly to commit `9c6a7a2`. Brendan's review raised a rebooking boundary we have carried into Stage 7. Writing issue criteria, checking Copilot's claims against the code and running the integrated suite on every clone don't show up as commits either.
Contribution is better judged by traceable outcomes: requirements met, tests that would catch a defect, reviews that changed the code, and integration that works for everyone.

## L Stage 6 formative questions

1. What is version control?

A system that records every committed state of a project, with who changed it, when and why. It lets a team work on the same files, compare any two versions, see exactly what changed, and recover an earlier version if something breaks. Git is the tool we use, and GitHub hosts the shared copy.

2. Why is a feature branch useful?

It isolates one focused change from main until it has been tested and reviewed, so main stays stable and runnable for everyone. Several members can work in parallel without overwriting each other, and if a change turns out wrong it can be revised or abandoned without touching the integrated code.

3. What makes a commit a good engineering commit?

It contains one coherent change (for example, a behaviour plus its tests) with no unrelated edits, leaves the project working, and has a message that says what changed and why, ideally naming the requirement. Someone reading the history later should be able to understand and, if needed, revert it on its own.

4. What is a pull request?

A request to merge a branch into main that shows the full diff alongside a description of the linked issue, the changed behaviour and the tests run. It is where review happens: reviewers comment on specific lines, request changes, and approve before the change is integrated.

5. What is the purpose of code review?

A second person checks the change against the requirement and acceptance criteria before it reaches main. They look for correctness, error handling, responsibility boundaries, weak or missing assertions and unrelated scope. Review catches defects the author is too close to see, spreads knowledge of the code across the team, and keeps a human accountable for what gets merged.

6. What does a Git diff show?

The exact lines added and removed between two versions (working tree, staging area, commits or branches), with surrounding context. It shows what actually changed rather than what the author says changed, which is why review and pre-commit checks are based on it.

7. What is a Definition of Done?

The team's shared checklist for when work counts as finished, beyond "the code is written". For us, that means the acceptance criteria are met with meaningful passing tests, the full suite has passed, a different member has reviewed the diff, feedback is resolved, documentation and the evidence record are updated, the PR is merged, and everyone has verified the integrated main.

8. What is the appropriate role of GitHub Copilot in pull-request review?

A second opinion that comes after the human reviewer's own observations. It can summarise a diff, point out risks or missing tests and suggest questions, but every claim is a candidate to check against the requirement, the actual code and a test run we observed ourselves. It can't run our tests, approve a PR, or replace another member's review, and humans stay accountable for the merge decision. In our PR, Copilot claimed list ordering after cancellation was "only implied"; checking the test showed it was already asserted.

9. Why should individual contribution not be judged only by commit count?

Commit count rewards splitting work up, not doing it well, and it misses review, testing, issue writing, design discussion, debugging, integration and mentoring, none of which produce many commits. A fair judgement looks at observable outcomes: what each person implemented or reviewed, the quality of their tests and reviews, and whether they followed through.

10. What is the Stage 6 engineering rule?

No change reaches main unless it traces from a requirement through a focused issue and branch, has meaningful tests, has been reviewed by a different team member using the actual diff (with human judgement first and Copilot only as a checked assistant), and has been verified after integration by everyone.

## M Completion and handover

- Starting SHA: `5ad6f803fe04665237f8405284bc2dddf3bd007b`
- Final Stage 6 code SHA: `a74ea06a5fcdca236f1f220fa1219ebc98a7ca95` (merge of PR #2)
- Test command: `python -m pytest`
- Working directory: `project/` (inside the repository root `st1-assignment-3`)
- Observed result: 38 passed in 0.10s (all four members got 38 passed on `a74ea06`)
- PR and another-member reviewer: PR #2 reviewed and approved by Emilio (#1), Quang (#3) and Brendan (#4); the Stage 6 evidence PR (`docs/stage06-evidence`) is reviewed by Emilio
- Unresolved issue or none: no Stage 6 defects. Carried forward:
  - Stage 7: test whether the same patient can rebook a freed practitioner slot (FR-05 boundary; there is no patient-conflict rule).
  - Stage 9: lookup error messages do not include the requested ID; the console will need to report it.
- Stage 7 handover status: ready for tutor checkpoint
- Final submitted SHA if later than tested SHA: the evidence PR merge commit that adds this record. A file cannot contain its own future commit hash, so that SHA is reported in the Stage 7 record's starting SHA and at submission. It adds only this record and the READMEs, with no executable changes, so `a74ea06` remains the verified code version.
- [x] Three Stage 6 service targets completed and checked.
- [x] Original supplied tests retained and passing.
- [x] At least two focused issues link requirements and acceptance criteria.
- [x] Feature work reviewed by another member using the actual diff.
- [x] Human-first review and required Copilot comparison recorded.
- [x] Feedback resolved and approval recorded before merge.
- [x] Everyone pulled main and integrated checks passed.
- [x] Required activities, quiz responses and contribution notes completed.
- [x] Only synthetic data included; confidential peer material kept out.
- [x] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
