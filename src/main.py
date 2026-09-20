from ip_lookup import IPLookup
from domain_enum import DomainEnum
from username_lookup import UsernameLookup
import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

class HelpFormatter(argparse.HelpFormatter):

    def format_help(self):
        return """Welcome to osintmaster multi-function Tool

OPTIONS:
    -i  "IP Address"       Search information by IP address
    -u  "Username"         Search information by username
    -d  "Domain"           Enumerate subdomains and check for takeover risks
    -o  "FileName"         File name to save output
    --help                 Display this help message
"""


class Main:

    def __init__(self):
        load_dotenv()

        self.parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=HelpFormatter
        )

        # Mutually exclusive tools
        group = self.parser.add_mutually_exclusive_group()

        group.add_argument(
            "-i",
            help="Search information by IP address"
        )

        group.add_argument(
            "-u",
            help="Search information by username"
        )

        group.add_argument(
            "-d",
            help="Enumerate subdomains and check for takeover risks"
        )

        # Global output option
        self.parser.add_argument(
            "-o",
            metavar="FileName",
            help="File name to save output"
        )

        self.parser.add_argument(
            "--help",
            action="store_true"
        )

        self.output = ""

    def run(self):

        args = self.parser.parse_args()

        # Display help
        if args.help:
            print(self.parser.format_help())
            sys.exit(0)

        # Check if a tool was selected
        if args.i is None and args.u is None and args.d is None:
            print(self.parser.format_help())
            sys.exit(0)

        # Execute the selected tool
        try:
            if args.i is not None:
                ip = IPLookup(args.i)
                self.output = ip.lookup()

            elif args.u is not None:
                username = UsernameLookup(args.u)
                self.output = username.lookup()

            elif args.d is not None:
                domain = DomainEnum(args.d)
                self.output = domain.enumeration()

        except Exception:
            print("Error: An error occurred while executing the tool",
                  file=sys.stderr)
            sys.exit(1)

        # Print results
        if self.output is not None:
            print(self.output)

        # Save output
        if args.o is not None:
            self.save_output(args.o)

    def save_output(self, filename):

        try:
            base_dir = Path(__file__).resolve().parent.parent
            output_dir = base_dir / "output"

            output_dir.mkdir(parents=True, exist_ok=True)

            filename = os.path.basename(filename)
            output_path = output_dir / filename

            with open(output_path, "w", encoding="utf-8") as file:
                file.write(str(self.output))

            print(f"Results saved to {output_path}")

        except OSError:
            print("Error: Could not save output", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main = Main()
    main.run()