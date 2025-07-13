mod cli;
mod commands;
mod config;
mod envs;
mod options;
mod path;
mod python;
mod result;
mod utils;

use result::Result;

pub fn main() -> Result<()> {
    cli::main()
}
