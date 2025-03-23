use std::path;

pub struct Options {
    pub root_directory: path::PathBuf,
}

impl Options {
    pub fn new<P: AsRef<path::Path>>(root_directory: P) -> crate::Result<Self> {
        Ok(Self {
            root_directory: root_directory.as_ref().to_path_buf(),
        })
    }

    pub fn from_root(&self, path: &str) -> path::PathBuf {
        self.root_directory.join(path)
    }

    pub fn batch_file(&self) -> path::PathBuf {
        self.from_root("set-vars.bat")
    }

    pub fn environments(&self) -> path::PathBuf {
        self.from_root("envs")
    }

    pub fn rc_file(&self) -> path::PathBuf {
        self.from_root("cenv.rc")
    }

    pub fn root_directory(&self) -> path::PathBuf {
        self.root_directory.clone()
    }
}
