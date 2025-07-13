@default:
    just --list

init:
    uv sync

check:
    cargo clippy

test:
    uv run run_tests.py


build-rs:
    cargo build 

test-rs:
    cargo test
