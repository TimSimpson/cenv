use std::path;

pub struct World {
    cfg: Config,
}

impl World {
    pub fn create() -> World {
        let cfg = Config::load_from_env_vars();
        Self {
            cfg,
        }
    }
    pub fn cfg(&self) -> &Config {
        return &self.cfg;
    }
}

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
        return self.cenv_root.clone();
    }
    pub fn cget_prefix(&self) -> Option<path::PathBuf> {
        return self.cget_prefix.clone();
    }        
    pub fn set_cenv_root(&mut self, value: Option<path::PathBuf>) {
        self.cenv_root = value
    }    
    pub fn set_cget_prefix(&mut self, value: Option<path::PathBuf>) {
        self.cget_prefix= value
    }    
}
