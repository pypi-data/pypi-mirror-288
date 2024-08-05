# Py Utility Scripts

Python packaging is an essential method for sharing code, libraries, and applications. It facilitates the packaging of modules, enabling them to be published and deployed by other users, whether through binary files, source code, or package managers that fetch them from online repositories, both public and private.

In this repository, I demonstrate how to leverage the power of **setuptools**, a built-in Python library with robust functionalities for packaging and publishing code on the official Python repository, PyPI.

## Example Use Cases

Packaging your code offers several benefits, including:

- Easier management of release versioning
- Simplified shipping and deployment
- Automatic dependency management
- Increased code accessibility
- Support for cloud computing
- Facilitation of containerizing your application

## Code Example

This library contains various utility functions for handling Excel files, file operations, logging, and SQL connections.

### Features

- Create and write to Excel workbooks and worksheets
- Read specified columns from an Excel file and return data as a list of dictionaries
- Rename files in a specified directory to a sequentially numbered format with a user-defined prefix and format
- Provide flexible logging to both console and log file in JSON format with log file rotation
- Generate the structure of a given directory, following the provided Project Structure format
- MySQL functions for connecting to databases, logging middleware, executing queries, handling execution, and formatting responses

## Project Structure

The project is organized as follows:

    python-utility-functions/
      ├── .github
      │   ├── pypi-publish.yml
      │   └── test.pypi-publish.yml
      ├── app/
      │   ├── python_utils/
      │   │   ├── src/
      │   │   │   ├── __init__.py
      │   │   │   ├── excel_functions.py
      │   │   │   ├── file_functions.py
      │   │   │   ├── log_message.py
      │   │   │   ├── project_structure_generator.py
      │   │   │   └── sql_functions.py
      │   │   ├── tests/
      │   │   │   ├── __init__.py
      │   │   │   ├── test_excel_functions.py
      │   │   │   ├── test_file_functions.py
      │   │   │   ├── test_log_message.py
      │   │   │   ├── test_project_structure_generator.py
      │   │   │   └── test_sql_functions.py
      │   │   └── __init__.py
      │   ├── __init__.py
      │   ├── README.md
      │   └── requirements.txt
      ├── .gitignore
      ├── .env
      ├── CHANGELOG.md
      ├── LICENSE
      ├── README.md
      └── setup.py

## Building and Installing a Package (sdist, wheel)

### Setuptools

**setuptools** is a standard Python library that enhances the **distutils** library, making it easier to package Python projects.

Key concepts in **setuptools**:

- **wheel (.whl)**: A pre-built (zip) binary file containing all the necessary information (code and metadata) for Python package managers to install the package. Create one with `python setup.py bdist_wheel`. `bdist` stands for binary distribution.
- **sdist (.tar.gz)**: The source code distribution equivalent to a wheel, containing the source code and `setup.py` file. Create a source distribution with `python setup.py sdist`.

To generate both distributions, run:

    python setup.py bdist_wheel sdist

The output will be stored in the _dist_ folder created alongside `setup.py`.

### Building and Installing a Package

To build and install the package locally:

1. Run `python setup.py bdist_wheel sdist` to create both the source and binary files.
2. Install the package locally with `pip install .` under the directory containing `setup.py`.


## Introducing PyPI

[PyPI (Python Package Index)](https://pypi.org/) is a repository for Python software. It enables developers to find and install software shared by the Python community.

To publish a package, create an account on [PyPI](https://pypi.org/) and, for testing purposes, [TestPyPI](https://test.pypi.org/). Configure a `.pypirc` file for automatic authentication when uploading packages.

Example `.pypirc` file:

    [distutils]
    index-servers =
        pypi
        pypitest

    [pypi]
    repository = https://upload.pypi.org/legacy/
    username = <your-pypi-username>
    password = <your-pypi-password>

    [pypitest]
    repository = https://test.pypi.org/legacy/
    username = <your-test-pypi-username>
    password = <your-test-pypi-password>


- Alternatively you can create [GitHub actions](.github) to publish your package in [PyPI](https://pypi.org/)/[TestPyPI](https://test.pypi.org/).


## Publishing the Package on PyPI

- Ensure twine is installed. Run `pip install .[dev]`. (Twine is declared as a development dependency, so that will install it automatically together with the package itself.)
- Check the package with `twine check dist/*` , to ensure both the source and wheel files pass.
- Upload to TestPyPI with `twine upload --repository testpypi dist/*`. Ensure a `.pypirc` file is configured. (If you try to publish the same version name as already published, TestPyPI won’t allow it and you’ll get an error.)
- Visit your package’s TestPyPI webpage to verify the upload.

To test the package, create a new environment and install it using pip.

## Contributing

This code is packaged for personal use and to assist other developers. Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## Contact

- LinkedIn: [Hirushiharan Thevendran](linkedin.com/in/hirushiharan-thevendran-a08a82152)
- Email: [hirushiharant@gmail.com](hirushiharant@gmail.com)
