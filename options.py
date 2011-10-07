#!/usr/bin/env python

import argparse

action_choices = [
    "scratch",
    "update",
    "purge",
    "index",
    "add_tag",
]

parser = argparse.ArgumentParser(
    description="Manage MongoDB music library",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    "action",
    default="update",
    choices=action_choices,
    nargs="?",
    help="""Action to perform""")

parser.add_argument(
    "-m", "--music-path",
    dest="music_path",
    help="""Add music from this dir (overrides configured value)""")

parser.add_argument(
    "-v", "--verbose",
    action="store_true",
    default=False,
    help="""Be verbose""")

parser.add_argument(
    "-a", "--artist",
    dest="artist",
    help="""Artist to be tagged""")

parser.add_argument(
    "-t", "--tag",
    dest="tag",
    help="""Tag to add""")

options = parser.parse_args()
