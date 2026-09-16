---
name: sz-mtr-project-bootstrap
description: Initialize the SZ-MTR project lifecycle, equivalent to the init stage. Use when creating a new frontend/backend project, generating the standard scaffold, binding or creating GitLab, pushing main, running CI/CD, and deploying a reachable test environment with SZ-MTR deployment conventions.
metadata:
  short-description: Bootstrap SZ-MTR frontend/backend projects
---

# SZ-MTR Project Bootstrap

## When to Use

Use this skill for the `init` stage when the user asks to initialize a frontend/backend project, generate standard deployment files, add AGENTS.md or CLAUDE.md, add release/CI/CD guidance, add local validation docs, or bootstrap a project through GitLab to a reachable test environment.

## Workflow

1. Read `references/project-bootstrap.md` for the current scaffold contract.
2. For a full bootstrap to test environment, ask the user to complete a private env file based on `config/init-project.env.example`.
   - Do not commit the filled env file.
   - Use the env file as the single source for GitLab, Registry, Runner, test deployment, and production gate values.
   - If the env file is missing, collect only the missing values before continuing.
3. Confirm or infer these scaffold parameters from the env file or user message:
   - `target`
   - `app`
   - `display-name`
   - `domain`
   - `backend`
   - `frontend`
   - `database`
   - `backend-port`
   - `enable-oidc`
4. Run `tools/project-scaffold/create_project.py` from the standards repository.
5. If the user requested full bootstrap, initialize or bind the GitLab project, push `main`, verify CI/CD, wait for the test deployment, and return the test URL.
6. Validate generated files:
   - `bash -n deploy/*.sh`
   - `docker compose -f deploy/docker-compose.yml config`
   - `test -f docs/active-skill-flow.md`
   - `test -f docs/release-and-cicd.md`
   - inspect `AGENTS.md`, `CLAUDE.md`, `docs/`, and `deploy/`
7. Update `docs/worklog.md`.
8. Commit the generated standard files.

## Rules

- Do not copy full docs into `AGENTS.md` or `CLAUDE.md`; link to `docs/`.
- Do not generate real secrets.
- Do not commit generated real `.env` files.
- Do not commit a filled `init-project.env`; only commit `.example` files.
- Do not fake CI/CD success. If GitLab, Registry, Runner, deployment, or health check fails, report the exact failed stage.
- Do not generate OpenSpec by default. OpenSpec or any equivalent change governance tool is a developer/team choice, not part of this project scaffold standard.
