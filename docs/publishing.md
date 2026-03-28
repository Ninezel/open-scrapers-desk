# Publishing Checklist

1. Run `python -m compileall src`
2. Run `python scripts/smoke_test.py`
3. Build the executable with `python scripts/build_exe.py`
4. Confirm the app opens and the toolkit connection still works
5. Update `CHANGELOG.md` with the current date and timestamp
6. Update README and wiki source pages when features change
7. Commit with a detailed message
8. Push the main repo
9. Sync the live wiki from `docs/wiki`
10. Publish the GitHub Actions build artifacts, zip, and SHA256 manifest or a tagged release

When the app changes how it calls the toolkit CLI, make sure the toolkit docs are updated in parallel.
