use std::path::PathBuf;
use clap::{Parser, Subcommand};

use crate::commands;

#[derive(clap::Parser)]
#[command(name="cenv", about = "Works with cget prefix paths")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Parser)]
enum Command {
    Init(InitArgs),
    List(ListArgs),
    Set(SetArgs),
}

#[derive(clap::Parser)]
struct ListArgs {
    #[structopt(short, long, help = "verbose")]
    verbose: bool,
}

#[derive(clap::Parser)]
struct InitArgs {
    #[structopt(help = "name of new cenv")]
    env_name: String,    
    extra_args: Vec<String>,
}

#[derive(clap::Parser)]
#[group(required = false, multiple = false)]
struct SetArgs {
    #[structopt(help = "name of the enviornment")]
    env_name: Option<String>,    
    #[structopt(short, long, help = "directory of an enviornment")]
    dir: Option<String>,    
}

pub fn main() -> crate::Result<()> {
    use clap::builder::TypedValueParser;
    let opt = Cli::parse();
    match opt.command {
        Command::Init(args) => {
            commands::init(args.env_name, args.extra_args)            
        }
        Command::List(args) => {
            commands::list(args.verbose)
        }
        Command::Set(args) => {
            match args.env_name {
                Some(env_name) => commands::set(true, Some(env_name)),
                None => match args.dir {
                    Some(dir) => commands::set(false, Some(dir)),
                    None => commands::set(false, None)
                }
            }
        }
    }
}
