---
name: sz-mtr-deploy-prod
description: Promote a test-verified SZ-MTR release to production using the same Docker image and deploy artifact. Use when the user asks to deploy production, release a tag, approve production, rollback production, or verify a production rollout.
---

# SZ-MTR Deploy Prod

## Workflow

1. Read `docs/release-and-cicd.md` and confirm the production gate: manual approval or protected tag.
2. Require a test-verified commit SHA, image tag, and deploy artifact.
3. Do not rebuild in production; production must pull the same image and artifact tested in `deploy-test`.
4. Confirm backup and rollback instructions before triggering production.
5. Trigger or verify the protected/manual production job.
6. Verify production health check and public URL.
7. Report exact failure stage and rollback option if production deployment fails.

## Handoff

The final output must include:

- production URL and health result
- deployed commit SHA and image tag
- backup/rollback note
- any post-deploy manual checks
