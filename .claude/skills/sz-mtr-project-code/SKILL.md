---
name: sz-mtr-project-code
description: Implement approved project changes in a SZ-MTR standard project. Use when the user says to code, fix, refactor, implement, continue after an approved plan, or apply a scoped change while preserving standards, worklog, and git discipline.
---

# SZ-MTR Project Code

## Workflow

1. Read `AGENTS.md`, `CLAUDE.md`, `docs/worklog.md`, and the approved plan if present.
2. Check `git status --short` before editing.
3. Inspect existing patterns before adding abstractions or dependencies.
4. Implement horizontal architecture contracts first when the approved plan requires them.
5. Use `git worktree` for parallel vertical slices when useful:
   - create one worktree per slice from the same approved base commit
   - keep shared contracts stable across slices
   - validate each worktree independently
   - merge slices through the planned integration order
   - remove completed worktrees after merge
6. Make scoped edits only; do not revert unrelated user changes.
7. Update docs or generated examples when behavior changes.
8. Update `docs/worklog.md` when the project has one.
9. Commit after validation unless the user explicitly asks not to.

## Handoff

The output must be ready for `sz-mtr-project-test`:

- implementation summary
- horizontal contracts implemented or changed
- vertical slices completed and remaining
- worktree branches used, if any
- changed files
- migration/config notes
- commands needed to validate
