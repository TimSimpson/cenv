from cenv import envs  # NOQA

from . import path


if False:
    import typing as t  # NOQA


def write_file(old_env, new_env, script_type, file_path):
    # type: (t.Optional[envs.Env], t.Optional[envs.Env], str, str) -> None

    sep = {
        'bash': ':',
        'dos': ';',
    }[script_type]

    p = path.PathUpdater(sep)

    new_path_str = p.update_paths(
        'PATH',
        new_path=None if new_env is None else [new_env.bin, new_env.lib],
        old_path=None if old_env is None else [old_env.bin, old_env.lib])

    new_ld_library_path_str = p.update_paths(
        'LD_LIBRARY_PATH',
        new_path=None if new_env is None else new_env.lib,
        old_path=None if old_env is None else old_env.lib)

    conan_profile = None if new_env is None else new_env.conan_profile
    template_args = {
        'cenv_name': '' if new_env is None else new_env.name,
        'cget_prefix': '' if new_env is None else new_env.directory,
        'conan_profile': conan_profile or '',
        'path': new_path_str,
        'ld_library_path': new_ld_library_path_str,
    }

    comment = {
        'bash': '#',
        'dos': 'REM',
    }[script_type]
    export = {
        'bash': 'export',
        'dos': 'set',
    }[script_type]

    # CONAN_DEFAULT_PROFILE_PATH
    with open(file_path, 'w') as f:
        f.write(
            "{comment} This file was created by Cenv.\n"
            "{comment} It's intended to be used only once then deleted.\n"
            "{export} CENV_NAME={cenv_name}\n"
            "{export} CGET_PREFIX={cget_prefix}\n"
            "{export} CONAN_DEFAULT_PROFILE_PATH={conan_profile}\n"
            "{export} PATH={path}\n"
            "{export} LD_LIBRARY_PATH={ld_library_path}\n"
            .format(comment=comment, export=export, **template_args))
