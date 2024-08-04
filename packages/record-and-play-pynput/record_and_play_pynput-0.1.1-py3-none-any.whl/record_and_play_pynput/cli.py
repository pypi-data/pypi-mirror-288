"""This module serves as the entry point for the CLI tool."""

# Built-in modules
import argparse
import sys

# Local modules
from record_and_play_pynput import record, play

def main():
    parser = argparse.ArgumentParser(description="Record and play back keyboard and mouse inputs.")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")
    
    record_parser = subparsers.add_parser("record", help="Record keyboard and mouse inputs.")
    record_parser.add_argument('-n', '--name_of_recording', type=str, required=True, help='Name of the recording')
    
    play_parser = subparsers.add_parser("play", help="Play back recorded keyboard and mouse inputs.")
    play_parser.add_argument('-n', '--name_of_recording', type=str, required=True, help='Name of the recording')
    play_parser.add_argument('-p', '--plays', type=int, required=True, help='Number of times to repeat the recording')
    
    args = parser.parse_args()
    
    if args.command == "record":
        record.main(args)
    elif args.command == "play":
        play.main(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()