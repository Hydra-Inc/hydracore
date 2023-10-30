
import os.path
import sys


def info_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser('info', help='get info from the save game file')
    p.set_defaults(main=info_main)
    
    p.add_argument('savegame', metavar='SAVEGAME',
        action='store',
        help='path to save game file')
    
    p.add_argument('category',choices=['all', 'heroes'],
        action='store',
        help="what category you want to see")
    
    p.add_argument('--verbose',
        action='store_true',
        help="add verbose information")
    
 
def info_main(cmdargs):

    if not os.path.isfile(cmdargs.savegame):
        print(f'File not found: {cmdargs.savegame}')
        return

    from hydracore.format.heroes3 import Heroes3SaveGameFile
    from hydracore.heroes3.savegame.main import savegame
    
    sgf = Heroes3SaveGameFile(cmdargs.savegame)
    heroes3sg = savegame(sgf)

    print(heroes3sg)
