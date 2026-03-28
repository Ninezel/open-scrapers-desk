# Release Workflow

This repository follows a paired release workflow with the toolkit repo so app changes, docs, and public wiki content ship together.

## Standard workflow

1. implement the desktop changes
2. update repo docs and wiki source pages
3. update `CHANGELOG.md` with the current date
4. run `python -m compileall src`
5. run `python scripts/smoke_test.py`
6. run `python scripts/build_exe.py`
7. confirm toolkit integration still works
8. commit with a detailed message
9. push the main repo
10. sync the GitHub wiki from `docs/wiki`

## Release note format

Use a dated heading:

```md
## 2026-03-28
```

Group changes under `Added`, `Changed`, and `Maintenance` where useful.
