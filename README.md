# Task Manager (Python MVP)

Minimal Python task manager MVP (CLI + SQLite storage).

Quickstart

- Create a virtualenv (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

- Run CLI (creates `tasks.db` in repo root):

```bash
python src/cli.py add "Buy milk" --description "2 liters"
python src/cli.py list
python src/cli.py complete 1
python src/cli.py delete 1
```

Run unit tests:

```bash
python -m unittest discover -v
```

Project layout

- `src/task_manager/` — package with models and storage
- `src/cli.py` — command-line interface
- `tests/` — unit tests (unittest)

