pub trait EnvVars {
    fn get_var(&self, var_name: &str) -> String;
}

pub struct OsEnvVars {}

impl OsEnvVars {
    pub fn new() -> Self {
        Self {}
    }
}

impl EnvVars for OsEnvVars {
    fn get_var(&self, var_name: &str) -> String {
        std::env::var(var_name).unwrap_or_default()
    }
}
