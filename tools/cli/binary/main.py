from .search import search_add_cmdargs


def binary_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser('binary', help='Binary files manipulation')
    binary_action_subparser = p.add_subparsers(
        title='action', metavar='ACTION', dest='action_command')

    search_add_cmdargs(p, binary_action_subparser)
    
    p.set_defaults(main=binary_main)
    p.set_defaults(action_command=(lambda cmdargs: p.print_help()))


def binary_main(cmdargs):
    cmdargs.action_command(cmdargs)
