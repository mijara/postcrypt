import sys
import argparse

from postcrypt import Postcrypt


def create_arg_parser():
    parser = argparse.ArgumentParser(description='Postcrypt HTTP scripts')

    parser.add_argument('crypt', type=str, help='Scrypt to run')
    parser.add_argument('mode', type=str, nargs='?', help='Optional scrypt mode')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('--save', action='store_true', help='Remember input values')

    return parser


if __name__ == '__main__':
    args = create_arg_parser().parse_args()
    postcrypt = Postcrypt(args.crypt, mode=args.mode, verbose=args.verbose, save=args.save)
    postcrypt.process()
