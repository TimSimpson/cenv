@default:
    just --list

init:
    uv sync

build:
    uv run maturin develop

test:
    uv run run_tests.py
