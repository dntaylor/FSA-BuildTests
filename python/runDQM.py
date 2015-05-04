#!/usr/bin/env python

import argparse
from gitUtilities import *

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="Run DQM")

    args = parser.parse_args(argv)
    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    begin_dqm()

    return 0

if __name__ == "__main__":
    main()
