# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A collection of four independent Python course assignments ("TSIS" 1–4). There is no shared package, build system, dependency manifest, linter config, or test suite. Each `TSISn` folder is a standalone program; modules import each other by bare name (`from config import DB_CONFIG`, `from tools import *`), so **run each program from inside its own source directory**.

Dependencies (install manually): `pygame` (TSIS2–4), `psycopg2` (TSIS1, TSIS4). The checked-in `__pycache__` files show Python 3.14 was used.

## Running

| Project | Directory | Command | Needs |
|---|---|---|---|
| TSIS1 – PhoneBook CLI | `TSIS1/TSIS1/` | `python phonebook.py` | PostgreSQL `phonebook_db` |
| TSIS2 – Paint | `TSIS2/TSIS2/` | `python paint.py` | — |
| TSIS3 – Racer | `TSIS3/` | `python main.py` | — |
| TSIS4 – Snake | `TSIS4/` | `python main.py` | PostgreSQL `snake_db` |

TSIS4 DB connectivity check: `python test_db.py` (a connection smoke script, not a unit test).

Database settings live in each project's `config.py` (`DB_CONFIG` dict passed straight to `psycopg2.connect`) and point at a local Postgres on `localhost:5432` with the author's username. `test_db.py` duplicates the TSIS4 credentials inline.

## Architecture notes

**TSIS1 (PhoneBook)** — Schema and server-side logic are in SQL, not Python. Apply `schema.sql` then `procedures.sql` to the database before running (the app does not create them). Python calls procedures with `CALL add_phone(...)` / `CALL move_to_group(...)` and functions with `SELECT * FROM search_contacts(...)` / `get_contacts_page(limit, offset)`; pagination is intentionally done in the DB function. Tables: `contacts` (name UNIQUE), `groups`, `phones` (`type` constrained to home/work/mobile, cascade delete). Export/import read and write `contacts.json` relative to the **current working directory**; import assigns group `"Other"` when missing and prompts skip/overwrite on duplicate names. `contacts.csv` is present but unused by the code.

**TSIS2 (Paint)** — `paint.py` is a single event loop drawing onto an off-screen `canvas` Surface blitted each frame; `tools.py` holds color lookup, BFS `flood_fill`, and shape helpers. Keyboard selects color (R/G/B), brush size (1/2/3), and tool (Q/W/E/C/F/T/6–9); Ctrl+S saves a timestamped PNG. The `__pycache__` for `connect`/`config` in `TSIS2/` has no matching source and is stale.

**TSIS3 (Racer)** — `main.py` is a state machine (`menu` / `input` / `leaderboard` / `settings` / `game`) that hands control to `racer.run_game(screen, username, settings)`, which runs its own loop and returns `"menu"` or `"quit"`. `persistence.py` stores `settings.json` and a top-10 `leaderboard.json` next to the module (paths resolved from `__file__`). Assets load from `assets/`; `racer.py` also references `coin.wav` and `power.wav`, which don't exist, so those sounds load as `None`. `ui.py` has draw helpers that `main.py` does not use (it draws inline).

**TSIS4 (Snake)** — Same menu state-machine pattern as TSIS3. `game.run_game(username)` imports pygame/db lazily inside the function, re-reads `settings.json` itself, and returns `{"score", "level"}`. `db.py` creates its tables at startup (`players`, `game_sessions`) and opens a fresh connection per call; leaderboard and personal best come from `game_sessions`.

## Conventions

- Code comments and some UI strings are in Russian.
- Each DB helper opens and closes its own connection rather than sharing one.
- `.DS_Store` and `__pycache__` files are committed; there is no `.gitignore`.
