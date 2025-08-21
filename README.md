# Introduction
This is the central backend service that acts as a bridge between a client and services. 

## Features included
- **Repository layer** that provides connections to Databases
- **Service layer** that provides connectors (to 3rd party services, and other internal services like Data etc).

## Installation
The project use **pip-tools** to generate .txt files which can be  used to install
packages in your virtual env. We need to install this in our global Python.

**Steps:**
1. Add the package you need to base.in file and generate (or update) the base.txt file
    ```bash
    pip-compile requirements/base.in --output-file=requirements/base.txt
    ```
2. Install in your env the new packages
    ```bash
    pip install -r .\requirements\base.txt
    ```
## Run tests
To run tests, you can use the following command:

```bash
pytest
pytest -s # to see print statements
coverage run -m pytest # to see coverage
coverage html
```