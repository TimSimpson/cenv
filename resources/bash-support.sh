bash_support_root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

export CENV_ROOT="${CENV_ROOT:-$HOME/.cenv}"

cenv_path=$(which cenv)
cget_path=$(which cget)

if [ "${cenv_path}" == "" ]; then
    # Assume the user used the install script
    cenv_path="${bash_support_root}"/../output/bvenv/bin/cenv
    # To avoid dragging everything from the virtualenv into the path,
    # make cget available this way.
    if [ "${cget_path}" == "" ]; then
        function cget(){
            "${bash_support_root}"/../output/bvenv/bin/cget $@
        }
    fi
fi


function cenv(){
    if [ -e "${CENV_ROOT}"/cenv.rc ]; then
        rm -f "${CENV_ROOT}"/cenv.rc
    fi
    "${cenv_path}" "$@"
    if [ "${?}" -eq 0 ] && [ -e "${CENV_ROOT}"/cenv.rc ]; then
        source "${CENV_ROOT}"/cenv.rc
    fi
}

function cmake(){
    local cmake_path=$(which cmake)
    local is_build=
    for arg in "$@"
    do
        if [[ "${arg}" == "--build" ]]; then
            is_build="yes"
        fi
        echo "${arg}"
    done
    if [ "${CGET_PREFIX}" == "" ] || [ "${is_build}" != "" ]; then
        "${cmake_path}" "${@}"
    else
        "${cmake_path}" \
            -DCMAKE_TOOLCHAIN_FILE="${CGET_PREFIX}"/cget/cget.cmake \
            -DCMAKE_INSTALL_PREFIX="${CGET_PREFIX}" \
            "${@}"
    fi
}
