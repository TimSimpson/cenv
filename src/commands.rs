use crate::Result;


pub fn init(env_name: String, extra_args: Vec<String>) -> Result<()> {
    println!("init - TODO");
    println!("env_name={}", env_name);
    println!("env_args={:?}", extra_args);
    Ok(())
}

pub fn list(verbose: bool) -> Result<()> {
    println!("list - TODO");
    println!("verbose={}", verbose);
    Ok(())
}

pub fn set(managed: bool, env_name: Option<String>) -> Result<()> {
    println!("set_env - TODO");
    println!("managed={:?}", managed);
    println!("env_name={:?}", env_name);
    Ok(())
}