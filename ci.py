import os
import subprocess
import sys

from cenv import frontdoor


REGISTRY = frontdoor.CommandRegistry('ci')
cmd = REGISTRY.decorate
ROOT=os.path.dirname(os.path.realpath(__file__))


def from_root(path):
    """Returns a path relative to the root directory."""
    if os.name == 'nt':
        path = path.replace('/', '\\')
    return os.path.join(ROOT, path)


def check_tox(name):
    if not os.path.exists(os.path.join(ROOT, '.tox', name)):
        raise RuntimeError('This requires tox to run first. Run `tox {}`.'
                           .format(name))


@cmd('flake8', 'Runs flake8, pep8 checks')
def flake8(args=None):
    check_tox('pep8')
    print('* * Flake 8 * *')
    args = args or ['cenv']
    return subprocess.call(
        [
            from_root('.tox/pep8/bin/flake8'),
            '--import-order-style=google',
            from_root('cenv'),
        ] + args,
        cwd=ROOT)


@cmd('mypy', 'Runs MyPy\'s optional static typing.')
def mypy(_args):
    check_tox('mypy')
    args = [
        from_root('.tox/mypy/bin/mypy'),
        '--strict-optional',
        '--ignore-missing-imports',
        '--disallow-untyped-calls',
        '--disallow-untyped-defs',
    ]
    print('* * MyPy 2.7 Mode * *')
    result = subprocess.call(args + ['--py2', from_root('cenv')], cwd=ROOT)
    if result: return result
    print('* * MyPy 3.6 Mode * *')
    return subprocess.call(args + [from_root('cenv')], cwd=ROOT)


def tests(venv, name, args):
    args = args or [from_root('cenv/tests'), '-vv', '-s', '-x']
    check_tox(venv)
    print('* * Tests {} * *'.format(name))
    return subprocess.call(
        [
            from_root('.tox/{}/bin/pytest'.format(venv)),
        ] + args,
        cwd=ROOT)


@cmd('tests-2', 'Runs Python 2 tests')
def tests_2(args=None):
    return tests('py27', '2.7', args)


@cmd('tests-3', 'Runs Python 3 tests')
def tests_3(args=None):
    return tests('py36', '3.6', args)


@cmd('coverage', 'Generate coverage report')
def coverage(args=None):
    return subprocess.call([
            from_root('.tox/py36/bin/coverage'),
            'run',
            '-m',
            'py.test',
            from_root('cenv/tests')
        ], cwd=ROOT) or subprocess.call([
            from_root('.tox/py36/bin/coverage'),
            'report',
            '-m'
        ], cwd=ROOT) or subprocess.call([
            from_root('.tox/py36/bin/coverage'),
            'html'
        ], cwd=ROOT)


if __name__ == "__main__":
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    result = REGISTRY.dispatch(args)
    sys.exit(result)
