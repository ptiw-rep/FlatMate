# FlatMate

A Python script to generate structured Markdown documentation from a project's source code, optionally including a text-based directory tree.

## Features

- Recursively scans a project directory and extracts code into a Markdown file.
- Supports syntax highlighting for multiple programming languages.
- Reads `.gitignore` to exclude ignored files and directories.
- Generates a visual directory tree at the beginning of the output.
- Logs the process for better debugging and transparency.

## Requirements

- Python 3.6+

## Installation

Clone the repository or copy the script to your local machine.

## Usage

Run the script with the following command:

```sh
python app.py [project_dir] [output_file]
```

### Arguments

- `project_dir` (optional) – The root directory of the project to document (default: current directory `.`).
- `output_file` (optional) – The name of the generated Markdown file (default: `flattened.md`).

### Example

```sh
python app.py my_project docs.md
```

This generates `docs.md` with a directory tree and source code content.

## Output Structure

The generated documentation consists of:

1. **Project File Structure** – A hierarchical representation of included files.
2. **Concatenated Code Files** – Each file's content in Markdown format with appropriate syntax highlighting.

### Sample Output

```md
# Project File Structure
```

└── src/ │   └── main.py │   └── utils.py └── README.md

````

## File: src/main.py
```python
# This is the main Python script
print("Hello, World!")
````

```

## Logging
The script provides logging for better debugging:
- **INFO**: Process updates.
- **WARNING**: Missing `.gitignore` or minor issues.
- **ERROR**: Critical failures such as unreadable files.

## License
This project is licensed under the MIT License. See `LICENSE` for details.
---

```
