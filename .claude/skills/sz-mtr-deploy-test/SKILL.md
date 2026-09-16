---
name: sz-mtr-deploy-test
description: Deploy or verify the main branch in the SZ-MTR test environment through GitLab CI/CD. Use when the user asks to push main, deploy test, run CI/CD to test, check the test environment, or provide a browser-accessible test URL.
---

# SZ-MTR Deploy Test

## Workflow

1. Read `docs/release-and-cicd.md` and any private bootstrap env path provided by the user.
2. Confirm the target branch is `main` unless the user specifies another test branch.
3. Push or verify the commit on `main`.
4. Watch GitLab CI stages: test, build, image push, deploy artifact, deploy test.
5. Verify the test runner pulled the image and deploy package.
6. Run or verify the health check and open the test URL when possible.
7. Do not fake deployment success. Name the failed stage exactly.

## Handoff

The output must be ready for `sz-mtr-deploy-prod`:

- commit SHA
- image tag
- deploy artifact
- pipeline URL/status
- test URL and health result
