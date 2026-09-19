from ip_lookup import IPLookup
from domain_enum import DomainEnum
from username_lookup import UsernameLookup
import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
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


parser = argparse.ArgumentParser(add_help=False, formatter_class=HelpFormatter)

# Mutually exclusive tools
group = parser.add_mutually_exclusive_group()

group.add_argument("-i", help="Search information by IP address")
group.add_argument("-u", help="Search information by username")
group.add_argument("-d", help="Enumerate subdomains and check for takeover risks")

# Global output option
parser.add_argument("-o", metavar="FileName", help="File name to save output")
parser.add_argument("--help",action="store_true")

args = parser.parse_args()
output = ""

# Display help
if args.help:
    print(parser.format_help())
    sys.exit(0)

# Check if a tool was selected
if args.i is None and args.u is None and args.d is None:
    print(parser.format_help())
    sys.exit(0)


# Execute the selected tool
try:
    if args.i is not None:
        ip = IPLookup(args.i)
        output = ip.lookup()

    elif args.u is not None:
        username = UsernameLookup(args.u)
        output = username.lookup()

    elif args.d is not None:
        domain = DomainEnum(args.d)
        output = domain.enumeration()

except Exception as error:
    print(f"Error : {error}", file=sys.stderr)
    sys.exit(1)


# Print results
if output is not None:
    print(output)


# Save output
if args.o is not None:
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        OUTPUT_DIR = BASE_DIR / "output"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        filename = os.path.basename(args.o)
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(str(output))

        print(f"Results saved to {output_path}")

    except OSError as error:
        print(f"Could not save output: {error}", file=sys.stderr)
        sys.exit(1)