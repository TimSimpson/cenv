use clap::Error;
use clap::Parser;

use crate::commands;
use crate::world;

#[derive(clap::Parser)]
#[command(name = "cenv", about = "Works with cget prefix paths")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(clap::Args, Debug)]
struct GlobalOptions {
    #[arg(long, help = "Enable debug logging")]
    debug: bool,
    #[arg(short, long, help = "verbose")]
    verbose: bool,
}

#[derive(Parser)]
enum Command {
    Init(InitArgs),
    List(ListArgs),
    Set(SetArgs),
    Set2(Set2Args),
}

#[derive(clap::Parser)]
struct ListArgs {
    #[clap(flatten)]
    global: GlobalOptions,
}

#[derive(clap::Parser)]
struct InitArgs {
    #[clap(flatten)]
    global: GlobalOptions,

    #[structopt(help = "name of new cenv")]
    env_name: String,
    extra_args: Vec<String>,
}

#[derive(clap::Parser)]
#[group(required = false, multiple = false)]
struct SetArgs {
    #[clap(flatten)]
    global: GlobalOptions,

    #[structopt(help = "name of the enviornment")]
    env_name: Option<String>,
    #[structopt(short, long, help = "directory of an enviornment")]
    dir: Option<String>,
}

#[derive(clap::Parser)]
#[group(required = false, multiple = false)]
struct Set2Args {
    #[clap(flatten)]
    global: GlobalOptions,
    #[structopt(help = "name of the shell language")]
    shell_name: String,
    #[structopt(help = "the variable to print")]
    var_name: String,
    #[structopt(help = "name of the enviornment")]
    env_name: Option<String>,
    #[structopt(short, long, help = "directory of an enviornment")]
    dir: Option<String>,
}

pub fn main() -> crate::Result<()> {
    let opt = Cli::parse();
    let exit_code = match opt.command {
        Command::Init(args) => {
            let ctx = world::World::create(args.global.debug)?;
            commands::init(&ctx, args.env_name, args.extra_args)?
        }
        Command::List(args) => {
            let ctx = world::World::create(args.global.debug)?;
            commands::list(&ctx, args.global.verbose)?
        }
        Command::Set(args) => {
            let ctx = world::World::create(args.global.debug)?;
            match args.env_name {
                Some(env_name) => commands::set(&ctx, true, Some(env_name))?,
                None => match args.dir {
                    Some(dir) => commands::set(&ctx, false, Some(dir))?,
                    None => commands::set(&ctx, false, None)?,
                },
            }
        }
        Command::Set2(args) => {
            let ctx = world::World::create(args.global.debug)?;
            let script_lang = match args.shell_name.as_str() {
                "dos" => commands::ScriptLanguage::Dos,
                "bash" => commands::ScriptLanguage::Bash,
                _ => {
                    eprintln!("Unknown script lang name: {}", args.var_name);
                    std::process::exit(1);
                }
            };
            let env_var = match args.var_name.as_str() {
                "CENV_NAME" => commands::EnvVar::CenvName,
                "CGET_PREFIX" => commands::EnvVar::CgetPrefix,
                "LD_LIBRARY_PATH" => commands::EnvVar::LbLibraryPath,
                "PATH" => commands::EnvVar::Path,
                _ => {
                    eprintln!("Unknown var name: {}", args.var_name);
                    std::process::exit(1);
                }
            };
            match args.env_name {
                Some(env_name) => commands::set_2(&ctx, script_lang, env_var, true, Some(env_name))?,
                None => match args.dir {
                    Some(dir) => commands::set_2(&ctx, script_lang, env_var, false, Some(dir))?,
                    None => commands::set_2(&ctx, script_lang, env_var, false, None)?,
                },
            }
        }
    };
    std::process::exit(exit_code);
}
