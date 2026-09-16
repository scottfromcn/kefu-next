---
name: sz-mtr-project-test
description: Validate a SZ-MTR project change locally and through CI-ready checks. Use when the user asks to test, verify, run acceptance, inspect UI, validate Docker/local deployment, or confirm that code is ready to push or deploy.
---

# SZ-MTR Project Test

## Workflow

1. Read project validation docs: `docs/project-framework-and-local-validation.md`, `docs/frontend-backend-deployment-plan.md`, and `docs/release-and-cicd.md` if present.
2. Run the smallest reliable checks first, then broaden based on risk.
3. For frontend/UI changes, start the app and verify in a browser or screenshot-capable tool.
4. For deployment changes, run `bash -n deploy/*.sh` and `docker compose -f deploy/docker-compose.yml config`.
5. For database changes, verify migrations and seed/init scripts are repeatable.
6. Report exact failing command, error, and likely owner when validation fails.

## Handoff

The output must be ready for `sz-mtr-deploy-test`:

- passed and failed checks
- unresolved risks
- whether `main` is safe to push
- test URL or local URL when available
