import sys
import argparse

from parsers.parsers import SiteParser
from storages.storage import Storage


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('text', help='Search text')
    parser.add_argument('-e', '--engine', dest='engine', choices=['google', 'yandex'], default='google',
                        help="Search engine")
    parser.add_argument('-l', '--limit', dest='limit', type=int, choices=range(1, 101), default=100, metavar='[0-100]',
                        help='Number of results shown')
    parser.add_argument('-d', '--depth', dest='depth', type=int, choices=range(0, 3), default=1, metavar='[0-2]',
                        help='Search depth')

    return parser


if __name__ == '__main__':
    SiteParser.get_parser(Storage(), **vars(get_args().parse_args())).parse()

