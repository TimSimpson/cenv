use std::path::PathBuf;

use clap::{Parser, Subcommand};

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
    #[structopt(short, long, help = "name of new cenv")]
    env_name: String,    
    #[structopt(long, help = "additional arguments to cget")]
    extra_args: Vec<String>,
}

#[derive(clap::Parser)]
struct SetArgs {
    #[structopt(short, long, help = "name of new cenv")]
    env_name: String,    
    #[structopt(short, long, help = "explicit directory if the prefix path wasn't created by cget")]
    dir: Option<String>,
}

pub fn main() -> crate::Result<()> {
    use clap::builder::TypedValueParser;
    let opt = Cli::parse();
    match opt.command {
        Command::Init(args) => {
            // TODO
            Ok(())
        }
        Command::List(args) => {
            // TODO
            Ok(())
        }
        Command::Set(args) => {
            // TODO
            Ok(())
        }
    }
}
