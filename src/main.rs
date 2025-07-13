mod cli;
mod commands;
mod envs;
mod options;
mod path;
mod python;
mod result;
mod utils;
mod world;

use result::Result;

pub fn main() -> Result<()> {
    cli::main()
}
