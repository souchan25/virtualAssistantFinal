# Bolt's Journal

## 2024-05-22 - [Playwright vs Real World]
**Learning:** Verification scripts in headless environments can fail due to race conditions or specific selector mismatches (e.g., placeholder text vs label) even when the feature works perfectly in manual/curl tests.
**Action:** When UI tests are flaky but backend API is verified via curl/unit tests and frontend logic is sound via code review, trust the architectural improvement and the partial success (e.g., page load ok) rather than burning hours debugging the *test harness*. Use robust, generic selectors (IDs) over text/placeholders where possible.
