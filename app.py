import fnmatch
import os
import logging
import pathlib
import argparse

DEFAULT_GITIGNORE_TXT_PATH = "./ignore.txt"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_language_extension(file: str) -> str:
    """Determines the language extension for Markdown code blocks based on file extension."""
    extensions = {
        ".py": "python", ".js": "javascript", ".html": "html", ".css": "css",
        ".java": "java", ".cpp": "cpp", ".c": "c", ".sh": "bash", ".R": "r",
        ".cs": "csharp", ".go": "go", ".php": "php", ".rb": "ruby", ".rs": "rust",
        ".sql": "sql", ".swift": "swift", ".ts": "typescript", ".vb": "vb",
        ".xml": "xml", ".yml": "yaml", ".yaml": "yaml"
    }
    return extensions.get(pathlib.Path(file).suffix, "")


def read_gitignore(gitignore_path: str) -> list:
    """Reads a .gitignore file and returns a list of patterns to ignore."""
    ignore_patterns = []
    try:
        with open(gitignore_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore_patterns.append(line)
        logging.info(f"Loaded {len(ignore_patterns)} ignore patterns from {gitignore_path}")
    except FileNotFoundError:
        logging.warning(f".gitignore not found at {gitignore_path}, using default ignore list.")
    return ignore_patterns


def should_ignore(path: str, ignore_patterns: list) -> bool:
    """Determines if a given path should be ignored based on .gitignore patterns."""
    path = pathlib.Path(path).as_posix()  # Convert to POSIX format for consistency
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern) or any(part in pattern for part in path.split("/")):
            return True
    return False


def format_directory_structure(directory: str, ignore_patterns: list) -> str:
    """Creates a structured representation of the directory tree, excluding ignored paths."""
    
    def recurse_folder(current_dir: str, indent_level: int) -> str:
        tree_str = ""
        try:
            for item in sorted(os.listdir(current_dir)):
                item_path = os.path.join(current_dir, item)
                if should_ignore(item_path, ignore_patterns):
                    continue
                if os.path.isdir(item_path):
                    tree_str += "│   " * indent_level + f"└── {item}/\n"
                    tree_str += recurse_folder(item_path, indent_level + 1)
                else:
                    tree_str += "│   " * indent_level + f"└── {item}\n"
        except OSError as e:
            tree_str += f"│   " * indent_level + f"└── Error accessing folder: {e}\n"
            logging.error(f"Error accessing {current_dir}: {e}")
        return tree_str

    return recurse_folder(directory, 0)


def concatenate_files_to_markdown(directory: str, ignore_patterns: list) -> str:
    """Concatenates all files in a directory into a Markdown string, excluding ignored paths."""
    markdown_content = ""
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if should_ignore(file_path, ignore_patterns):
                continue
            
            language = get_language_extension(file)
            markdown_content += f"\n\n## File: {file_path}\n"
            markdown_content += f"```{language}\n" if language else "```\n"
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as infile:
                    markdown_content += infile.read()
            except Exception as e:
                markdown_content += f"Error reading file: {e}\n"
                logging.error(f"Failed to read {file_path}: {e}")

            markdown_content += "\n```"
    
    logging.info("Finished concatenating files.")
    return markdown_content


def create_doc_file(
    root_path: str, save_path: str, include_file_tree: bool = True
) -> str:
    """Generates documentation for a project, excluding paths in .gitignore."""
    
    gitignore_path = os.path.join(root_path, ".gitignore")
    if not os.path.exists(gitignore_path):
        gitignore_path = os.path.join(root_path, DEFAULT_GITIGNORE_TXT_PATH)
    
    ignore_patterns = read_gitignore(gitignore_path)
    
    try:
        # Generate file tree first
        file_tree = format_directory_structure(root_path, ignore_patterns)
        file_tree_section = f"# Project File Structure\n```\n{file_tree}```\n\n"
        
        # Generate documentation content
        documentation = concatenate_files_to_markdown(root_path, ignore_patterns)
        
        if include_file_tree:
            documentation = file_tree_section + documentation

        with open(save_path, "w", encoding="utf-8") as file:
            file.write(documentation)
        logging.info(f"Documentation saved at {save_path}")

        return documentation
    except Exception as e:
        logging.error(f"Error generating documentation: {e}")
        raise Exception(f"Error generating documentation: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Markdown file containing all source code in a directory.")
    parser.add_argument("project_dir", nargs="?", default=".", help="Path to the project directory (default: current directory).")
    parser.add_argument("output_file", nargs="?", default="flattened.md", help="Output file name (default: flattened.md).")

    args = parser.parse_args()

    logging.info(f"Generating documentation for {args.project_dir}...")
    create_doc_file(args.project_dir, args.output_file)
    logging.info("Documentation generation complete.")
