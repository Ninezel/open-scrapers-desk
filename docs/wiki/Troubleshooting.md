# Troubleshooting

- backend missing: check toolkit path and run `npm run build` in the toolkit repo
- no source health rows: validate Node and toolkit CLI access first
- queued jobs not starting: wait for the current `QProcess` job to finish
- empty results library: confirm the output directory matches the toolkit run location
- packaged build warnings: use the generated SHA256 manifest until code signing is added
