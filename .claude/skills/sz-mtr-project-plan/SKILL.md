---
name: sz-mtr-project-plan
description: Create a concrete implementation plan from an approved spec or user-confirmed scope. Use before coding when work has multiple steps, affects architecture/deployment/auth/database/API contracts, or needs an explicit validation and rollout plan.
---

# SZ-MTR Project Plan

## Workflow

1. Read `AGENTS.md`, `CLAUDE.md`, `docs/worklog.md`, and the approved spec or latest user scope.
2. Inspect the codebase before deciding the plan.
3. Define the horizontal architecture first: module boundaries, data model, API contracts, auth/permission model, deployment/config contracts, observability, and shared test strategy.
4. After the horizontal architecture is stable, split the work into vertical slices by end-to-end user or system capability.
5. Make each vertical slice independently buildable, testable, and mergeable.
6. Plan `git worktree` usage for parallel slices when the work can be safely split.
7. Define validation commands, UI checks, database checks, and deployment checks.
8. Call out migration, rollback, secret, or infrastructure assumptions.
9. Wait for user approval when the project rules require plan approval before execution.

## Handoff

The output must be ready for `sz-mtr-project-code`:

- ordered implementation steps
- horizontal architecture map
- vertical slice breakdown
- suggested worktree branches and integration order when parallel work is useful
- expected touched areas
- validation plan
- rollback/deploy notes if relevant
- explicit blockers if any
