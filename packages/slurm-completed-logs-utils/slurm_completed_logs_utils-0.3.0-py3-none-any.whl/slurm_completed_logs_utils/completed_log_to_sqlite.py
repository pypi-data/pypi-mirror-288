"""Parse the SLURM Completed Logs file and load into a table in SQLite."""
import click
import logging
import os
import pathlib
import sys
import yaml


from rich.console import Console

from sqlite.manager import Manager as SQLiteManager
from parser import Parser as SlurmCompletedLogsParser
from file_utils import check_infile_status
from console_helper import print_yellow, print_green
import constants


DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP
)


error_console = Console(stderr=True, style="bold red")

console = Console()


def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """

    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return constants.DEFAULT_VERBOSE
    return value


@click.command()
@click.option(
    "--config_file",
    type=click.Path(exists=True),
    help=f"The configuration file for this project - default is '{constants.DEFAULT_CONFIG_FILE}'",
)
@click.option(
    "--database_file",
    help="Optional: The SQLite3 database file - default will be [infile].sqlite3",
)
@click.option(
    "--infile",
    help="Required: The input SLURM Completed Logs text file to be parsed and loaded into the SQLite3 database",
)
@click.option("--logfile", help="Optional: The log file for the execution of this program.")
@click.option(
    "--outdir",
    help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'",
)
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{constants.DEFAULT_VERBOSE}'.", callback=validate_verbose)
def main(
    config_file: str,
    database_file: str,
    infile: str,
    logfile: str,
    outdir: str,
    verbose: bool,
):
    """Parse the SLURM Completed Logs file and load into a table in SQLite."""
    error_ctr = 0

    if infile is None:
        error_console.print("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(infile)

    if config_file is None:
        config_file = constants.DEFAULT_CONFIG_FILE
        print_yellow(f"--config_file was not specified and therefore was set to '{config_file}'")

    check_infile_status(config_file)

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        print_yellow(f"Created output directory '{outdir}'")

    if logfile is None:
        logfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".log"
        )
        print_yellow(f"--logfile was not specified and therefore was set to '{logfile}'")

    if verbose is None:
        verbose = constants.DEFAULT_VERBOSE
        print_yellow(f"--verbose was not specified and therefore was set to '{verbose}'")

    logging.basicConfig(
        filename=logfile,
        format=constants.DEFAULT_LOGGING_FORMAT,
        level=constants.DEFAULT_LOGGING_LEVEL,
    )

    # Read the configuration from the JSON file and
    # load into dictionary.
    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(pathlib.Path(config_file).read_text())

    if database_file is None:
        extension = config.get(
            "database_file_extension", constants.DEFAULT_DATABASE_FILE_EXTENSION
        )
        database_file = f"{os.path.join(infile)}.{extension}"
        print_yellow(f"--database_file was not specified and therefore was set to '{database_file}'")

    manager = SQLiteManager(
        config=config,
        config_file=config_file,
        outdir=outdir,
        logfile=logfile,
        infile=infile,
        database_file=database_file,
        verbose=verbose
    )

    parser = SlurmCompletedLogsParser()

    records = parser.get_records(infile)

    manager.load_records(records)

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()  # pragma: no cover
