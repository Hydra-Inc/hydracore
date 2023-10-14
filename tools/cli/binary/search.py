import os


def search_add_cmdargs(parser, subparsers):
    p = subparsers.add_parser('search', help='Search binary files')
    p.set_defaults(main=search_main)

    p.add_argument('file', metavar='BINARY_FILE',
                   action='store',
                   help='path to binary file')

    p.add_argument('--str', type=str,
                   action='store',
                   help='substring to search')
    
    p.add_argument('--hex', type=str,
                   action='store',
                   help='hex to search')
    
    p.add_argument('--str-rus', type=str,
                   action='store',
                   help='string in Russian')


def search_main(cmdargs):

    from hydracore.format.base import BinFile
    from hydracore.format.chunk import Chunk

    if not os.path.isfile(cmdargs.file):
        print(f'File {cmdargs.file} not found!')
        return

    bin = BinFile(cmdargs.file)

    subbin = False
    if cmdargs.str:
        subbin = bytes(cmdargs.str, 'utf-8')
    if cmdargs.hex:
        subbin = bytes.fromhex(cmdargs.hex)
    if cmdargs.str_rus:
        subbin = bytes(cmdargs.str_rus, 'cp1251')
    
    if subbin:
        i = 0
        for chunk in bin.substr_search(subbin):
            blob = chunk.blob
            start = chunk.start
            end = chunk.end
            i += 1
            blob = bytes(blob)
            print(f'{i: <3}: {blob} at {start} to {end}')
            

        print(f'Total found: {i}')
        return