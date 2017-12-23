set -e

readonly root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo '* * Building virtualenv for Python dependencies...'
python -m venv output/bvenv || virtualenv output/bvenv
echo '* * Installing CGet...'
./output/bvenv/bin/pip install cget
echo '* * Installing Cenv...'
./output/bvenv/bin/pip install -e "${root}"

echo '* * CENV installed.'

echo 'To use cenv, add the following code to your bash.rc file or wherever '
echo 'you initialize your shell:'
echo ''
echo '    source '"${root}"'/resources/bash-support.sh'
echo ''
echo 'To make the active cenv display in your prompt, add something like this:'
echo ''
echo '    # Show the name of the cenv in your prompt (optional):'
echo '    function echo_current_cenv() {'
echo '        if [ "${CENV_NAME}" != "" ]; then'
echo '            echo "{${CENV_NAME}} "'
echo '        else'
echo '            echo ""'
echo '        fi'
echo '    }'
echo ''
echo '    export PS1="\`echo_current_cenv\` ${PS1}"'
echo ''
