@default:
    just --list

init:
    uv sync

check:
    cargo clippy

build:
    uv run maturin develop

test:
    uv run run_tests.py


test-rs:
    cargo test
