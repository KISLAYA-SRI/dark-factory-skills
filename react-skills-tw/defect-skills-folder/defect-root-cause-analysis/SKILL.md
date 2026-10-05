---
name: defect-root-cause-analysis
description: Use as Phase 3 of the FE Defect Fix workflow to find the root cause by tracing the exact code path the reported trigger executes, filtering out context and comments that are not on that path, and proving the mechanism explains the observed symptom before classifying fault origin, blast radius and the edge-case matrix. Runs once per issue. Triggers include root cause analysis, RCA, locate defect, diagnose issue.
disable-model-invocation: true
---

## Defect Root Cause Analysis — Symptom-Anchored

A root cause is **the mechanism that turns the TRIGGER into the OBSERVED result.** Anything that does not do that is not the root cause — however relevant it looks.

```text
TRIGGER  ──►  code path actually executed  ──►  OBSERVED
                         ▲
              the root cause lives here, and only here
```

⚠️ No fix, no tests in this phase.

---

## ⚠️ RELEVANCE FILTER — READ BEFORE OPENING ANY FILE

The code base and the documents are full of things that look related. They are noise unless they pass this filter.

| You see | Treat as |
| --- | --- |
| A comment, JSDoc, TODO or ticket tag (`[TAW-486 / …]`, `TAW-229:`) | **Noise.** Comments describe intent and history, not behaviour. Read the code under it. |
| Code that runs at a **different time** than the trigger (on mount, on resend, on another screen) | **Out of scope** — it cannot cause what happens *after* the trigger |
| A function with a similar name or the same keyword (`toast`, `error`) not called on the trigger path | **Out of scope** |
| A document claim ("AC-11 COVERED", "error mapping implemented") | **Unverified.** The document is the map, not proof |
| A prior fix in the same file | Relevant **only if** its lines are on the trigger path |
| Code on the trigger path that shapes OBSERVED | **In scope — this is where you look** |

⚠️ **Keyword matching is not diagnosis.** "Ticket mentions a message, code has a toast comment" is how the wrong file gets fixed. Only the executed path counts.

---

## STEP 1 — Trace the trigger path, file by file

Start at the **trigger entry** from Phase 2. Follow the path the trigger actually executes, **opening every file on it**, until you reach the point where OBSERVED is produced.

```text
TRACE — ISSUE-001  (TRIGGER: incorrect OTP → Verify)
  1. OtpVerificationContainer.tsx → handleVerify()           opened ✓
       calls verifyOtpWithCallbacks(payload, { onErrorToast, … })
  2. Hooks/useOtpVerify.ts → verifyOtpWithCallbacks()        opened ✓
       onError: reads error.code … does it call onErrorToast for BE_OTP_INVALID?
  3. SitecoreHelpers → resolveToastFromErrorCode()           opened ✓
       matches ApiCode … what if no entry matches?
  4. OtpVerificationView.tsx → Toast render                  opened ✓
       renders only when isShowToast …
  → OBSERVED is produced at step N because …
```

Rules:
- **Follow calls and callbacks, not file names.** If a handler moved to a hook, follow it into the hook.
- **Open every hop.** A hop you did not open is a guess.
- **Use the SIGNALS.** Search for the ticket's concrete identifiers (error code, API, field) on the path: `grep -rn "BE_OTP_INVALID" <feature dir>`.
- **Stop at the first point where behaviour diverges from EXPECTED.** That is the candidate.
- Line numbers drift — find symbols **by name**.

---

## STEP 2 — The Symptom-Fit Test (mandatory)

Before accepting a candidate, answer all four. Any **no** → reject and keep tracing.

```text
1. Is the candidate code EXECUTED when TRIGGER happens?               yes / no
2. Does it, by itself, produce OBSERVED (quote the ticket)?           yes / no
3. Would changing it produce EXPECTED (quote the ticket / AC)?        yes / no
4. Does it explain every SIGNAL? (e.g. why BE_OTP_INVALID arrives
   yet nothing renders)                                               yes / no
```

```text
❌ "Toast shown on initial mount"   → runs on MOUNT, trigger is VERIFY CLICK → fails Q1. Reject.
✅ "useOtpVerify.onError does not call onErrorToast for BE_OTP_INVALID"
                                    → runs on verify error · produces "no message" · fix shows it · explains code. Accept.
```

⚠️ EXPECTED comes from the ticket or an AC — **quote it**. Never derive it from code, comments, or the code-gen document.

If no candidate passes after tracing the full path: record `BLOCKED — cause not located on trigger path`, list the hops traced, and continue the run. A blocked issue is better than a wrong fix.

---

## STEP 3 — Fault origin

Use git **only on the root-cause lines**:

```bash
git log -L :<symbol>:<file> --format="%h %ad %an %s" --date=short
```

| Origin | When | Learning? |
| --- | --- | --- |
| Agent miss | Lines are as generated; agent had what it needed | ✅ |
| Regression from prior fix | A later defect-fix commit changed these lines and broke them | ✅ |
| Post-generation manual change | A developer commit changed these lines | ❌ |
| Upstream gap · Contract change · Design change · Ambiguous | As named | ❌ |
| Unknown | No git history available | ❌ (record, don't guess) |

⚠️ Classify from **the root-cause lines**, not from the file or from comments elsewhere in it.

---

## STEP 4 — Blast radius, with test files

Consumers of the code you will change, and the test files that cover them. Name files.

```bash
grep -rl --include=*.ts --include=*.tsx "<symbol>" Portals/ Packages/
```

A consumer with no test is a gap — record it.

---

## STEP 5 — Edge-case matrix

Change narrowly, verify widely. Cases flowing through the lines you will change:

| Dimension | Check |
| --- | --- |
| Data | null · undefined · "" · unknown code · code with no CMS message |
| Branches | both sides — especially the path already working (other error codes, success) |
| Locale | en and ar |
| State | into / out of the changed state (error → retry → success) |
| Consumers | each blast-radius consumer |
| Existing behaviour on the path | must be preserved unless EXPECTED says otherwise |

Only the REGRESSION row must fail first; GUARD and BLAST rows protect working behaviour.

---

## STEP 6 — Test plan

```text
TEST PLAN — ISSUE-001
  Regression (must FAIL first): reproduces TRIGGER exactly, asserts EXPECTED
      e.g. mock verify error { code: BE_OTP_INVALID } → click Verify → expect message visible
  Guards (must PASS):           other error codes · success path · missing CMS message
  Blast (must PASS):            co-located tests + --related on changed files
```

⚠️ The regression test must exercise **the TRIGGER**, not a neighbouring behaviour. A test of mount behaviour cannot prove a verify-click bug.

---

## Output — one block per issue

```text
RCA — ISSUE-001 · DIAGNOSED
  Trigger:   incorrect OTP → Verify
  Trace:     handleVerify → useOtpVerify.onError → resolveToastFromErrorCode → View.Toast
  Cause:     Hooks/useOtpVerify.ts → onError  — BE_OTP_INVALID branch sets error state
             but never calls onErrorToast, so no message renders
  Fit:       executed ✓ · produces OBSERVED ✓ · fix gives EXPECTED ✓ · explains signals ✓
  Expected:  "display an appropriate error message returned by the API" (ticket)
  Origin:    agent miss (lines as generated, git a1b2c3)
  Blast:     OtpVerificationContainer.test.tsx · useOtpVerify.test.ts
  Plan:      [test plan]
```

### Gate (per issue)
```text
- [ ] Trigger path traced from entry to where OBSERVED is produced; every hop opened
- [ ] Comments, tags, and off-path code ignored
- [ ] Symptom-fit test: all four YES — or issue BLOCKED with hops listed
- [ ] EXPECTED quoted from ticket / AC
- [ ] Origin classified from the root-cause lines
- [ ] Blast radius with test files; edge-case matrix; test plan exercises the TRIGGER
- [ ] No source modified; no test written
```

### Never
- **Never pick a cause because a comment, tag, or document mentions similar words.**
- **Never accept a cause that runs at a different time than the trigger.**
- **Never skip a hop** — if a handler delegates, open the delegate.
- **Never take EXPECTED from code, comments, or the code-gen document.**
- Never revert a developer's change to match a document.
- Never modify source or write tests here.
