from argparse import Namespace


def file_filter(file_path: str, args: Namespace) -> bool:
    if args.file_filter:
        return file_path.endswith(args.file_filter)

    # ignore hidden files or directories
    if file_path.startswith('.'):
        return False

    return False
