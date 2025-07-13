use std::path;


struct Config {
    cget_prefix: Option<path::PathBuf>,
    cenv_root: Option<path::PathBuf>,
}

impl Config {
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