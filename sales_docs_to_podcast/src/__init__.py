import argparse
from pathlib import Path

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process a file given by a relative path."
    )
    parser.add_argument(
        "input_path",
        help="Relative path to the input file (e.g., ./data/input.txt)",
    )
    return parser.parse_args(argv)


def get_path(argv: list[str] | None = None):
    args = parse_args(argv)

    # Resolve relative path against current working directory
    raw_path = Path(args.input_path)
    path = (Path.cwd() / raw_path).resolve(strict=True) if not raw_path.is_absolute() else raw_path.resolve(strict=True)
    return path, path.name

def get_input_file_content(path: Path):
    with open(path, "r", encoding="UTF-8") as f:
        file_content = f.read()
    return file_content