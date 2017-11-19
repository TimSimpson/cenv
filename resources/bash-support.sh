bash_support_root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

export CENV_ROOT="${CENV_ROOT:-$HOME/.cenv}"

cenv_path=$(which cenv)
if [ "${cenv_path}" == "" ]; then
    # Assume the user used the install script
    cenv_path="${bash_support_root}"/../output/bvenv/bin/cenv
    # To avoid dragging everything from the virtualenv into the path,
    # make cget available this way.
    function cget(){
        "${bash_support_root}"/../output/bvenv/bin/cget $@
    }
fi

function cenv(){
    "${cenv_path}" "$@"
    if [ "${?}" -eq 0 ]; then
        source "${CENV_ROOT}"/cenv.rc
    fi
}

function cmake(){
    local cmake_path=$(which cmake)
    if [ "${CGET_PREFIX}" == "" ]; then
        $(which cmake) "${@}"
    else
        $(which cmake) \
            -DCMAKE_TOOLCHAIN_FILE="${CGET_PREFIX}"/cget/cget.cmake \
            -DCMAKE_INSTALL_PREFIX="${CGET_PREFIX}" \
            "${@}"
    fi
}
