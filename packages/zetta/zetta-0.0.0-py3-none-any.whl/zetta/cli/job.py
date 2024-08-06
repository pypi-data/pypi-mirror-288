import typer
import zetta.job as zjob

job_cli = typer.Typer(name="container", help="Manage your jobs in Zetta Workspace.", no_args_is_help=True)


@job_cli.command("list")
async def list(json: bool = False):
    """List all jobs that are currently running."""
    pass
