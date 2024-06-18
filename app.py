import os
import argparse


from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.document_loaders import GitLoader

from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn
from dotenv import load_dotenv

from utils.filter import file_filter
from utils.chain import invoke_chain

load_dotenv()

ollama_host = os.getenv("OLLAMA_HOST") or "http://127.0.0.1:11434"

parser = argparse.ArgumentParser(
    description="Generate documentation for a set of documents.")

parser.add_argument(
    "--git-repo",
    required=True,
    type=str,
    help="Path to the git repository containing the documents to generate documentation for.",
)


parser.add_argument(
    "--file-filter",
    required=True,
    type=str,
    help="Filter for the files in the git repository to generate documentation for.",
)

args = parser.parse_args()

if args.git_repo is None:
    parser.error("Please provide a path to the git repository.")


with Progress(
    TextColumn("🖋️ [progress.description]{task.description}"),
    BarColumn(style="yellow1", pulse_style="white"),
    TimeElapsedColumn(),
) as progress:
    progress.add_task(
        f"[yellow] Starting loading codebase from git repository and running the chain...", total=None)

    # Load documents from a git repository
    loader = GitLoader(
        repo_path=args.git_repo,
        file_filter=lambda file_path: file_filter(file_path, args),
        branch="master"
    )

    llm = ChatOllama(
        model="mistral:7b",
        base_url=ollama_host,
    )

    result = invoke_chain(loader, llm)

    with open("documentation.md", "w") as f:
        f.write(result["output_text"])

print(
    f"✨ Documentation successfully generated! Check the output.txt file for the result. ✨"
)
