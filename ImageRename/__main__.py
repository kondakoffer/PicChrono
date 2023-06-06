# type: ignore[attr-defined]
from typing import Optional

from enum import Enum
from random import choice

import typer
from rich.console import Console

from ImageRename import version
from ImageRename.renamer import cnt

class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="ImageRename",
    help="Rename images based on their date-time taken EXIF data.",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]ImageRename[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command()
def main(
    options: Optional[str] = typer.Option(
        None,
        "-o",
        "--options",
        help="Here should be the options for the ImageRename command.",
    ),
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the ImageRename package.",
    ),
) -> None:
    """Rename images based on their date-time taken EXIF data."""
    console.print(f"[bold green]Options:[/]\n{options}")

if __name__ == "__main__":
    app()