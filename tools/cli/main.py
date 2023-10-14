import argparse

from .binary import binary_add_cmdargs
from .info import info_add_cmdargs
from .heroes3 import heroes3_add_cmdargs


def main():
    # Create parser.
    parser = argparse.ArgumentParser(prog='hydracore')
    subparsers = parser.add_subparsers(dest='main', metavar='COMMAND')
    parser.set_defaults(main=(lambda cmdargs: parser.print_help()))
    
    binary_add_cmdargs(parser, subparsers)
    info_add_cmdargs(parser, subparsers)    
    heroes3_add_cmdargs(parser, subparsers)

    cmdargs = parser.parse_args()
    cmdargs.main(cmdargs)
    