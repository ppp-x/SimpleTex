# SimpleTex
The simplest, most basic text editor that supports very little but is a single Python file. It also highlights PHP and Bash syntaxes.

## What is SimpleTex
SimpleTex is a GUI plain text editor designed to be as little as possible. It is a single Python file that can be run on computers with very minimal resources. It is also perfect to be run over SSH (with -X flag) and can be installed without root privileges, as long as Python 3 and PyQt5 are available (PyQt5 can often also be installed without root privileges using Pip).

## Dependencies
- Python 3
- PyQt5

## Installation
Just download the file simpletex.py and place it anywhere.

## Usage
Run the following command:
`python3 /path/to/simpletex.py`

You can also add a filename as argument:
`python3 /path/to/simpletex.py /path/to/file.txt`

Alternatively, you can place this in a shell script to make it easier to run.

Simple keyboard shortcuts are available: CTRL+S saves your file and CTRL+Q quits the programme.
