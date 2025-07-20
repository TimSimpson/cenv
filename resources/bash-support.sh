# source this in Bash to replace "cenv" with a function that wrapper Bash
# function that will call "cenv" and then set variables in your shell session,
# and replaces "cmake" with an imposter that will set the tool chain and
# install prefix files.
bash_support_root=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

export CENV_ROOT="${CENV_ROOT:-$HOME/.cenv}"

function cenv(){
    if [ -e "${CENV_ROOT}"/cenv.rc ]; then
        rm "${CENV_ROOT}"/cenv.rc
    fi
    if [[ "${1}" == "set" ]]; then
        shift 1        
        new_cenv_name=$(cenv-rs set2 bash CENV_NAME "${@}")
        # if something goes wrong, print what we got and quit
        if [[ ${?} -ne 0 ]]; then
            >&2 echo "${new_cenv_name}"
            return 
        fi
        
        new_cget_prefix=$(cenv-rs set2 bash CGET_PREFIX "${@}")
        if [[ ${?} -ne 0 ]]; then
            >&2 echo "${new_cget_prefix}"
            return 
        fi

        new_path=$(cenv-rs set2 bash PATH "${@}")
        if [[ ${?} -ne 0 ]]; then
            >&2 echo "${new_path}"
            return 
        fi

        new_ld_library_path=$(cenv-rs set2 bash LD_LIBRARY_PATH "${@}")
        if [[ ${?} -ne 0 ]]; then
            >&2 echo "${new_ld_library_path}"
            return 
        fi

        if [[ "" != "${new_cenv_name}" ]]; then
            export CENV_NAME="${new_cenv_name}"
        else 
            unset CENV_NAME
        fi
        if [[ "" != "${new_cget_prefix}" ]]; then
            export CGET_PREFIX="${new_cget_prefix}"
        else 
            unset CGET_PREFIX
        fi         
        if [[ "" != "${new_path}" ]]; then
            export PATH="${new_path}"        
        fi
        if [[ "" != "${new_ld_library_path}" ]]; then
            export LD_LIBRARY_PATH="${new_ld_library_path}"        
        fi
        if [[ "${CENV_NAME}" != "" ]]; then
            echo '* * using '"${CENV_NAME}"
        else
            echo '* * cenv deactivated'
        fi
    else
        cenv-rs "$@"
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
