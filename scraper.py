import argparse

from src.data_sources import DataSources


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command", type=str,
        choices=[
            "list",
            "snapshot", "dump-snapshot", "dump-snapshot-table",
            "snapshot-status", "changes-status",
            "dump-convert", "dump-convert-meta", "dump-changes",
            "debug"
        ],
        help="Command to execute",
    )

    parser.add_argument(
        "-i", "--include", type=str, nargs="+",
        help="wildcard pattern for sources to include"
    )
    parser.add_argument(
        "-e", "--exclude", type=str, nargs="+",
        help="wildcard pattern for sources to exclude"
    )
    parser.add_argument(
        "-it", "--include-type", type=str, nargs="+",
        help="wildcard pattern for source types to include"
    )
    parser.add_argument(
        "-df", "--date-from", type=str,
        help="date string to limit considered snapshots. snapshot-date >= date-from"
    )
    parser.add_argument(
        "-dt", "--date-to", type=str,
        help="date string to limit considered snapshots. snapshot-date < date-to"
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

    parser.add_argument(
        "--resample", type=str, default=None,
        help="pandas time resampling option for 'dump-changes' mode"
    )

    return parser.parse_args()


def main(args):
    sources = DataSources(
        use_cache=args.cache,
        include=args.include,
        exclude=args.exclude,
        include_type=args.include_type,
        date_from=args.date_from,
        date_to=args.date_to,
    )

    if args.command == "list":
        sources.dump_list()

    elif args.command == "snapshot":
        sources.make_snapshot(num_weeks=args.weeks, processes=args.processes)

    elif args.command == "dump-snapshot":
        sources.dump_snapshot(num_weeks=args.weeks)

    elif args.command == "dump-snapshot-table":
        sources.dump_snapshot_table(num_weeks=args.weeks)

    elif args.command == "snapshot-status":
        sources.dump_snapshot_status()

    elif args.command == "changes-status":
        sources.dump_changes_status()

    elif args.command == "dump-convert":
        sources.dump_convert_snapshots()

    elif args.command == "dump-convert-meta":
        sources.dump_convert_snapshots_meta()

    elif args.command == "dump-changes":
        sources.dump_snapshot_changes(resample=args.resample)

    elif args.command == "debug":
        sources.dump_snapshot_dates()
    else:
        print(f"Invalid command '{args.command}'")
        exit(1)


if __name__ == "__main__":
    main(parse_args())