import argparse

from src.data_sources import DataSources


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command", type=str,
        choices=["list", "snapshot", "dump-snapshot", "snapshot-status"],
        help="Command to execute",
    )

    parser.add_argument(
        "-i", "--include", type=str,
        help="wildcard pattern for sources to include"
    )
    parser.add_argument(
        "-e", "--exclude", type=str,
        help="wildcard pattern for sources to exclude"
    )

    parser.add_argument(
        "-w", "--weeks", type=int, default=4,
        help="Number of weeks to look ahead"
    )

    parser.add_argument(
        "-c", "--cache", type=bool, nargs="?", default=False, const=True,
        help="Enable caching of websites"
    )

    parser.add_argument(
        "-p", "--processes", type=int, default=1,
        help="Multiple processes for snapshot mode"
    )

    return parser.parse_args()


def main(args):
    sources = DataSources(
        use_cache=args.cache,
        include=args.include,
        exclude=args.exclude,
    )

    if args.command == "list":
        sources.dump_list()

    elif args.command == "snapshot":
        sources.make_snapshot(num_weeks=args.weeks, processes=args.processes)

    elif args.command == "dump-snapshot":
        sources.dump_snapshot(num_weeks=args.weeks)

    elif args.command == "snapshot-status":
        sources.dump_snapshot_status()

    else:
        print(f"Invalid command '{args.command}'")
        exit(1)


if __name__ == "__main__":
    main(parse_args())