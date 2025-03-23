from concurrent import futures
import os
import pathlib
import subprocess
import sys


CENV_DIR = pathlib.Path(__file__).parent / "cenv"
BIN_DIR = pathlib.Path(sys.executable).parent
MYPY_OPTIONS = [
    "--strict-optional",
    "--ignore-missing-imports",
    "--disallow-untyped-calls",
    "--disallow-untyped-defs",
    str(CENV_DIR),
]

def mypy3() -> int:
    print(f"{BIN_DIR / 'mypy'} " + " ".join(MYPY_OPTIONS))
    return subprocess.call(f"{BIN_DIR / 'mypy'} " + " ".join(MYPY_OPTIONS), shell=True)


def coverage() -> int:
    return (
        subprocess.call(f"{BIN_DIR / 'coverage'} run -m pytest {CENV_DIR}/tests", shell=True)
        or subprocess.call(f"{BIN_DIR / 'coverage'} report -m", shell=True)
        or subprocess.call(f"{BIN_DIR / 'coverage'} html --directory coverage/py36", shell=True)
    )


def run_all() -> int:
    executor = futures.ThreadPoolExecutor(max_workers=4)
    async_results = []
    async_results.append(executor.submit(mypy3))
    async_results.append(executor.submit(coverage))

    for f in futures.as_completed(async_results):
        if f.result() != 0:
            return f.result()

    return 0


if __name__=='__main__':
    sys.exit(run_all())
