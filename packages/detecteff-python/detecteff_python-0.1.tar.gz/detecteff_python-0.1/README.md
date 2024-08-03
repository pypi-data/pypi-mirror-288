# Overview

`Detecteff` was originally written in rust but now has python bindings.

This was created for a Freelancing Job and is a command-line utility to find duplicate files in a directory and delete them.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Cases](#cases)
- [Caution](#caution)

## Features
- Optional Recursive scan
- Default output and a formatted output choice
- Thorough
- super fast (rust backend)
- Ability to ignore directories
- Auto-ignore Directories whose name starts with `.` as they are not to be messed with

>NOTE: If scanning the `HOME` directory of your OS, be careful as some directories shouldn't be messed with like the `Library` and `Applications` folder in macOS. Try scanning individual directories in the home directory.

**ADDITIONAL NOTE**:
- Avoid scanning OS directories or any application installation directory or else it might result in tampering with important files.
- Before using --delete or -d flag to delete the temp files, check the list of files that will be deleted (white background, red foreground) that will be printed after scanning.

For Full Documentation on Errors and Bug Fixes, refere [here](https://github.com/d33pster/detecteff).

## Installation

> Run the following code in Terminal

```bash
pip install detecteff-python
```

## Usage

> The Installation will build a bin called `detectf`. Run help to see full help

```bash
$ detectf --help
detecteff help
   -
   [INFO]
   | -h, --help : show help text and exit.
   | -v, --version : show version and exit.
   -
   [FLAG]
   | -r, --recursive : recursive mode. Default -> OFF
   | -fmt, --formatted : show formatted output. Default -> OFF
   -
   [INPUT]
   | -s, --scan <directory> : scan the directory for duplicate files. (Mandatory)
   | -i, --ignore <directory1>, <directory2>, ... : ignore these directories. (Optional)
   -
   [IRREVERSIBLE FLAG]
   | -del, --delete : delete any found duplicates. Default -> OFF
```

## Cases

> scanning a specific directory

`Normal`

```bash
detectf --scan <directory>
```

`Recursive`

```bash
detectf --scan <directory> --recursive
```

`Better Formatting`

```bash
detectf --scan <directory> --formatted
```

`Ignoring directories`

```bash
detectf --scan <directory> --ignore <dir1> <dir2> ...
```

`Deleting Duplicates on the go`

This is irreversible command!

```bash
detectf --scan <directory> --ignore <dir1> <dir2> --delete
```

## Caution

- Try to avoid scanning directories that contain system files like the `Applications` or `Library` directory in macos.

- Try to avoid scanning directories that contain source code binaries.

- Try to avoid scanning the `HOME` directory of your OS as it may contain several of those directories mentioned in point 1 and 2. If important, then scan it individual directories at a time or add the trouble making directories in the `ignore` argument.

- Try not to scan entire Filesystem, This is not made for that.