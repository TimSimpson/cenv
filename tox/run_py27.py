import os
import subprocess
import sys

with open(os.path.join(os.path.dirname(__file__), "py27_path.txt")) as f:
    PYTHON_BIN = f.read()


CENV_DIR = os.path.join(os.path.dirname(__file__), "..", "cenv")
BIN_DIR = os.path.join(os.path.dirname(PYTHON_BIN))

def coverage():
    coverage = os.path.join(BIN_DIR, "coverage")
    return (
        subprocess.call("{} run -m py.test {}/tests".format(coverage, CENV_DIR), shell=True)
        or subprocess.call("{} report -m".format(coverage), shell=True)
        or subprocess.call("{} html --directory coverage/py27".format(coverage), shell=True)
    )


sys.exit(coverage())
