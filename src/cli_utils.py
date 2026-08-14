"""
CLI helper utilities — argument parsing and validation.
"""

import argparse
import os


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the pipeline CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, help="Ask a single question and exit")
    return parser.parse_args()


def validate_data_dir(data_dir: str) -> bool:
    """Return True if data_dir exists, printing an error if not."""
    if not os.path.isdir(data_dir):
        print(f"Error: data directory not found at {data_dir}")
        return False
    return True