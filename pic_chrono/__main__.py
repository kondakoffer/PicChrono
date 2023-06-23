# type: ignore[attr-defined]
from typing import Optional

import os
from enum import Enum
from random import choice

import typer
from typing_extensions import Annotated
from rich.console import Console

from pic_chrono import version
from pic_chrono.renamer import Renamer


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


def rename_dir_callback(
    source_dir: str,
    destination_dir: str = os.curdir,
    error_dir: str = os.curdir,
) -> None:
    """Rename all images in a directory."""
    Renamer().rename(
        source_dir=source_dir,
        destination_dir=destination_dir,
        error_dir=error_dir,
    )


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
    source_path: str = typer.Argument(
        ...,
        help="Path to the file or directory which (contents) should be renamed.",
    ),
    destination_dir: str = typer.Argument(
        os.curdir,
        help="Path to the directory where the renamed files should be stored.",
    ),
    error_dir: str = typer.Argument(
        os.curdir,
        help="Path to the directory where the files which could not be renamed should be stored.",
    ),
) -> None:
    """Rename images based on their date-time taken EXIF data."""
    if options:
        # console.print(f"You passed an option: {options}")
        pass
    else:
        if not os.path.exists(source_path):
            console.print(f"[bold red]Source path does not exist:[/]\n{source_path}")
            raise typer.Exit(code=1)
        if os.path.isfile(source_path):
            rename_image_callback(
                filepath=source_path,
                destination_dir=destination_dir,
                error_dir=error_dir,
            )
        elif os.path.isdir(source_path):
            rename_dir_callback(
                source_dir=source_path,
                destination_dir=destination_dir,
                error_dir=error_dir,
            )


if __name__ == "__main__":
    app()
