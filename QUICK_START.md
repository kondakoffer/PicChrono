# Quick Start Guide

Welcome to the PicChrono project! This guide will provide you with the essential steps to quickly get started with using this project.

## Prerequisites

Before you begin, ensure that you have the following prerequisites installed:

- Python (version 3.10 or higher), refer to [python's website](https://www.python.org) to install it.
- pip, refer to [pip's official documentation](https://pip.pypa.io/en/stable/installing/) to install it.

## Installation

Install the package using pip:
```bash
pip install PicChrono
```
or 
```bash
pip install git+https://github.com/kondakoffer/PicChrono
```
It is recommended to use a virtual environment to install the package (see [here](https://docs.python.org/3/library/venv.html)).

## Usage

Once the package is installed, you can use it as follows:
```bash
PicChrono [OPTIONS] SOURCE_PATH [DESTINATION_DIR] [ERROR_DIR]  
```
- `SOURCE_PATH`: The path to the directory containing the photos you want to rename. You can also specify a single file by using its path.
- `DESTINATION_DIR`: The path to the directory where you want to save the renamed photos. If not specified, the photos will be stored in the current directory.
- `ERROR_DIR`: The path to the directory where you want to save the photos that could not be renamed. If not specified, the photos will be stored in the current directory.

### Options

- `--help`: Show the help message and exit.
- `-v` or `--version`: Show the version number and exit.

## Troubleshooting

If you encounter any issues or errors, here are a few troubleshooting tips:

- Double-check that package is installed correctly.
- Consult the project's documentation or issue tracker for common troubleshooting steps.
- If the issue persists, feel free to seek help through the project's support channels mentioned below.
    - Documentation: ***LINK TO DOCUMENTATION***  
    - Issue Tracker: https://github.com/kondakoffer/PicChrono/issues

## License
This project is licensed under the [MIT-LICENSE](LICENSE). Please review the license terms before using the project.
Since this project uses other packages, you must also agree and follow their license agreements. You can find the license agreements of the packages used in the [NOTICES.md](NOTICES.md) file.

## Support
We hope this Quick Start Guide helps you get up and running quickly with our project! If you have any questions or need further assistance, don't hesitate to reach out.
