use crate::Result;
use crate::envs;
use crate::path;
use crate::world;
use std::path::PathBuf;

fn get_env_manager<'a>(w: &'a world::World) -> envs::Manager<'a> {
    envs::Manager::new(w.ops().environments(), w)
}

pub fn init(w: &world::World, env_name: String, extra_args: Vec<String>) -> Result<i32> {
    println!("init - TODO");
    w.view().log_debug(&format!("env_name={env_name}"))?;
    w.view().log_debug(&format!("env_args={extra_args:?}"))?;
    for args in &extra_args {
        if args == "--prefix" || args == "-p" {
            eprintln!("Invalid value `--prefix` or `-p`: cenv sets this when calling cget.");
            return Ok(1);
        }
    }
    let env = get_env_manager(w).create(env_name, extra_args)?;
    println!("Created new {env}");
    Ok(0)
}

pub fn list(w: &world::World, verbose: bool) -> Result<i32> {
    w.view().log_debug("list - TODO")?;
    w.view().log_debug(&format!("verbose={verbose}"))?;

    let mut envs = get_env_manager(w).list()?;
    if envs.is_empty() {
        println!("No envs found!")
    } else {
        envs.sort_by(|a, b| a.name().cmp(b.name()));
        for env in envs {
            let active = if env.active() { '*' } else { ' ' };
            if verbose {
                println!("{} {}\t{}", active, env.name(), env.get_creation_info()?);
            } else {
                println!("{} {}", active, env.name());
            }
            if !env.managed() {
                println!("    ^- full path: {:?}", env.directory());
            }
        }
    }
    Ok(0)
}

fn path_buf_to_string(path: &PathBuf) -> String {
    path.to_owned().to_string_lossy().to_string()
}

enum ScriptLanguage {
    Bash,
    Dos,
}

fn write_file(
    old_env: &Option<envs::Env>,
    new_env: &Option<envs::Env>,
    script_type: ScriptLanguage,
    file_path: &PathBuf,
) -> Result<()> {
    use ScriptLanguage::*;
    use std::io::Write;

    let path_sep = match script_type {
        Bash => ':',
        Dos => ';',
    };
    let p = path::PathUpdater::new(path_sep);

    let new_path_str = {
        let new_path_arg = match new_env {
            None => Vec::new(),
            Some(env) => vec![
                path_buf_to_string(&env.bin()),
                path_buf_to_string(&env.lib()),
            ],
        };
        let new_path_arg_2 = new_path_arg
            .iter()
            .map(|s| s.as_str())
            .collect::<Vec<&str>>();
        let old_path_arg = match old_env {
            None => Vec::new(),
            Some(env) => vec![
                path_buf_to_string(&env.bin()),
                path_buf_to_string(&env.lib()),
            ],
        };
        let old_path_arg_2 = old_path_arg
            .iter()
            .map(|s| s.as_str())
            .collect::<Vec<&str>>();
        p.update_paths("PATH", &new_path_arg_2, &old_path_arg_2)
    };

    let new_ld_library_path_str = {
        let new_path_arg = match new_env {
            None => Vec::new(),
            Some(env) => vec![path_buf_to_string(&env.lib())],
        };
        let new_path_arg_2 = new_path_arg
            .iter()
            .map(|s| s.as_str())
            .collect::<Vec<&str>>();
        let old_path_arg = match old_env {
            None => Vec::new(),
            Some(env) => vec![path_buf_to_string(&env.lib())],
        };
        let old_path_arg_2 = old_path_arg
            .iter()
            .map(|s| s.as_str())
            .collect::<Vec<&str>>();
        p.update_paths("LD_LIBRARY_PATH", &new_path_arg_2, &old_path_arg_2)
    };

    let comment = match script_type {
        Bash => "#",
        Dos => "REM",
    };
    let export = match script_type {
        Bash => "export",
        Dos => "set",
    };

    let quote = |var: &str| -> Result<String> {
        if let Bash = script_type {
            Ok(shlex::try_quote(var)?.to_string())
        } else {
            Ok(var.to_string())
        }
    };
    let cenv_name = quote(match new_env {
        None => "",
        Some(e) => e.name(),
    })?;
    let cget_prefix_uq = match new_env {
        None => "",
        Some(e) => &path_buf_to_string(e.directory()),
    };
    let cget_prefix = quote(cget_prefix_uq)?;
    let path = quote(&new_path_str)?;
    let ld_library_path = quote(&new_ld_library_path_str)?;

    let mut file = std::fs::File::create(file_path)?;
    file.write_all(
        format!(
            "{comment} This file was created by Cenv.\n\
        {comment} It's intended to be used only once then deleted.\n\
        {export} CENV_NAME={cenv_name}\n\
        {export} CGET_PREFIX={cget_prefix}\n\
        {export} PATH={path}\n\
        {export} LD_LIBRARY_PATH={ld_library_path}\n",
        )
        .as_bytes(),
    )?;
    Ok(())
}

pub fn set(w: &world::World, managed: bool, env_name: Option<String>) -> Result<i32> {
    w.view().log_debug("set_env - TODO")?;
    w.view().log_debug(&format!("managed={managed:?}"))?;
    w.view().log_debug(&format!("env_name={env_name:?}"))?;

    let env_manager = get_env_manager(w);

    let old_env = env_manager.find_active_env()?;

    let new_env = match env_name {
        Some(env_name) => match env_manager.get(managed, &env_name)? {
            Some(env) => Some(env),
            None => {
                if managed {
                    println!("No such environment {env_name}");
                } else {
                    println!(
                        "\"{env_name}\" is not a directory or does not contain a valid toolchain file at \"{env_name}/cget/cget.cmake\"."
                    );
                }
                return Ok(1);
            }
        },
        None => None,
    };
    write_file(&old_env, &new_env, ScriptLanguage::Bash, &w.ops().rc_file())?;
    write_file(
        &old_env,
        &new_env,
        ScriptLanguage::Dos,
        &w.ops().batch_file(),
    )?;

    match new_env {
        Some(new_env) => println!("* * using {}", new_env.name()),
        None => println!("* * cenv deactivated"),
    }

    Ok(0)
}
