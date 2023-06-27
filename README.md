# PicChrono

[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-black-black.svg)](https://github.com/psf/black)
[![Coverage](./assets/badges/coverage.svg)](./assets/badges/coverage.svg)
[![Testing](https://img.shields.io/badge/Testing-PyTest-olive.svg)](https://docs.pytest.org/)


## Description
A python package helping you to archive your photos. It renames the photos based on the date and time they were taken.

## Prerequisites
Before you begin, ensure that you have the following prerequisites installed:

- Python (version 3.10 or higher), refer to [python's website](https://www.python.org) to install it.
- pip, refer to [pip's official documentation](https://pip.pypa.io/en/stable/installing/) to install it.

## Installation
Install the package using pip:
```bash
pip install pic-chrono
```
or 
```bash
pip install git+https://github.com/kondakoffer/PicChrono
```
It is recommended to use a virtual environment to install the package (see [here](https://docs.python.org/3/library/venv.html)).

## Usage
Once the package is installed, you can use it as a command line tool or as a python package.

### As command line tool
The intended usage is as command line tool. You can use it as follows:
```bash
PicChrono [OPTIONS] SOURCE_PATH [DESTINATION_DIR] [ERROR_DIR]  
```
- `SOURCE_PATH`: The path to the directory containing the photos you want to rename. You can also specify a single file by using its path.
- `DESTINATION_DIR`: The path to the directory where you want to save the renamed photos. If not specified, the photos will be stored in the current directory.
- `ERROR_DIR`: The path to the directory where you want to save the photos that could not be renamed. If not specified, the photos will be stored in the current directory.

#### Options
- `--help`: Show the help message and exit.
- `-v` or `--version`: Show the version number and exit.

### As python package
It is also possible to integrate the package into your own python code by using the typical python import statement:
```python
import pic_chrono
```
If you only want to use the functionalities with renaming the photos, you can import the `Rename` class:
```python
from pic_chrono.renamer import Rename
```

<!-- For an extended documentation of the package, please refer to ***ADD LINK TO DOCS***. -->

## Troubleshooting
If you encounter any issues or errors, here are a few troubleshooting tips:

- Double-check that package is installed correctly.
- Consult the project's documentation or issue [tracker](https://github.com/kondakoffer/PicChrono/issues) for common troubleshooting steps.
- If the issue persists, feel free to open a new issue [here](https://github.com/kondakoffer/PicChrono/issues).

## Contributing
Any contributions are welcome! 
Please follow the [contributing guidelines](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).

## License
This project is licensed under the [MIT-LICENSE](LICENSE). 
Please review the license terms before using the project.
Since this project uses other packages, you must also agree and follow their license agreements. You can find the license agreements of the packages used in the [NOTICES.md](NOTICES.md) file.

## Acknowledgements
Since this project uses other software and packages, we would like to thank the authors of these for their work.
This includes [Poetry](https://python-poetry.org/), [Python](https://www.python.org/), [Pillow](https://python-pillow.org/), [Typer](https://typer.tiangolo.com/), [rich](https://github.com/Textualize/rich), [pytest](https://docs.pytest.org/), [pytest-cov](https://github.com/pytest-dev/pytest-cov), [black](https://github.com/psf/black), [coverage-badge](https://github.com/dbrgn/coverage-badge).
