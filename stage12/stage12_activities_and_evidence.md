# Stage 12 activities and evidence
BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.
Group/tutorial: Online Group 4, Tuesday 17:30 tutorial
Members and UG/PG applicability: Novica (@BN007-CMD), Emilio (@ucemilio), Quang (@quangle330), Brendan (@BrendoAC11). All UG, so the common scope applies; PG Stages 10–11 do not.
## A Release scope and starting SHA
Release label/version and requirements baseline: SmartCare v1.0 (course release). Assignment 3 revision 2 baseline: FR-01–FR-09 (FR-10 retired), QRY-01–04, FP-01–03, UI-01–02, NFR-01–06.
Common starting SHA / branch / applicable members: `b5bce81` on `main` (after the Stage 9 integration PR #13, merged as `10be97c`, then two record-only commits: moving the Stage 9 evidence into `stage09/` and editing the Stage 6 record); release branch `release/stage12`; all four members (UG).
PG starting SHA / branch / applicable members or not applicable: Not applicable (UG-only group).
Working-state review and approved integration: `git status --short` was empty on `main` at `b5bce81`. All earlier stage work arrived through reviewed PRs (#2, #5, #6, #11, #12, #13). No unmerged feature branches are in scope.
Protected common candidate and PG differences: no PG extension, so the common candidate is the release candidate. `b5bce81` is the known-good pre-release state.
Feature freeze / owner / verifier: feature freeze declared at `b5bce81`; no new features after it. Release owner: Novica. Verifier and reviewer: Quang.
## B Requirements and release readiness matrix
Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: **Do not release yet.** Passing tests only cover what the tests assert. An incomplete README means nobody else can reproduce the result. An unreviewed dependency is an unknown supply-chain and licence risk. An undocumented limitation means users are misled about what the system does. Before sign-off: complete and fresh-clone-verify the README, review the dependency (origin, version pin, licence, actual need) or remove it, and document the limitation in the README and release notes. Then rerun the full suite on the exact candidate. Our own release hit the first problem: both READMEs were stale at `b5bce81` (H1), and we fixed them before release.
Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.
| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Tests assert the same object, CANCELLED status, still found and still listed after cancel; repeated cancel rejected without change | `test_services.py::test_cancelled_appointment_is_retained_as_history`, `test_regressions.py::test_f8_02_cancelled_appointment_is_still_found`, `test_workflows.py::test_cancel_retained_history`; demo D6 | Quang | Yes | None |
| Architecture responsibilities are appropriate | Code inspection (E1); tests use services without the console (NFR-02); queries are pure (FP-01) | `smartcare/` modules; `test_queries.py::test_fp_repeat_no_mutation` | Quang | Yes for course scope | Inspection is judgement-based; no automated architecture check |
| Rescheduling is safe — PG only | Not applicable | — | — | — | UG-only group |
| AI use is responsible — common recheck / PG assurance | Human-first reviews before Copilot, with Accept/Modify/Reject decisions in stage records; final AI and dependency recheck (E) | stage06 H/I, stage08 E/F, PR #2 and PR #11 reviews | Quang | Yes, with disclosed gaps | Some early Copilot sessions weren't saved verbatim; summaries were recorded instead (E) |
| System is maintainable | Clear module responsibilities; type hints and docstrings on most public methods; 124 tests; pyflakes clean | `smartcare/`; section E | Quang | Partly | Style and docstring gaps recorded as debt (E, G); no code change at release |
| FR-01–03 register/find and validation | Domain and service tests for unique IDs, required fields, trimmed case-sensitive lookup, ValueError vs LookupError | `test_domain.py`, `test_services.py` (FR-02/FR-03 sections) | Quang | Yes | None |
| FR-04–05 booking/conflict rules | Same practitioner + exact time + SCHEDULED rejected with the store unchanged; a different practitioner is allowed; a cancelled slot is freed | `test_services.py` TEST-26–33, `test_regressions.py::test_f8_01_conflict_is_per_practitioner_at_exact_time`, `test_starter.py::test_conflict_rule_and_different_practitioner` | Quang | Yes | Same-patient rebooking of a freed slot isn't tested separately (no patient-conflict rule exists) |
| FR-06–08 cancellation/history/find | As in the cancellation row, plus COMPLETED rejection and unknown/invalid ID handling | `test_services.py` cancellation section | Quang | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | Practitioner isolation, default all statuses, each status filter, empty vs unknown vs invalid, date-then-ID ordering, fresh lists, no mutation | `test_queries.py` (10), `test_workflows.py::test_qry04_*`, `test_qry01_service_isolation` | Quang | Yes | None |
| UI full console sequence and error recovery | Integrated menu sequence and invalid-input recovery; release demo | `test_workflows.py::test_ui01_sequence`, `test_rejection_no_partial_state`, `test_console.py`, `stage09/stage09_evidence/ui01_transcript.txt`, `ui02_transcript.txt`; demo D | Quang | Yes | None |
| Session-only scope / FR-10 retired | No persistence code; the exit message says session data is discarded | `console.py`, `data_store.py`; demo D11 | Quang | Yes | Accepted scope limit (G) |
| PG RES and assurance integration | Not applicable | — | — | — | UG-only group |
## C Full regression results
| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.14.7, pytest 8.3.5 | `project/`, `python -m pytest -q` | `b5bce81` + release docs (branch `release/stage12`, [BRANCH SHA]) | 124 passed in 0.24s | release PR |
| Complete PG if applicable | — | — | — | Not applicable (UG) | — |
| Affected focused checks after correction | — | — | — | Not applicable: no code changed in Stage 12 (H2 no-change decision) | — |
| Full integrated recheck | Python 3.14.7, pytest 8.3.5 | `project/`, `python -m pytest -q` | 74246fae45a379b72a59c8427207cfccd63c8e86  | 124 passed in 0.15s | section K |
Prior assertions preserved / reviewed test diff: no test file was changed in Stage 12. `git diff b5bce81 -- project/tests` is empty, and the count stays at 124.
Remaining failure / limitation: none.
## D Console and end to end demonstration
Run from a fresh process: `cd project` then `python main.py --interactive`. All data is synthetic.
| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | Clinic front-desk staff manage practitioner schedules; patients and practitioners are affected by double-booking or lost history | Problem statement | Explained | — |
| Register and find Patient and two Practitioners | 1 P1 "Alex"; 3 DR1 "Taylor" "General"; 3 DR2 "Morgan" "Physio"; 2 P1; 4 DR1; 2 P404 | FR-01–03, UI-02 | All registered; "P1: Alex"; "DR1: Taylor, General"; P404 gave "Error: Patient not found" and the menu returned | terminal transcript |
| Valid booking | 5 A1 P1 DR1 2026-12-01 09:00 | FR-04, AC-03.1 | "Appointment booked." | terminal transcript |
| Same practitioner exact-time conflict rejected | 5 A2 P1 DR1 2026-12-01 09:00, then 7 A2 | FR-05, AC-04.1, NFR-01 | "Error: Practitioner already has a SCHEDULED appointment at this time"; 7 A2 gave "Error: Appointment not found", so no partial appointment was created | terminal transcript |
| Different practitioner same time allowed | 5 A3 P1 DR2 2026-12-01 09:00 | AC-04.2 | "Appointment booked." | terminal transcript |
| Cancel SCHEDULED and retain/find CANCELLED object | 6 A1; 7 A1 | FR-06/07/08, AC-05.1/05.2 | "Appointment cancelled."; then "A1: P1 with DR1, 2026-12-01 09:00, cancelled" (same ID, participants and time) | terminal transcript |
| Invalid/repeated cancellation rejected | 6 A1 again; 6 A404 | AC-05.3 | "Error: Only SCHEDULED appointments may be cancelled"; "Error: Appointment not found" | terminal transcript |
| Default all-status listing | Fresh session: 1 P1; 3 DR1; 5 A1 P1 DR1 2026-12-01 09:00; 6 A1; 8 DR1 with a blank status | FR-09, QRY-02 | "A1: P1 with DR1, 2026-12-01 09:00, cancelled". The default listing includes CANCELLED appointments, whereas the earlier `scheduled` filter excluded A1. In the same run, a date typed with a trailing space was rejected with "Error: Use date/time format YYYY-MM-DD HH:MM" (strict parser) and stray menu input gave "Unknown choice; enter 0-8.", both followed by continued operation. Typing "All" at the status prompt was rejected with "Status must be blank, scheduled, cancelled or completed". Multi-appointment ordering is shown by the `scheduled` listing and asserted in `test_queries.py::test_qry03_tie_break` and `test_workflows.py::test_qry02_service_default_all`. | terminal transcripts |
| Explicit filtering / empty vs unknown / deterministic order | 8 DR1 scheduled; 8 DR2 cancelled; 8 DR9 | QRY-02/04 | "A4: P1 with DR1, 2026-12-01 08:00, scheduled" only (cancelled A1 excluded); DR2 cancelled gave "No appointments found." (known, empty); DR9 gave "Error: Practitioner not found" (unknown) | Equal-time ID tie: `test_queries.py::test_qry03_tie_break` |
| Invalid date/status/menu/lookup recovery and continued operation | 9; 5 A5 P1 DR1 2026-13-40 25:00; 8 DR1 bogus; then 2 P1 | UI-02 | "Unknown choice; enter 0-8."; "Error: Invalid calendar date/time; use YYYY-MM-DD HH:MM"; "Error: Status must be blank, scheduled, cancelled or completed"; then "P1: Alex", so the session continued with its data intact | terminal transcript |
| Session-only limitation and normal exit | 0 | FR-10 retired | "Session data discarded." Data is held only in memory for this process; there is no restart storage. | terminal transcript |
| One meaningful requirement-linked pytest test explained | `python -m pytest -q tests/test_regressions.py::test_f8_02_cancelled_appointment_is_still_found` | FR-07, AC-05.2/05.3 | 1 passed in 0.01s. It asserts identity (`is`) for both store and service lookup after cancelling, and a rejected repeat cancel. It does not prove behaviour across sessions or under concurrency. | `tests/test_regressions.py` |
| Architecture and one actual AI decision / known limitation | Module walk-through (F); Stage 8 F8-02 Copilot suggestion 2 | NFR-03 | Copilot's "service maps None to LookupError" was modified: a real mechanism, but downstream of the store filter, so it was rejected as the repair location. Limitation: session-only data. | stage08 F |
| PG reschedule identity/participants/time and no-op | — | — | Not applicable (UG) | — |
| PG conflict/invalid status/failure non-mutation | — | — | Not applicable (UG) | — |
| PG old slot / current lookup/list ordering / assurance risks | — | — | Not applicable (UG) | — |
Stable demo owner / fresh process / command: Novica; new terminal; `cd project`, `python main.py --interactive`. No AI or internet needed.
PG demonstrations through service/tests or not applicable: not applicable (UG-only group).
## E Final code quality and AI review
| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | `domain.py` (entities, `cancel()`), `data_store.py` (session collections), `services.py` (use cases), `queries.py` (pure functions), `console.py` (I/O) | No finding. State rules stay in `Appointment`; services use only the store's public API; queries take explicit inputs and return new lists. | No change |
| PascalCase and snake_case naming | all modules | No finding | No change |
| Useful type hints and meaningful docstrings | `data_store.py` | `find_appointment` and `has_practitioner_conflict` have no docstrings; they were removed when the Stage 8 faults were injected and not restored by the repairs | No change at release (H2); recorded as debt (G). Behaviour is unaffected. |
| Four-space indentation and imports/layout | `console.py`, `services.py`, `queries.py`, `data_store.py`, `main.py` | Four-space indentation and clean imports throughout. `pycodestyle` reports 11 cosmetic issues in production code (long lines, missing blank lines, whitespace on blank lines). | No change at release: cosmetic only, and the handout says a correct project needs no cosmetic rewrite (H2). Recorded as debt (G). |
| Focused methods / duplication / dead or commented code | `data_store.find_appointment`; `main.py` | `find_appointment` re-implements `required_text` by hand with a linear scan (a Stage 8 preparation leftover, same error message and behaviour). `main.py` still catches `NotImplementedError` from the starter, which can no longer occur. | No change at release: both are behaviour-neutral, and changing code now would need re-verification for no functional gain (H2). Recorded as debt (G). |
| Globals / leakage / unnecessary inheritance or frameworks | all modules | No finding: no globals, no inheritance beyond `Enum`, no frameworks | No change |
| No SQLite/persistence/repository ABCs/speculative features | all modules | No finding | No change |
| Synthetic data / secrets / dependencies / provenance | `git ls-files`; `requirements-dev.txt` | Only synthetic "Example" names. No secrets, `.env` or credentials. Single dependency `pytest==8.3.5`, pinned, from PyPI, MIT licence, test-only. No Stage 8 utility or `.stage8_faults/` files tracked (`.gitignore`). | No change |
| Significant common Copilot contributions and human verification | stage06 H/I (PR #2), stage07, stage08 E/F (PR #11), stage09 | Copilot was used for review comparisons and debugging suggestions after human-first observations, each with a recorded decision.| Rechecked: every merged change was reviewed by another member and is covered by tests |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | — | Not applicable (UG) | — |
| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Copilot (Stage 6): list ordering after cancellation is "only implied" by the tests | FR-07; `test_cancel_changes_only_the_requested_appointment` | Read the test: it asserts `list_appointments() == [first, second]` | Reject: ordering is asserted directly | No change |
| Copilot (Stage 6): add service-layer ID validation | FR-02/03; `services.py` | Read `required_text` in the store path | Reject: it would duplicate validation, and no requirement asks for it | No change |
| Copilot (Stage 8, F8-01): the service passes the wrong practitioner ID | FR-05; `services.py` | Traceback showed `'D2'` passed; `services.py` unchanged by the fault injection; calling the store directly still gave inverted results | Reject: contradicted by evidence | Repaired in the store instead (`2ef8a3a`) |
| Copilot (Stage 8, F8-02): the service's None → LookupError mapping causes the failure | FR-07/08; `services.py` | Runtime check: the object is still listed with status CANCELLED, while the store lookup returns None | Modify: the mechanism is real but downstream of the store filter, so it is not the repair location | Repaired in the store (`afb89ad`) |
| FR-02/03/06/07; `services.py`, `test_services.py` | Author read every line; fail-first and full-suite runs; three member reviews | Accept with modification: reviewers' unchanged-state request added (`9c6a7a2`) | Merged in PR #2 |
Access route or approved equivalent / limitations: GitHub Copilot Chat on members' own authorised accounts; no agent mode was used (UG).
Available AI evidence and missing evidence honestly disclosed: Copilot outputs and comparisons are saved as PR comments (PR #2, PR #7/#11). Some Stage 7 and 9 Copilot sessions are summarised in their stage records rather than saved verbatim.
## F README and reproducibility check
| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | `project/README.md`, top and "Included capabilities" | Quang | Matched on fresh clone; no gap |
| Out-of-scope capabilities and known limitations | `project/README.md` "Out of scope", "Known limitations" | Quang | Matched on fresh clone; no gap |
| Confirmed teaching Python version and dependency installation | `project/README.md` "Environment" | Quang | Matched on fresh clone; no gap |
| Working directory / demo / interactive / test commands | `project/README.md` "Run and test" | Quang | Matched on fresh clone; no gap |
| Repository structure and architecture responsibilities | `project/README.md` "Structure and responsibilities" | Quang | Matched on fresh clone; no gap |
| Responsible AI summary / synthetic-data rule | `project/README.md` "AI use" and top | Quang | Matched on fresh clone; no gap|
| Release label/version and SHA links | root `README.md` group index; this record K | Quang | Matched on fresh clone; no gap |
Root README index and project/README verified: both were stale at `b5bce81` (H1) and were rewritten in the release PR. Quang checked them against the running application.
Fresh clone or extracted ZIP / candidate identity: Quang: fresh `git clone` of https://github.com/BN007-CMD/st1-assignment-3 at SHA b0452522aea4ca75bc26c4218c99f5534fce75c8
Verifier and clean environment / actual version: Quang, Windows 11, Python 3.15.2, new virtual environment
Setup/run/test commands and observed results: `cd project`; `python -m pip install -r requirements-dev.txt` →; `python main.py` → ; `python main.py --interactive` then `0` → ; `python -m pytest -q` 
Missing local file or setup gap / remedy and recheck: Quang: none found 
## G Known limitations debt and release notes
Delivered features: register and find patients and practitioners; book appointments with exact-time practitioner conflict rejection; cancel with retained, findable history; practitioner listing with status filter and deterministic ordering through a pure query; interactive console with error recovery. All are session-only, in one shared store.
Important fixes: F8-01, the practitioner conflict check was inverted (`2ef8a3a`); F8-02, cancelled appointments couldn't be found (`afb89ad`); Stage 9, missing `AppointmentStatus` import in `console.py` (`3641739`); Stage 12, stale READMEs corrected (H1).
Architecture/quality improvements: Stage 8 replaced the status string with the `AppointmentStatus` enum (`3a1b426`). Stage 12 made no code changes; the quality findings are recorded as debt below.
Known limitations: session-only data; naive local minute-precision times; single operator, with no authentication or concurrency control; lookup errors don't name the missing ID; console only.
AI-assisted development note: GitHub Copilot was used for review comparisons and debugging suggestions, always after a human's own observations, with recorded Accept/Modify/Reject decisions. Stage 6 had review by Claude due to user programming issues. No AI output was merged without a member's review and passing tests.
| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| PEP 8 issues in test files (long lines, blank lines, missing final newlines) | Readability only; no behaviour impact | Low | Reformat the tests in a separate reviewed change, with no assertion edits | Yes: reformatting tests at release risks unreviewed test edits |
| Production code style and docstrings: 11 cosmetic PEP 8 issues, two missing data store docstrings, `find_appointment` duplicating `required_text`, a dead `NotImplementedError` handler in `main.py` | Readability and maintainability only; behaviour identical | Low | Restore `self._appointments.get(required_text(...))` and the docstrings, remove the dead handler, reformat; rerun the full suite | Yes: behaviour-neutral, not a release blocker |
| Lookup error messages don't include the requested ID | Staff see "Patient not found" without the ID they typed | Low | Include the ID in the service messages and update the `match=` tests | Yes: the revision 2 contract fixes exception types, not messages |
| Same-patient rebooking of a freed slot isn't tested on its own | Small gap in boundary coverage | Low | Add one FR-05 boundary test | Yes: behaviour follows from the practitioner-only rule, which is already tested |
| Commit-message quality is uneven early on (typos, reused starter message) | History is harder to read | Low | Follow the section E commit convention | Yes: history isn't rewritten (handout rule) |
Session-only synthetic data and minute-precision local time: records exist only for one process run (FR-10 retired). Times are naive local `datetime` at minute precision, entered as `YYYY-MM-DD HH:MM`. Data is synthetic only (NFR-06).
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: none implemented; deliberately out of scope for this course release.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: single user and in-memory; no timezone handling, logging, monitoring or deployment; no usability or accessibility evaluation was done.
Difference between accepted scope limit and unresolved required behaviour: everything in this section is either outside the revision 2 baseline or a low-priority quality item. No current requirement is unmet; all FR/QRY/FP/UI rows in B are covered by passing tests.
PG assurance residual risks / owner / status or not applicable: not applicable (UG).
## H Release findings and corrective action
| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| H1: README accuracy (Stage 12 section 5) | At `b5bce81`, `project/README.md` said "Stage 8 complete" and that the Stage 9 functions "still raise NotImplementedError"; the root README said the starter "deliberately leaves the three Stage 6 tasks incomplete" and gave 111 passed (actual 124) | Release blocker: the instructions misdescribe the release | Novica: rewrite both READMEs for v1.0 | release PR: `README.md`, `project/README.md` | Commands in the README run as written (F) | None |
| H2: Code quality (Stage 12 section 4) | `pycodestyle` reports 11 cosmetic production-code issues; two data store methods lack docstrings; `find_appointment` duplicates `required_text`; `main.py` has a dead handler | Low: no behavioural or requirement impact | Novica: justified no change at release | None | 124 passed unchanged at `b5bce81`; pyflakes clean | Recorded as technical debt (G) |
Justified no-change conclusion if no defect found: no functional defect was found. All 124 tests passed at `b5bce81` and every B row is covered.
Release blockers still open / status: none after H1 (READMEs) is merged.
## I Git review and integration evidence
Issue / PR / diff links and reviewed SHA: release PR [#__ LINK], branch `release/stage12`, reviewed SHA [SHA]
Independent reviewer / feedback / response: Quang; approved without changes after a fresh-clone check (124 passed in 0.19s on 'b0452522') https://github.com/BN007-CMD/st1-assignment-3/pull/14#pullrequestreview-5822511483 
Integration commit / full recheck: 74246fae45a379b72a59c8427207cfccd63c8e86 ; `python -m pytest -q` from `project/` → 124 passed in 0.15s
Tracked and untracked file inspection / cleanliness: `git ls-files` lists only `.gitignore`, both READMEs, `project/` source and tests, `requirements-dev.txt`, the stage records, the Stage 7 screenshots and `stage09/stage09_evidence/` transcripts. `git status --short` was empty before the release branch.
Secrets/staff material/caches/tool-metadata exclusion check: no `.env`, credentials, `__pycache__`, `.venv`, `.pytest_cache`, Stage 8 utility or `.stage8_faults/` files are tracked; `.gitignore` covers them.
Candidate recovery plan / known-good SHA: known-good pre-release `b5bce81`; Stage 9 integration `10be97c`; release merge 74246fae45a379b72a59c8427207cfccd63c8e86 . Any of them can be restored with `git switch --detach <SHA>`. History is never rewritten.
Named substantive contributions: Stage 6 lead Novica (PR #2); Stage 7 lead Emilio (PR #6); Stage 8 lead Quang (PR #11, #12); Stage 9 integration (PR #13, reviewed by Quang); Stage 12 release Novica (this PR), reviewed by Quang. Each stage record lists review roles.
## J Human release decision
Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: **READY WITH DOCUMENTED LIMITATIONS**
Approver / date / rationale and evidence: Novica, release owner, 9/11/2026, with Quang as independent reviewer. All revision 2 common requirements are traced to passing tests (B), the full suite passes on the merged candidate (C), the demo sequence works from a fresh process (D), the README was reproduced from a fresh clone (F), the README blocker is corrected and the code-quality finding is a justified no-change recorded as debt (H).
What risks remain / conditions / owners: the session-only, single-user and naive-time limits and the low-priority debt in G. These are accepted for a course release, not production. Owner: the group. Condition: no production or clinical use.
Can the team explain the system: yes. Each member led one stage and reviewed others (I), and section N lists the explanation points.
Can a change be recovered: yes, through the known-good SHAs in I.
Common decision / PG decision where different: common only (UG).
## K Final tested release SHA
Exact common tested SHA: 74246fae45a379b72a59c8427207cfccd63c8e86  (full suite 124 passed in 0.15s on 74246fa by Novica and Quang). This replaces the earlier draft value `32fde1d`, which predated the release corrections.
Exact PG tested SHA or not applicable: not applicable (UG)
Final submitted SHA / repository URL: https://github.com/BN007-CMD/st1-assignment-3. The submitted SHA is the commit that adds this completed record; a file can't contain its own future SHA, so it's given in the submission form.
Evidence-only later commit and difference explanation: if the record's final values are added in a later commit, that commit changes only `stage12/stage12_activities_and_evidence.md` (no executable changes), so the tested code SHA above still stands.
Executable changes after testing and re-verification: none after the tested SHA.
Source ZIP name / SHA correspondence / extracted comparison: `SmartCare-release.zip` from `git archive --format=zip --output=../SmartCare-release.zip <SUBMITTED SHA>`. Extracted and checked: root has `README.md`, `.gitignore`, `project/` and the stage folders; `python -m pytest -q` in the extracted `project/` → [RESULT].
## L Submission package verification
- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, cindividual peer forms routed separately.
Confirmed assessment item/upload route: Canvas
Deadline/timezone: 23:59 9/11/2026 AEST
Repository access arrangement: public repository, https://github.com/BN007-CMD/st1-assignment-3
Mixed-candidate upload arrangement: not applicable (UG-only group, one candidate)
Oral/video recording/accessibility arrangements: Nil
Remaining administration or release dependency: group reflection, peer forms and team reports are submitted through cadmus.
## M Formative questions
1. What is a release candidate? A specific, frozen version of the software, identified by an exact commit SHA, that the team proposes to release once it passes final verification. If verification finds a blocker, the fix produces a new candidate rather than quietly changing the old one.
2. What is feature freeze and why is it used? A point after which no new features are added; only release blockers are fixed. It stops the target moving, so testing, documentation and review describe the version that actually ships.
3. What is regression testing in a release context? Rerunning the whole accumulated test suite on the exact candidate to show that earlier behaviour still works after the final changes. Ours went from 8 starter tests to 124, and every one is rerun on the release SHA.
4. What is a known limitation? Something the release deliberately doesn't do, or does only within stated bounds, documented so users aren't misled. SmartCare's data lasting only for one session is an example. It's different from a defect, which breaks a stated requirement.
5. What is technical debt? A shortcut or imperfection accepted now that makes future change harder or riskier, such as our test-file style issues. Debt is recorded with its impact and a planned action so it's managed rather than forgotten.
6. What are release notes? A short account, written for users and maintainers, of what the release delivers, what was fixed or improved, its known limitations and how AI was used.
7. What is software maintenance? All the work after release: fixing defects, adapting to new environments or requirements, improving quality and keeping the documentation true. Each change gets the same review and testing discipline as development.
8. What is the purpose of the individual demonstration/viva? To show that each member understands and can explain the system and their own contribution (requirements, design, tests, a defect, AI decisions), so marks reflect real understanding rather than a repository alone.
9. What should the final responsible-AI check establish before release? That every significant AI contribution is understood by a human, traceable, verified by tests or inspection and honestly recorded; that no secrets, real data or unreviewed dependencies came in through AI; and that humans, not the AI, made the release decision.
10. What is the main course conclusion about AI and the role of the software engineer? AI can produce plausible code and diagnoses quickly, but it can't own requirements, judge evidence or take responsibility. In this project it proposed wrong causes and an unsupported ordering claim that only human checks caught. The engineer's role shifts towards specifying, verifying, reviewing and being accountable for what is released.
## N Reflection viva and handover
Strongest evidence SmartCare is ready: 124 requirement-linked tests passing on the exact release SHA; regression tests that failed before the Stage 8 repairs and pass after; a fresh-clone reproduction by another member.
Weakest area: AI evidence from Stages 7 and 9 is summarised rather than saved verbatim, and test-file style is uneven. Neither affects behaviour, but both make the history harder to audit.
How AI use changed from Stage 1 to Stage 12: we moved from accepting AI output as a starting point to treating every suggestion as a hypothesis. In Stage 6 we recorded human observations before Copilot; by Stage 8 we were ranking Copilot's causes against runtime evidence and rejecting two of them. Our Stage 1 answer isn't available to quote, so we don't compare against it directly.
Start doing engineering and AI use: commit the team agreement and refactor plans before the work they govern; save AI prompts and outputs in the PR as they happen.
Stop doing engineering and AI use: committing directly to `main`; letting tool-generated or AI-generated formatting go unreviewed for style.
Continue doing engineering and AI use: one focused issue and branch per change; a different member reviewing every PR; human-first review before Copilot; regression tests that fail before a fix.
What worked / caused rework / future delivery improvement: Worked: rotating stage leads with assigned reviewers, and fail-first regression tests. Caused rework: one combined issue that had to be split (Stage 6), records filled after the fact (Stage 6 E, Stage 8 H), and stale READMEs found only at release. Improvement: update the READMEs and record sections in the same PR as each change.
One paragraph If AI can write code why do we still need software engineers: Because writing code was never the hard part to trust. In SmartCare, Copilot produced confident but wrong causes for both Stage 8 defects and claimed something "was only implied" when a test asserted it directly. Only a person who knew the requirement, ran the code and checked the evidence could tell. Engineers decide what the system must do, design how responsibilities fit together, judge whether evidence actually proves anything, and stay accountable for what is released to people who depend on it. AI speeds up producing candidates; engineers decide which candidates are true.
| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | Clinic staff need reliable booking without double-booking a practitioner, and an audit of cancellations; patients and practitioners rely on it |
| Two requirements and acceptance criteria | FR-05 (AC-04.1 reject same practitioner + exact time + SCHEDULED; AC-04.2 allow a different practitioner); FR-07 (AC-05.2 cancelled appointment retained and findable) |
| Domain model and architecture | `Patient`, `Practitioner`, `Appointment` + `AppointmentStatus`; one `SmartCareDataStore`; three services; pure `queries`; `console`; see `project/README.md` |
| Design trade-off | Pure `select_appointments` over explicit lists (testable, no hidden state) vs a store method (one fewer call); we chose purity (FP-01) |
| Meaningful test and its limits / 100 percent coverage | `test_f8_02_cancelled_appointment_is_still_found` proves identity and retention in one session. It doesn't prove other sessions, concurrency or usability; 100% coverage only shows lines ran, not that the assertions are right |
| Diagnosed defect and verification | F8-01: inverted `!=` in the conflict check, found by calling the store directly; fixed in `2ef8a3a`; the regression test failed before and passed after |
| Shared store and session-state/query responsibilities | All services share one store so a booking is visible to lookups and conflict checks immediately; queries only read the lists they're given |
| What would break if session-state lookup/query responsibilities changed? | Separate stores per service would miss conflicts and lose cancelled history from lookup; a query that reads the store or sorts in place would break FP-01/02 and the no-mutation tests |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Only `Appointment` knows its own legal transitions, so `cancel()` guards them. A conflict involves many appointments, so the service asks the shared store |
| FR-07 retained history test | `test_services.py::test_cancelled_appointment_is_retained_as_history` |
| Actual AI change rejected/modified or honestly accepted with verification | Stage 8 F8-02: Copilot's "service mapping" cause modified to a downstream effect after the runtime check (stage08 F) |
| Unresolved limitation / future production work | Session-only data. Production would need durable storage, authentication and roles, timezone policy and concurrency control |
| Personal implementation contribution | Novica: Stage 6 lead. Implemented PatientService.find_patient, PractitionerService.find_practitioner and AppointmentService.cancel_appointment with 30 service tests (PR #2, 562097f), then added the unchanged-state checks the reviewers requested (9c6a7a2). Emilio led Stage 7 (PR #6), Quang led Stage 8 (PR #11) and Stage 9 was integrated in PR #13; each member explains their own stage in the team viva. |
| Personal test/review/design/integration contribution | Novica: wrote issues #1, #3 and #4 and split the original combined issue; responded to all Stage 6 review points; reviewed the Stage 8 refactor (#10 in PR #11), requested the missing section H and approved after it was added; merged PRs #2, #5 and #6; Stage 12 release owner: rewrote both READMEs, ran the release regression and demo, and opened PR #14.|
| PG agentic change and rescheduling verification | Not applicable (UG) |
| PG responsible-AI risk/remediation or supported no finding | Not applicable (UG) |
Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.
Practice question/change and reasoning: not undertaken
Separate reflection / peer / common team viva evidence links and routing: submitted separately through Canvas/Cadmus; not stored in Git.
No further coding stage. Later corrections use the published assessment process.