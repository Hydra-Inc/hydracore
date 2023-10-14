from .model import model_add_cmdargs
from .savegame import savegame_add_cmdargs
from .trainer import trainer_add_cmdargs


def heroes3_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser('heroes3', help='Heroes 3 manipulation commands')
    heroes3_action_subparser = p.add_subparsers(
        title='action', metavar='ACTION', dest='action_command')

    model_add_cmdargs(p, heroes3_action_subparser)
    savegame_add_cmdargs(p, heroes3_action_subparser)
    trainer_add_cmdargs(p, heroes3_action_subparser)

    p.set_defaults(main=heroes3_main)
    p.set_defaults(action_command=(lambda cmdargs: p.print_help()))


def heroes3_main(cmdargs):
    cmdargs.action_command(cmdargs)
