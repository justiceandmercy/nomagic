"""Command-line interface for nomagic."""

import argparse
import json
import sys

from .scanner import scan_path


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="nomagic",
        description="Detect magic numbers in source code.",
    )
    parser.add_argument("path", nargs="?", default=".",
                        help="file or directory to scan (default: .)")
    parser.add_argument("--json", action="store_true",
                        help="emit findings as JSON")
    parser.add_argument("--allow", default="",
                        help="comma-separated numbers to allow")
    parser.add_argument("--ext", default="",
                        help="comma-separated extensions to scan (e.g. .py,.js)")
    args = parser.parse_args(argv)

    extra = [x.strip() for x in args.allow.split(",") if x.strip()]
    exts = None
    if args.ext:
        exts = {e.strip() if e.strip().startswith(".") else "." + e.strip()
                for e in args.ext.split(",") if e.strip()}

    findings = scan_path(args.path, extra_allowed=extra, exts=exts)

    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        if not findings:
            print("No magic numbers found.")
        else:
            for f in findings:
                print(f'{f["file"]}:{f["line"]}: magic number {f["number"]}'
                      f' -> {f["context"]}')
            print(f"\nTotal: {len(findings)}")

    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
