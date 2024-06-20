# Disk Stats Test

This repository contains a Python script that gathers data about a disk to verify its presence in the OS. Additionally, it includes a test case description for testing SSH connectivity using both password and key-based authentication methods.

## Completed has the following files

- `code.py`: A Python script that replaces the original `disk_stats_test.sh` and is written in PEP8 compliant Python3.
- `Testcase`: A test case description for testing SSH connectivity using password and key-based authentication.
- `output.png`: A screenshot showing the output of the `code.py` script and the PEP8 compliance check using Flask and Pylint.
- `README.txt`: Previsouly contained instructions to enter the new script; now includes the new Python script.

## Instructions

### Running the Script

To run the `code.py` script, execute the following command:

```bash
python3 code.py [disk]
```
-If no disk is specified, the script defaults to using sda

### Checking PEP8 Compliance
To check the PEP8 compliance of the code.py script, I have used flake and pylint. The output.png is a screenshot showing the output of the code.py script and the PEP8 compliance check using Flask and Pylint.

The Testcase file contains a detailed description of the test case for testing SSH connectivity using both password and key-based authentication methods. This includes the test scenario, setup and teardown procedures, tools used, and pass/fail criteria.
