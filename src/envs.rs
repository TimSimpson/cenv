use crate::utils;
use crate::world::World;
use crate::Result;
use std::sync::Arc;
use std::fs;
use std::process;
use eyre::eyre;
use std::path;

pub struct Env {
    name: String,
    directory: path::PathBuf,
    env_vars: Box<dyn utils::EnvVars>,
    managed: bool,
}

impl Env {
    pub fn new(name: String, directory: path::PathBuf, managed: bool) -> Self {
        Self {
            name,
            directory,
            managed,
            env_vars: Box::new(utils::OsEnvVars::new()),
        }
    }

    pub fn new2(
        name: String,
        directory: path::PathBuf,
        managed: bool,
        env_vars: Box<dyn utils::EnvVars>,
    ) -> Self {
        Self {
            name,
            directory,
            managed,
            env_vars,
        }
    }

    fn cget_prefix(&self) -> Option<path::PathBuf> {
        match self.env_vars.get_var("GET_PREFIX").as_ref() {
            "" => None,
            content => Some(path::PathBuf::from(content)),
        }
    }

    pub fn active(&self) -> bool {
        match self.cget_prefix() {
            None => false,
            Some(cget_prefix) => self.directory == cget_prefix,
        }
    }

    pub fn bin(&self) -> path::PathBuf {
        self.directory.join("bin")
    }

    pub fn get_creation_info(&self) -> Result<String> {
        let cenv_info_file = self.directory.join("cenv-info.txt");
        match std::fs::read_to_string(&cenv_info_file) {
            Ok(contents) => Ok(contents),
            Err(_) => Err(eyre!("<info file not found>")),
        }
    }

    pub fn managed(&self) -> bool {
        self.managed
    }

    pub fn name(&self) -> &str {
        &self.name
    }

    pub fn directory(&self) -> &path::PathBuf {
        &self.directory
    }

    pub fn lib(&self) -> path::PathBuf {
        self.directory.join("lib")
    }
}

impl PartialEq for Env {
    fn eq(&self, other: &Self) -> bool {
        self.name == other.name && self.directory == other.directory
    }
}

impl std::fmt::Display for Env {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "Env(name={}, directory={})",
            self.name,
            self.directory.display()
        )
    }
}

pub struct Manager {
    root_dir: path::PathBuf,
    world: Arc<World>,
}

impl Manager {
    pub fn new(root_dir: path::PathBuf, world: Arc<World>) -> Self {
        Self { root_dir, world }
    }

    pub fn create(&self, name: String, cget_args: Vec<String>) -> Result<Env> {
        use std::io::Write;

        let prior = self.get(true, &name)?;
        if let Some(prior) = prior {
            return Err(eyre::eyre!("{} already exists at {:?}", prior.name, prior.directory));
        }
        let new_env_directory = self.root_dir.join(&name);
        fs::create_dir_all(new_env_directory.clone())?;
        let new_env_directory_str = match new_env_directory.to_str() {
            Some(s) => s.to_string(),
            None => return Err(eyre::eyre!("error getting path at {:?}", new_env_directory))
        };
        
        let mut cmd = vec![
            "cget".to_string(), "init".to_string(), "--prefix".to_string(), new_env_directory_str,
        ];
        cmd.extend(cget_args.clone());
        self.world.view().run_command(cmd.join(" "))?;
        let status = std::process::Command::new(&cmd[0]).args(cmd.iter().skip(1)).status()?;
        if !status.success() {
            return Err(eyre::eyre!("error calling process: {:?}", cmd));
        }
        let cenv_info_txt = new_env_directory.join("cenv-info.txt");
        let mut file = fs::File::create(cenv_info_txt)?;
        let joined = cget_args
            .iter()
            .map(|arg| {
                if arg.contains(' ') {
                    format!("\"{}\"", arg)
                } else {
                    arg.clone()
                }
            })
            .collect::<Vec<_>>()
            .join(" ");
        file.write_all(joined.as_bytes())?;
        Ok(Env::new(name, new_env_directory, true))
    }

    pub fn delete(&self, name: &str) -> Result<()> {
        if let Some(env) = self.get(true, name)? {
            if !self.manages_directory(env.directory()) {
                // Avoid deleteing an environment we don't seem to own.
                return Err(eyre::eyre!("It doesn't look like cenv manages this environment."));
            }
            fs::remove_dir_all(env.directory())?;
        }
        Ok(())
    }

    pub fn find_active_env(&self) -> Result<Option<Env>> {
        for env in self.list()? {
            if env.active() {
                return Ok(Some(env));
            }
        }
        Ok(None)
    }

    pub fn get(&self, managed: bool, name_or_directory: &str) -> Result<Option<Env>> {
        let (managed, name, dir_path) = if managed {
            (managed, name_or_directory.to_string(), self.root_dir.join(name_or_directory))
        } else {
            let dir_path = path::PathBuf::from(name_or_directory);
            let name = match dir_path.file_name() {
                Some(v) => v.to_string_lossy().into_owned().to_string(),
                None => return Result::Err(eyre::eyre!("cannont handle name or directory: {:?}", name_or_directory))
            };
            let managed =self.manages_directory(&dir_path) ;
            (managed, name, dir_path)
        };

        if dir_path.exists() && dir_path.is_dir() {
            let toolchain = dir_path.join("cget/cget.make");
            if toolchain.exists() && toolchain.is_file() {
                return Ok(Some(Env::new(name, dir_path, managed)));
            }
        }
        Ok(None)
    }

    pub fn list(&self) -> Result<Vec<Env>> {
        let mut result = Vec::new();

        if let Some(cget_prefix) = self.world.cfg().cget_prefix() {
            if !self.manages_directory(&cget_prefix) {
                let name = match cget_prefix.file_name() {
                    Some(file_name) => file_name.to_string_lossy().into_owned().to_string(),
                    None => return Err(eyre::eyre!("rotten file path: {:?}", cget_prefix))
                };
                let fs_env = Env::new(name, cget_prefix, false);
                result.push(fs_env);
            }
        }
        for file in fs::read_dir(&self.root_dir)? {
            if let Ok(file) = file {
                let file_name = file.file_name();
                let dir_path = self.root_dir.join(file.file_name());
                if dir_path.is_dir() {
                    result.push(Env::new(file_name.to_string_lossy().into_owned().to_string(), dir_path, true));
                }
            }
        }
        Ok(result)
    }

    fn manages_directory(&self, directory: &path::PathBuf) -> bool {
        directory.starts_with(&self.root_dir)
    }
}
