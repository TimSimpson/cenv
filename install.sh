set -e

readonly root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo '* * Building virtualenv for Python dependencies...'
python -m venv output/bvenv || virtualenv output/bvenv
echo '* * Installing CGet...'
./output/bvenv/bin/pip install cget
echo '* * Installing Cenv...'
./output/bvenv/bin/pip install -e "${root}"

echo '* * CENV installed.'

echo 'To use cenv, you need to run the following file from your shell:'
echo 'export PATH="'"${root}"'/output/bvenv/bin:${PATH}"
echo 'source '"${root}"'/resources/bash-support.sh'
