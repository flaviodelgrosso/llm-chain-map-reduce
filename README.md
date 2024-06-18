# Documentation Generator

This tool automates the generation of comprehensive documentation for software projects by analyzing codebases hosted in git repositories. It leverages large language models (LLMs) to produce detailed, functional documentation aimed at software developers.

## Features

- **Git Repository Support**: Load documents directly from a specified git repository.
- **File Filtering**: Specify a filter to only include certain files from the git repository in the documentation process.
- **Progress Tracking**: Visual progress tracking with rich text support.
- **Large Language Model Integration**: Uses ChatOllama for generating and refining documentation content.
- **Map-Reduce Paradigm**: Implements a map-reduce approach for processing and combining documentation from multiple sources.

## Requirements

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- All Python dependencies listed in `requirements.txt`

## Installation

1. Clone this repository or download the source code.
2. Install the required Python packages:
3. Set up the .env file based on .env.example to include your specific configurations such as the OLLAMA_HOST.

```sh
pip install -r requirements.txt
```

## Usage

To generate documentation, run the script with the necessary arguments:

```sh
python app.py --git-repo <path-to-git-repo> [--file-filter <file-extension>]
```

- `--git-repo`: Path to the git repository containing the documents.
- `--file-filter` (optional): Filter for the files in the git repository to generate documentation for (e.g., .py for Python files).
The generated documentation will be saved in output.txt.
