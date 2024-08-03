# Py Utility Scripts

Python packaging is the most common way to share code/libraries/applications. It allows packaging of the modules so they can later be published and deployed by other users, either by sharing binary files, source code, or by using a package manager to fetch them from online (public or private) repositories.

The recommended way to package your code is by using the built-in Python library _setuptools_, which has many powerful functionalities.

In this repository, I'll show you how to harness some of the power of _setuptools_ so that you can package and publish your code on the official Python repository _PyPI_.

## Example Use Cases (Where Packaging is a Must)

- Easier management of release versioning
- Shipping and deployment become pretty simple
- Automatic dependency management
- Increase your code’s accessibility
- Cloud computing
- Containerizing your application

## Code Example

This library contains various utility functions for handling Excel files, file operations, logging, and SQL connections.

### Features:

- Read specified columns from an Excel file and return data as a list of dictionaries.
- Create and write to Excel workbooks and worksheets.
- Rename files in a specified directory to a sequentially numbered format with a user-defined prefix and format.
- Provide flexible logging to both console and log file in JSON format with log file rotation.
- Generate structure of the given directory same as below provided Project Structure format.

## Project Structure

The project is structured as follows:

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
      │   │   │   └── project_structure_generator.py
      │   │   ├── tests/
      │   │   │   ├── __init__.py
      │   │   │   ├── test_excel_functions.py
      │   │   │   ├── test_file_functions.py
      │   │   │   ├── test_log_message.py
      │   │   │   └── test_project_structure_generator.py
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

_setuptools_ is a (now standard) Python library that facilitates packaging Python projects by enhancing the _distutils_ library.

Important keywords/parameters of _setuptools_ to be aware of:

- **wheel (.whl)**: A pre-built (zip) binary file, which is ready to be installed, that contains all the necessary information (code itself and metadata) for Python package manager to install the package. To create one you should run `python setup.py bdist_wheel` within the shell. `bdist` stands for binary distribution.
- **sdist (.tar.gz)**: The source code distribution equivalent to wheel. A tar file (zip) that contains the source code together with the `setup.py` file, so the user can re-build it. To create a source distribution run `python setup.py sdist`.

The above two commands can be combined into one if both distributions are desired. The output will be stored within the _dist_ folder that _setuptools_ will create in the same level where `setup.py` resides.

- **build folder**: Contains all the source code/modules that will be distributed.
- **egg-info**: A directory placed adjacent to the project's code and resources, that directly contains the project's metadata. Replaced by wheels.

### Building and Installing a Package

- Run `setup.py` using `python setup.py bdist_wheel sdist` command. This creates both source code files and binary (.whl) file.
- Then install the package locally by running `pip install .` under the directory where `setup.py` lives and will install your package directly, and can test the package locally.

## Introducing PyPI

- PyPI (Python Package Index) is a repository of software for the Python programming language. It helps you find and install software developed and shared by the Python community.
- You can browse and search for packages on [PyPI](https://pypi.org/). Each package's page provides metadata about the package, including its version history, dependencies, and installation instructions.
- When you run `pip install <PACKAGE_NAME>>`, you are basically fetching from PyPI.
- To publish a package, you need to create an account on [PyPI](https://pypi.org/). It’s recommended to first create a [TestPyPI](https://test.pypi.org/) account, so that you don’t publish under the official repository while testing.
- For convenience and security, you can configure/create a `.pypirc` file for automatic authentication when uploading your package to the repository. This also helps in keeping your token private.

```
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
```

- Alternatively you can create [GitHub actions](.github) to publish your package in [PyPI](https://pypi.org/)/[TestPyPI](https://test.pypi.org/).


## Publishing the Package on PyPI

- Make sure you have _twine_ installed. Run `pip install .[dev]`. Twine is declared as a development dependency, so that will install it automatically together with the package itself.
- Run `twine check dist/*` , you should see tests passed for both source code and wheel file.
- Run `twine upload --repository testpypi dist/*`. Assuming you have a `.pypirc` file configured, that should work and publish your package to the TestPyPI repo.
- Note: If you try to publish the same version name as already published, TestPyPI won’t allow it and you’ll get an error.
- Visit your package’s webpage so that viewers can see how the package looks published.
- You can also create a new environment and install the newly published package via pip. You can do the same within the existing environment but always more neat to do on a fresh environment.


## Contributing

I am packaging this code for my own use to use in a different environment. Also, other developers can use it if needed. Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## Contact

- LinkedIn: [Hirushiharan Thevendran](linkedin.com/in/hirushiharan-thevendran-a08a82152)
- Email: [hirushiharant@gmail.com](hirushiharant@gmail.com)
