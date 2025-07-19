use std::path;

use crate::Result;
use crate::options;

pub struct Config {
    cget_prefix: Option<path::PathBuf>,
    cenv_root: Option<path::PathBuf>,
}

impl Config {
    pub fn load_from_env_vars() -> Config {
        let cget_prefix = std::env::var("CGET_PREFIX").ok().map(path::PathBuf::from);
        let cenv_root = std::env::var("CENV_ROOT").ok().map(path::PathBuf::from);
        Config {
            cget_prefix,
            cenv_root,
        }
    }

    pub fn cenv_root(&self) -> Option<path::PathBuf> {
        self.cenv_root.clone()
    }
    pub fn cget_prefix(&self) -> Option<path::PathBuf> {
        self.cget_prefix.clone()
    }
    pub fn set_cenv_root(&mut self, value: Option<path::PathBuf>) {
        self.cenv_root = value
    }
    pub fn set_cget_prefix(&mut self, value: Option<path::PathBuf>) {
        self.cget_prefix = value
    }
}

pub trait View {
    fn log_debug(&self, msg: &str) -> Result<()>;
    fn run_command(&self, _command: String) -> Result<()>;
}

pub struct NullView {}

impl NullView {
    pub fn new() -> Self {
        Self {}
    }
}

impl View for NullView {
    fn log_debug(&self, _: &str) -> Result<()> {
        Ok(())
    }
    fn run_command(&self, _: String) -> Result<()> {
        Ok(())
    }
}

pub struct DebugView {}

impl DebugView {
    pub fn new() -> Self {
        Self {}
    }
}

impl View for DebugView {
    fn log_debug(&self, msg: &str) -> Result<()> {
        println!("{msg}");
        Ok(())
    }
    fn run_command(&self, command: String) -> Result<()> {
        println!("run_command: {command}");
        Ok(())
    }
}

pub struct World {
    cfg: Config,
    ops: options::Options,
    view: Box<dyn View>,
}

impl World {
    pub fn create(debug: bool) -> Result<World> {
        let cfg = Config::load_from_env_vars();
        let default_root = dirs::home_dir()
            .ok_or_else(|| eyre::eyre!("Could not find home directory"))?
            .join(".cenv");
        let root: path::PathBuf = cfg.cenv_root().unwrap_or(default_root);
        let ops = options::Options::new(root)?;
        Ok(Self {
            cfg,
            ops,
            view: if debug {
                Box::new(DebugView::new())
            } else {
                Box::new(NullView::new())
            },
        })
    }

    pub fn cfg(&self) -> &Config {
        &self.cfg
    }

    pub fn ops(&self) -> &options::Options {
        &self.ops
    }

    pub fn view(&self) -> &dyn View {
        self.view.as_ref()
    }
}
