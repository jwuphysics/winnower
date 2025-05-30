# CLAUDE.md - The Winnower

## General
- Use `uv` as the package manager
- Run single tests when we make modifications
- Keep the git repository clean
- Keep the number of dependencies small

## Notes

- **Repository**: https://github.com/jwuphysics/winnower
- **Author**: John F. Wu (jwuphysics@gmail.com)
- **License**: MIT
- **Python Version**: 3.8+

**Important**: Never commit API keys or configuration files with secrets. The `.gitignore` excludes `.env` and `config.json` files for this reason.

## Developer Memories

- Always use the project API keys in .env when testing
- Always use `uv run` to execute Python commands and tests
- When creating git tags, always update version numbers in both `winnower/__init__.py` and `pyproject.toml`