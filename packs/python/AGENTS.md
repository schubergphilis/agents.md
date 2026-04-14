## Python Conventions

**Toolchain:** uv (package management), ruff (lint + format), pyright (type checking), pytest (testing).

**Setup verification:** Before writing code, confirm: `uv --version` (>= 0.5), `python3 --version` (>= 3.12), `ruff --version`, `pyright --version`. If any are missing, stop and report.

**Package management:** Use `uv add` to add dependencies. Use `uv run` to execute scripts and tools. Do not use pip directly.

**Code style:** Use Python 3.12+ type hints on all public functions. Run `ruff check .` and `ruff format .` — fix all findings before presenting code. No `type: ignore` unless the reason is documented inline.

**Testing:** Tests live in `tests/`. Run with `uv run pytest`. Aim for >80% coverage on new code. Every error path needs a test — silent failures in production are unacceptable.

**Project structure:** Use either `src/<project>/` layout or flat layout with package at root. Be consistent within the project.

**Acceptance criteria:**
- [ ] `ruff check .` passes with zero findings
- [ ] `ruff format --check .` passes
- [ ] `pyright` passes on the source directories
- [ ] `uv run pytest` passes
- [ ] No unhandled error paths in new code
