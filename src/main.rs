mod cli;
mod commands;
mod envs;
mod options;
mod path;
mod result;
mod utils;
mod world;

use result::Result;

pub fn main() -> Result<()> {
    cli::main()
}
