import argparse
from pathlib import Path

from .runner import run_job


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Instagram influencer research pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a job from a JSON brief")
    run_parser.add_argument("job_file", type=Path, help="Path to inputs/job.json")
    run_parser.add_argument(
        "--env-file", type=Path, default=None, help="Optional path to .env file"
    )
    run_parser.add_argument(
        "--cache-ttl",
        type=int,
        default=86_400,
        help="Cache TTL in seconds (set 0 to disable caching)",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        run_job(args.job_file, env_file=args.env_file, cache_ttl_seconds=args.cache_ttl)


if __name__ == "__main__":
    main()

