# TYPO3 DDEV Workflow Notes

### Performance

1. **Disable Xdebug** when not debugging (`ddev xdebug off`)
2. **Use snapshots** instead of full imports for quick state changes
3. **Mount with Mutagen** on macOS for better file sync performance
4. **Use PHP 8.3 or 8.4** for best performance on TYPO3 v14

### Team Workflow

1. **Commit** `.ddev/config.yaml` to repository
2. **Gitignore** `.ddev/config.local.yaml` for personal overrides
3. **Document** additional setup steps in `README.md`
4. **Share** database snapshots for consistent development data

### Security

1. **Never expose** DDEV ports publicly
2. **Don't use** DDEV in production
3. **Rotate** any sensitive data in development databases
