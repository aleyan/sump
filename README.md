# SUMP(Summarizing Dump): Summarizing Source Code Projects

## Purpose

The Project Summary Generator is a Python utility designed to scan through a project's directory and generate a summary of the project's structure. It captures class names, function names, and signatures from TypeScript (TS) and Python (PY) files. Additionally, it respects `.gitignore` files to exclude unnecessary files from the summary. This tool is particularly useful for creating context files for feeding into language models (LLMs) or for getting a quick overview of a project's structure.

## Examples

### Generating a Summary for the Current Directory

To generate a summary for the current directory, simply run:

```sh
poetry run sump
```
