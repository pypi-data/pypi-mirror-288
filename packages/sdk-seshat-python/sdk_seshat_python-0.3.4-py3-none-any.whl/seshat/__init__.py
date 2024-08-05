import os.path

import typer

from seshat.general.command.base import RECOMMENDATION, SetUpProjectCommand

app = typer.Typer()

state = {"verbose": False}


@app.command(name="create-project")
def create_project(name: str, usecase=typer.Option(default=RECOMMENDATION)):
    command = SetUpProjectCommand(name, usecase, os.getcwd(), report=state["verbose"])
    try:
        command.handle()
    except Exception as exc:
        cli_msg = typer.style(
            f"Setup project in usecase {usecase} failed because of {str(exc)}",
            fg=typer.colors.RED,
            bold=True,
        )
    else:
        cli_msg = typer.style(
            f"""
            Setup project in usecase {usecase} done!\n
            You can deploy your project by this command 🚀:
            'python -m seshat deploy`
            """,
            fg=typer.colors.GREEN,
            bold=True,
        )
    typer.echo(cli_msg)


@app.callback()
def main(verbose: bool = False):
    state["verbose"] = verbose


@app.command()
def deploy():
    pass
