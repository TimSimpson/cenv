use crate::utils;
use crate::Result;
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
