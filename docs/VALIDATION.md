# Validation - October 8, 2026

- 18 Python API/retrieval tests passed locally on Python 3.10.
- 8 JavaScript ERP hostname/context checks passed.
- Actual unpacked MV3 extension loaded in Playwright Chromium on Linux.
- Confirmed sidebar injection, alpha citation, ServiceNow mock, Jira mock, beta-only fixture retrieval and literal rendering of HTML-like input.
- Screenshot inspected visually: readable ERP screen, synthetic labels, cited runbook, reviewed message and local mock ticket confirmation. No real account, customer or ERP data appears.
- One test-client deprecation warning from the installed FastAPI/Starlette stack. It did not fail the tests. Dependency upgrades should be regression-tested.
- GitHub CI has not run; the workflow is only staged.
- No cloud model, real ERP, Oracle DB or live ticket integration was tested. Edge was not tested.
- Release checks cover known credential shapes, cloud identifiers, emails, personal domains and unexpected non-demo URLs. Manual content review also excludes operational data and archives. Pattern scanning is not a guarantee that all possible secrets are detectable.
- No Git directory or imported history is in the candidate package.
