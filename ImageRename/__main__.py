# type: ignore[attr-defined]
from typing import Optional

import os
from enum import Enum
from random import choice

import typer
from rich.console import Console

from ImageRename import version
from ImageRename.renamer import Renamer

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

def rename_image_callback(
    filepath: str,
    destination_dir: str = os.curdir,
    error_dir: str = os.curdir,
) -> None:
    """Rename one specific image."""
    f_path = Renamer().rename_image(
        filepath=filepath,
        destination_dir=destination_dir,
        error_dir=error_dir,
    )
    console.print(f"[bold green]Renamed image:[/]\n{f_path}")

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
    filepath: str = typer.Option(
        None,
        "-f",
        "--filepath",
        help="Path to the image file.",
    ),
    destination_dir: str = typer.Option(
        os.curdir,
        "-d",
        "--destination-dir",
        help="Path to the destination directory.",
    ),
    error_dir: str = typer.Option(
        os.curdir,
        "-e",
        "--error-dir",
        help="Path to the error directory.",
    ),
) -> None:
    """Rename images based on their date-time taken EXIF data."""
    if options:
        console.print(f"You passed an option: {options}")
    if filepath:
        rename_image_callback(
            filepath=filepath,
            destination_dir=destination_dir,
            error_dir=error_dir,
        )
    else:
        console.print(f"[bold red]No filepath given.[/]")

if __name__ == "__main__":
    app()