# PicChrono

<center>

[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-black-black.svg)](https://github.com/psf/black)
[![Coverage](./assets/badges/coverage.svg)](./assets/badges/coverage.svg)
[![Testing](https://img.shields.io/badge/Testing-PyTest-olive.svg)](https://docs.pytest.org/)

</center>

-----------------

## :books: Description
A python package helping you to archive your photos. It renames the photos based on the date and time they were taken.

## :rocket: Quickstart
Please follow the [quickstart guide](QUICK_START.md).

## :wrench: Installation
```bash
pip install picchrono
pip install git+https://github.com/kondakoffer/PicChrono
```

## :gear: Usage
Install the package as explained above. Then, you can use the package as follows:
```bash
PicChrono [OPTIONS] SOURCE_PATH [DESTINATION_DIR] [ERROR_DIR]  
```
- `SOURCE_PATH`: The path to the directory/file (containing) the photos you want to rename.
- `DESTINATION_DIR`: The path to the directory where you want to save the renamed photos. If not specified, the photos will be stored in the current directory.
- `ERROR_DIR`: The path to the directory where you want to save the photos that could not be renamed. If not specified, the photos will be stored in the current directory.

Use `PicChrono --help` to see the help message.

### Options
- `--help`: Show the help message and exit.
- `--version`: Show the version of PicChrono and exit.

## :test_tube: Testing
Explain how to run tests, and provide examples if necessary.

## :pencil: Contributing
Contributions are welcome! Please follow the [contributing guidelines](CONTRIBUTING.md).

## :sparkles: Code of Conduct
Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before contributing to this project.

## :scroll: License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## :page_with_curl: Citation
If you use this project in your research, please cite it using the following BibTeX entry:
```
@misc{your_bibtex_entry,
  author = {Your Name},
  title = {Your Project's Title},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished =
}
```

## :email: Contact
If you have any questions or suggestions, feel free to reach out.

## :star: Acknowledgements
Give credit to any resources or individuals that helped inspire or contribute to the project.

## :link: Useful Links
Include any relevant links to documentation, tutorials, or related resources.
