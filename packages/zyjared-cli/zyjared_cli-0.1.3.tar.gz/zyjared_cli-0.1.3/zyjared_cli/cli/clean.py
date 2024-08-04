import typer
from typing import List, Optional, Annotated
from .app import app
from ..core.clean import clean as zy_clean


@app.callback()
def callback():
    """
    zyjared's tool
    """


@app.command()
def clean(
    dirpath: Annotated[
        str,
        typer.Argument(
            default=...,
            show_default=False,
            help="Specify the directory to clean up.",
        )
    ],
    include: Annotated[
        List[str],
        typer.Option(
            '-i',
            '--include',
            show_default=False,
            help="Regular expression to include files.",
        )
    ],
    exclude: Annotated[
        Optional[List[str]],
        typer.Option(
            '-e',
            '--exclude',
            help="Regular expression to exclude files",
        )
    ] = []
):
    """
    Clean up files in a directory with specified include.
    """
    zy_clean(dirpath, include, exclude)


@app.command()
def echo():
    """
    Echo 'hello world'.
    """
    typer.echo("hello world")
