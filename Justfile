@default:
    just --list

init:
    uv sync

test:
    uv run run_tests.py
