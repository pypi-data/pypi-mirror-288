from setuptools import setup, find_packages

# Read the requirements
with open("app/requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Read the README
with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="py_utility_scripts",
    version="1.4.0",
    description="A collection of utility scripts for working with files, Excel, logging, and database connections.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hirushiharan/python-utility-functions.git",
    author="Hirushiharan",
    author_email="hirushiharant@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    extras_require={
        "dev": ["pytest", "twine"],
    },
    python_requires=">=3.11",    
)
