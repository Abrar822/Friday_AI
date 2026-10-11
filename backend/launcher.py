
import argparse
import sys
from pathlib import Path

import uvicorn

# Project root: Friday/
ROOT = Path(__file__).resolve().parent.parent

# Make the project root available for backend imports.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=args.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
