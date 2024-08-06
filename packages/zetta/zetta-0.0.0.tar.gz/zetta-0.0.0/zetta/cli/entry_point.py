import click
import typer

from . import run
from .job import job_cli
from .model import model_cli
from .secret import secret_cli

from zetta.version import __version__


entrypoint_cli_typer = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="markdown",
    help="""
    Zetta stands for a better AI economics

    See the website at https://zettablock.com/ for documentation and more information
    about running code on ZettaBlock AI network.
    """,
)


def version_callback(value: bool):
    if value:
        from zetta_version import __version__

        typer.echo(f"zetta client version: {__version__}")
        raise typer.Exit()


@entrypoint_cli_typer.callback()
def zetta(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    pass


# Deployments
entrypoint_cli_typer.add_typer(job_cli, rich_help_panel="Deployments")


entrypoint_cli = typer.main.get_command(entrypoint_cli_typer)
entrypoint_cli.list_commands(None)  # type: ignore


if __name__ == "__main__":
    # this module is only called from tests, otherwise the parent package __main__.py is used as the entrypoint
    entrypoint_cli()
