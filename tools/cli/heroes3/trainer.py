import datetime

from hydracore.utils.filters import filter_seq, filter_by_bool_fld, filter_by_sub_fld
from hydracore.heroes3.model.game import VERSIONS, SUPPORTED_LANGUAGES


def trainer_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser('trainer', help='Heroes 3 trainer')

    trainer_action_subparser = p.add_subparsers(
        title='action', metavar='ACTION', dest='action_command')

    list_add_args(p, trainer_action_subparser)
    run_add_cmdargs(p, trainer_action_subparser)

    p.set_defaults(main=trainer_main)
    p.set_defaults(action_command=(lambda cmdargs: p.print_help()))


def trainer_main(cmdargs):
    cmdargs.action_command(cmdargs)


def list_add_args(parser, subparsers):
    p = subparsers.add_parser('list', help='list all trainers')
    p.set_defaults(action_command=(lambda cmdargs: list_main(cmdargs)))


def list_main(cmdargs):

    from hydracore.heroes3.trainer.list import TrainerList

    trainers = TrainerList()
    print('Available trainers:')
    i = 0
    for trainer_id in sorted(trainers.get_ids()):
        i += 1
        trainer = trainers.at(trainer_id)
        print(f'  {i}. {trainer_id} - {trainer.title}')
    print()


def run_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser('run', help='run selected trainer')
    p.set_defaults(action_command=(lambda cmdargs: run_main(cmdargs)))

    from hydracore.heroes3.trainer.list import TrainerList
    from hydracore.heroes3.trainer.base import Difficulty
    trainers = TrainerList()

    p.add_argument('trainer', choices=[trainer_id for trainer_id in sorted(trainers.get_ids())],
                   help="select trainer you want to run")

    p.add_argument('savegame', type=str, action='store',
                   help="savegame to patch")

    p.add_argument('--difficulty', choices=[dif.name for dif in Difficulty],
                   required=False, default=Difficulty.Medium.name,
                   help="difficulty to run the trainer")

    p.add_argument('--date', type=int,
                   required=False,
                   help="explicitly set the date in format 111 or 143")

    p.add_argument('--out-file', metavar='PATH', type=str, action='store',
                   required=True, help="output savegame file name")

    p.add_argument('--out-flow', metavar='PATH', type=str, action='store',
                   required=False, help="output generation flow of the trainer (used for debug)")

    p.add_argument('--in-flow', metavar='PATH', type=str, action='store',
                   required=False, help="input generation flow of the trainer (to reproduce the flow)")

    p.add_argument('--verbose',
                   action='store_true',
                   help="add verbose information")


def run_main(cmdargs):

    from hydracore.format.heroes3 import Heroes3SaveGameFile
    from hydracore.heroes3.model.map import maybe_map_info
    from hydracore.heroes3.model.scenario import maybe_scenario_info
    from hydracore.heroes3.model.time import from_num
    from hydracore.heroes3.savegame.main import savegame
    from hydracore.heroes3.trainer.main import get_trainer
    from hydracore.heroes3.trainer.base import Difficulty

    try:
        sgf = Heroes3SaveGameFile(cmdargs.savegame)
        heroes3sg = savegame(sgf)
        heroes3sg.unpack()
        heroes = [hero for hero in heroes3sg.heroes() if hero.Hired]

        if cmdargs.date is not None:
            heroes3sg.set_date(from_num(cmdargs.date))
        if heroes3sg.date is None:
            raise RuntimeError(f'Date not identified, please set it manually')

        trainer = get_trainer(cmdargs.trainer,
                              date=heroes3sg.date,
                              heroes=heroes,
                              difficulty=Difficulty[cmdargs.difficulty])
        if trainer is None:
            raise RuntimeError(f'Trainer {cmdargs.trainer} not found')

        if cmdargs.verbose:
            trainer.SetVerbose()

        if cmdargs.in_flow:
            trainer.Random.load(cmdargs.in_flow)

        mapinfo = maybe_map_info(heroes3sg.title, heroes3sg.description)
        scenario = maybe_scenario_info(heroes3sg.title, heroes3sg.description)

        trainer.SetMapTerrainInfo(mapinfo)
        trainer.SetScenarioInfo(scenario)
        trainer.check()
        trainer.run()

        heroes3sg.pack()
        heroes3sg.file.save(cmdargs.out_file)

        if cmdargs.out_flow:
            outflow_file = cmdargs.out_flow
            if outflow_file == '-':
                outflow_file = None
        else:
            date_string = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            outflow_file = f'.trainer_{cmdargs.trainer}_{date_string}.json'
        if outflow_file:
            trainer.Random.save(outflow_file)
            print(f'Train flow saved to {outflow_file}')

        print(
            f'Boosted save game written to file {cmdargs.out_file} successfully')

    except Exception as e:
        raise
        print('Got error:', e)
        return
