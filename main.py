import subprocess
import argparse
import sys
import common
from setup import ENV


def parse_args(args, cmd_line):
    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument('--env', nargs='?', type=bool, const=ENV, default=ENV,
                        help=f"Enables use of .env file. Defaults to {ENV}.")


def main(args, cmd_line=False):
    subprocess.Popen(
        ["start", "cmd", "/k", "python ./taus_bot.py"], shell=True)


if __name__ == "__main__":
    main(sys.argv[1:], True)
