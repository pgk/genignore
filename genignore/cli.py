import argparse


def parse(args):
    parser = argparse.ArgumentParser(description="Generates .gitignore files")
    subparsers = parser.add_subparsers(title='subcommands',
                                       help='valid genignore subcommands',
                                       dest="action")

    gen_parser = subparsers.add_parser('gen', help='generate a gitignore')


    gen_parser.add_argument('names', metavar='N', type=str, nargs='+',
                            help='Name(s) of things to include to the .gitignore')

    gen_parser.add_argument("-o", "--out", type=str, default='',
                            help='file to output the generated gitignore (default .gitignore of pwd)')

    gen_parser.add_argument("--update", action='store_true',
                            help='update the file if it exists, keeping custom entries')

    gen_parser.add_argument("--add", action='store_true', default=False,
                            help='add templates the file if it exists, keeping previous entries')

    sync_parser = subparsers.add_parser("sync", help='sync to latest templates (requires internet connection)')

    list_parser = subparsers.add_parser("list", help="list all available templates")

    return parser.parse_args(args)
