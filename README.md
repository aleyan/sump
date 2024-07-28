# SUMP(Summarizing Dump): Summarizing Source Code Projects

## Purpose

The Project Summary Generator is a Python utility designed to scan through a project's directory and generate a summary of the project's structure. It captures class names, function names, and signatures from TypeScript (TS) and Python (PY) files. Additionally, it respects `.gitignore` files to exclude unnecessary files from the summary. This tool is particularly useful for creating context files for feeding into language models (LLMs) or for getting a quick overview of a project's structure.


## Installation globaly from source

```sh
pipx install --editable .
```

Then just run it with `sump`.

## Help

```
poetry run sump --help
Usage: sump [OPTIONS]

Options:
  -d, --directory TEXT    Directory to summarize
  -o, --output_file TEXT  Write summary to file
  -i, --include TEXT      Files to include fully
  --help                  Show this message and exit.
```

### Generating a Summary for the Current Directory

To generate a summary for the current directory, simply run:

```sh
poetry run sump
```
