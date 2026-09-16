---
name: sz-mtr-project-spec
description: Turn a business request or rough idea into an approved project spec before implementation. Use when the user asks to clarify requirements, define acceptance criteria, settle scope, document architecture/API/data contracts, or prepare a spec before planning or coding.
---

# SZ-MTR Project Spec

## Workflow

1. Read project entry docs if present: `AGENTS.md`, `CLAUDE.md`, `docs/architecture.md`, `docs/worklog.md`.
2. Capture the business goal, users, environments, dependencies, data boundaries, non-goals, and acceptance criteria.
3. For cross-module, deployment, authentication, database, or external API changes, produce an explicit contract.
4. Ask only for missing information that materially blocks a correct spec.
5. Write or update the project spec in the project’s chosen location, or summarize the spec if no spec folder exists.
6. Do not implement code in this stage unless the user explicitly moves to code.

## Handoff

The output must be ready for `sz-mtr-project-plan`:

- approved scope
- acceptance checks
- affected files/modules
- risks and open questions
- deployment or data migration notes when relevant
