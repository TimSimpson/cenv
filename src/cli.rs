use std::path::PathBuf;
use clap::{Parser, Subcommand};

use crate::commands;
use crate::world;

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
    let exit_code = match opt.command {
        Command::Init(args) => {
            let ctx = world::World::create()?;
            commands::init(&ctx, args.env_name, args.extra_args)?
        }
        Command::List(args) => {
            let ctx = world::World::create()?;
            commands::list(&ctx, args.verbose)?
        }
        Command::Set(args) => {
            let ctx = world::World::create()?;
            match args.env_name {
                Some(env_name) => commands::set(&ctx, true, Some(env_name))?,
                None => match args.dir {
                    Some(dir) => commands::set(&ctx, false, Some(dir))?,
                    None => commands::set(&ctx, false, None)?
                }
            }
        }
    };
    std::process::exit(exit_code);
    Ok(())
}
