import os

from typing import Iterator, Optional
from functools import partial

from hydracore.utils.filters import filter_seq, filter_by_bool_fld, filter_by_sub_fld
from hydracore.heroes3.model.game import VERSIONS, SUPPORTED_LANGUAGES


def savegame_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser(
        'savegame', help='Heroes 3 save game reader/writer')

    p.add_argument('savegame', metavar='SAVEGAME',
                   action='store',
                   help='path to save game file')

    p.add_argument('--verbose',
                   action='store_true',
                   help="add verbose information")

    p.add_argument('--version', choices=VERSIONS.keys(),
                   action='store', default=None,
                   help="version of the savegame information")

    p.add_argument('--language', choices=SUPPORTED_LANGUAGES,
                   action='store', default=None,
                   help="language of the game")

    savegame_action_subparser = p.add_subparsers(
        title='action', metavar='ACTION', dest='action_command')

    dump_add_args(p, savegame_action_subparser)
    print_add_cmdargs(p, savegame_action_subparser)
    change_add_cmdargs(p, savegame_action_subparser)

    p.set_defaults(main=savegame_main)
    p.set_defaults(action_command=(lambda cmdargs: p.print_help()))


def savegame_main(cmdargs):
    from hydracore.format.heroes3 import Heroes3SaveGameFile
    from hydracore.heroes3.model.game import set_language

    if not os.path.isfile(cmdargs.savegame):
        print(f'File {cmdargs.savegame} not found!')
        return

    if cmdargs.language:
        set_language(cmdargs.language)

    sgf = Heroes3SaveGameFile(cmdargs.savegame)
    cmdargs.sgf = sgf

    cmdargs.action_command(cmdargs)


def dump_add_args(parser, subparsers):
    p = subparsers.add_parser(
        'dump', help='Dump savegame binary data and raw info')
    p.set_defaults(action_command=(lambda cmdargs: dump_main(cmdargs)))

    p.add_argument('action', choices=['full', 'hero', 'heroes'],
                   help="dump full file in binary format or hero chunk or all heroes chunks")

    p.add_argument('--out-file', metavar='PATH', type=str, action='store',
                   help="output file name (for single dump)")
    
    p.add_argument('--serialized',
                   action='store_true',
                   help="dump serialized")
    
    p.add_argument('--out-dir', metavar='PATH', type=str, action='store',
                   help="output file name (for mass dump)")
    
    p.add_argument('--filter-name', type=str, action='store',
                   help="filter heroes by name substring")


def dump_main(cmdargs):

    from hydracore.heroes3.savegame.main import savegame

    if cmdargs.action == 'full':
        if not cmdargs.out_file:
            print(f'Output file name is not set. Use --out-file option')
            return
        cmdargs.sgf.dump(cmdargs.out_file)
        print(f'File {cmdargs.out_file} written successfully')
        return
    
    # now try to "load" the Heroes3 object from this binary file
    try:
        heroes3sg = savegame(cmdargs.sgf, cmdargs.version,
                             verbose=cmdargs.verbose)
    except ValueError as e:
        print(
            f'Provided file {cmdargs.savegame} is not a Heroes 3 Save Game file')
        return

    # parse the file to objects
    heroes3sg.unpack()

    # get heroes
    filters = []
    if cmdargs.filter_name:
        filters.append(partial(filter_by_sub_fld, field='Name', sub=cmdargs.filter_name))    
    heroes = filter_seq(heroes3sg.heroes(), filters)
    if len(heroes) == 0:
        print(f'Heroes list is EMPTY')
        return

    if cmdargs.action == 'hero':
        if not cmdargs.out_file:
            print(f'Output file name is not set. Use --out-file option')
            return
        hero = heroes[0]
        if not cmdargs.serialized:
            count = hero.chunk.dump(cmdargs.out_file)
        else:
            #hero.Attack = 100
            #hero.AddCreature(6, 'Phoenix', 9999)
            chunk = hero.sgwrite()
            count = chunk.dump(cmdargs.out_file)
        print(f'Hero {hero.Name} written to file {cmdargs.out_file} successfully with {count} bytes')
        return
    
    if cmdargs.action == 'heroes':
        if not cmdargs.out_dir:
            print(f'Output file directory is not set. Use --out-dir option')
            return
        
        if not os.path.isdir(cmdargs.out_dir):
            os.makedirs(cmdargs.out_dir, exist_ok=True)
            
        num = 0
        for hero in heroes:
            num += 1
            fname = os.path.join(cmdargs.out_dir, hero.Name + '.dat')
            count = hero.chunk.dump(fname)
            print(f'Hero {hero.Name} written to file {fname} successfully with {count} bytes')
        print('Total written heroes:', num)
    

def print_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser(
        'print', help='Print loaded savegame: heroes, game info')
    p.set_defaults(action_command=(lambda cmdargs: print_main(cmdargs)))

    p.add_argument('action', choices=['gameinfo', 'heroes'],
                   help="print info on game, heroes")

    p.add_argument('--filter-name', type=str, action='store',
                   help="filter heroes by name substring")

    p.add_argument('--filter-hired', action='store_true',
                   help="filter only hired heroes")
    
    p.add_argument('--format', choices=['full', 'short', 'list', 'system'],
                   required=False, default='list',
                   help="which info to print")



def print_main(cmdargs):

    from hydracore.heroes3.savegame.main import savegame
    from hydracore.heroes3.model.arch import Color
    from hydracore.heroes3.model.map import maybe_template
    from hydracore.heroes3.model.scenario import maybe_scenario_info
    from hydracore.heroes3.model.template import TemplateList

    # now try to "load" the Heroes3 object from this binary file
    try:
        heroes3sg = savegame(cmdargs.sgf, cmdargs.version,
                             verbose=cmdargs.verbose)
    except ValueError as e:
        print(
            f'Provided file {cmdargs.savegame} is not a Heroes 3 Save Game file')
        return

    # parse the file to objects
    heroes3sg.unpack()

    if cmdargs.action == 'gameinfo':
        heroes3sg.dump_info()
        if maybe_template(heroes3sg.title, heroes3sg.description, heroes3sg.map_file_location):
            print('  Is map from template:', 'YES')
            templates = TemplateList()
            tpl = templates.identify_template(heroes3sg.title, heroes3sg.description, heroes3sg.map_file_location)
            if tpl:
                print('  Template:', tpl.fullname())
            else:
                print('  Template:', '-not identified-')
        else:
            print('  Is map from template:', 'NO')

        scenario = maybe_scenario_info(heroes3sg.title, heroes3sg.description)
        if scenario:
            if scenario.HumanCount is not None:
                print('  Human count:', scenario.HumanCount)
            if scenario.MyselfColor is not None:
                print('  Myself color:', Color.to_str(scenario.MyselfColor))

    elif cmdargs.action == 'heroes':

        # Filters setup
        filters = []
        if cmdargs.filter_name:
            filters.append(partial(filter_by_sub_fld, field='Name', sub=cmdargs.filter_name))
        if cmdargs.filter_hired:
            filters.append(partial(filter_by_bool_fld, field='Hired'))

        # List actually the heroes
        num = 0
        prev = 0
        for hero in filter_seq(heroes3sg.heroes(), filters):
            num += 1
            if cmdargs.format == 'full':
                hero.dump()
            elif cmdargs.format == 'short':
                hero.dump_short()
            elif cmdargs.format == 'list':
                color = Color.to_str(hero.Color) if hero.Hired else 'Not Hired'
                print(f'{hero.Name: <12} {hero.Class: <13} level {hero.Level: <3} exp {hero.Experience: <6}  | {color}' )
            elif cmdargs.format == 'system':
                print(f'{hero.Name: <12} from bytes {hero.chunk.start} to {hero.chunk.end}' )

        print('Listed heroes', num)



def change_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser(
        'change', help='Change savegame data')
    p.set_defaults(action_command=(lambda cmdargs: change_main(cmdargs)))

    p.add_argument('action', choices=['hero'],
                   help="what to change in the savegame file")

    p.add_argument('--out-file', metavar='PATH', type=str, action='store',
                   help="output file name for the resulting savegame file")
    
    p.add_argument('--verbose',
                   action='store_true',
                   help="add verbose information")
    
    p.add_argument('--filter-name', type=str, action='store',
                   help="filter hero by name substring")


def change_main(cmdargs):

    from hydracore.heroes3.savegame.main import savegame

    
    if not cmdargs.out_file:
        print(f'Output file name is not set. Use --out-file option')
        return

    # now try to "load" the Heroes3 object from this binary file
    try:
        heroes3sg = savegame(cmdargs.sgf, cmdargs.version,
                             verbose=cmdargs.verbose)
    except ValueError as e:
        print(
            f'Provided file {cmdargs.savegame} is not a Heroes 3 Save Game file')
        return

    # parse the file to objects
    try:
        heroes3sg.unpack()
    except ValueError as e:
        print(
            f'Got a problem while parsing SaveGame file')
        raise e

    # process hero
    if cmdargs.action == 'hero':
        filters = []
        if cmdargs.filter_name:
            filters.append(partial(filter_by_sub_fld, field='Name', sub=cmdargs.filter_name))    
        heroes = filter_seq(heroes3sg.heroes(), filters)
        if len(heroes) == 0:
            print(f'Heroes list is EMPTY')
            return
        if len(heroes) > 1:
            print(f'Got more than one hero')
            return
            
        hero = heroes[0]
        hero.Attack = 98
        hero.AddCreature(6, 'Phoenix', 9999)
        heroes3sg.pack()
        heroes3sg.file.save(cmdargs.out_file)
        
        print(f'Hero {hero.Name} written to file {cmdargs.out_file} successfully')
        return
    
    