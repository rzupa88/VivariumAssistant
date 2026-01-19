# Contributing

This repo is structured to support a clean “real project” workflow even when working solo.

## Workflow
1. Create an issue (or pick one from the Project board)
2. Create a branch from `main`
3. Implement the change
4. Run checks locally
5. Open a PR
6. Merge when checks are green

## Branch naming
Use prefixes:
- `docs/…`
- `infra/…`
- `engine/…`
- `sim/…`
- `hardware/…`

## Before opening a PR
Run:
```bash
poetry run ruff check .
poetry run mypy .
poetry run pytest -q

## Pull Request Expectations

All changes must be submitted via Pull Request.

A Pull Request is considered ready for review when:

- Code follows existing project structure and conventions
- New logic includes tests (where applicable)
- `ruff`, `mypy`, and `pytest` all pass
- Documentation is updated if behavior or architecture changes
- The PR references a GitHub Issue when applicable

### Commit & Branching Guidelines

- One logical change per branch
- Branches should be named using the pattern:
  - `docs/*`
  - `engine/*`
  - `infra/*`
  - `fix/*`

### Review Policy

- All PRs require CI to pass
- PR authors may not approve their own PRs
- Squash merge is preferred to keep history clean