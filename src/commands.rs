use crate::Result;

use crate::world;

pub fn init(w: &world::World, env_name: String, extra_args: Vec<String>) -> Result<()> {
    println!("init - TODO");
    println!("env_name={}", env_name);
    println!("env_args={:?}", extra_args);
    Ok(())
}

pub fn list(w: &world::World, verbose: bool) -> Result<()> {
    println!("list - TODO");
    println!("verbose={}", verbose);
    Ok(())
}

pub fn set(w: &world::World, managed: bool, env_name: Option<String>) -> Result<()> {
    println!("set_env - TODO");
    println!("managed={:?}", managed);
    println!("env_name={:?}", env_name);
    Ok(())
}