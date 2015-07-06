#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 1drive.py -- cli frontend to onedrive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import sys, os
from py1drive.common import arg_is_dir
from py1drive.CLI import CLI

"""OneDrive Python client"""

config = []
default_config_dir = os.path.expanduser('~/.py1drive')
supported_actions = ['authorize',
    'upload', 'download',
    'list', 'info',
    'mkdir', 'rm']
config_file = None
key_store_dir = None

def build_arg_parser():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-c',
        '--config',
        type=argparse.FileType('r'),
        help='Config file to load')
    parser.add_argument('-k',
        '--key-store-dir',
        type=lambda x: arg_is_dir(parser, x),
        help='Location of the authorization key store dir')
    parser.add_argument('action',
        choices=supported_actions,
        help='Action to execute on path')
    parser.add_argument('local_path',
        type=str,
        nargs='?',
        help='Path to local file/folder')
    parser.add_argument('remote_path',
        type=str,
        help='Path to remote folder')
    return parser

def exec_action(action, local_path, remote_path):
    from urllib.parse import urlparse
    url = urlparse(remote_path)
    if url.scheme == 'onedrive':
        from py1drive.OneDrive.OneDriveClient import OneDriveClient as API
    else:
        sys.exit("Unsupported scheme: %s" % url.scheme)
    if (url.scheme not in config):
        config[url.scheme] = dict()
        save_config()
    cli = CLI(API(config[url.scheme], key_store_dir=key_store_dir))
    method = getattr(cli, 'cmd_' + action, None)
    if method:
        method(local_path=local_path, remote_path=url.path)
    else:
        sys.exit("Action '%s' is not supported" % action)

def save_config():
    open(config_file, 'w').write(yaml.dump(config))

if __name__ == '__main__':
    import yaml
    parser = build_arg_parser()
    args = parser.parse_args()

    if (not os.path.exists(default_config_dir)):
        os.makedirs(default_config_dir)

    if (args.action == 'upload'):
        if (args.local_path is None):
            parser.error('"upload" action requires local_path')
        elif (not os.path.exists(args.local_path)):
            parser.error("invalid local_path %s, the location doesn't exist" % args.local_path)

    if (args.config is None):
        config_file = default_config_dir + '/py1drive'
    else:
        config_file = args.config.name

    if (args.key_store_dir is None):
        key_store_dir = default_config_dir
    else:
        key_store_dir = args.key_store_dir

    if (os.path.exists(config_file)):
        config = yaml.load(open(config_file, 'r'))
    else:
        config = dict()
    exec_action(args.action, args.local_path, args.remote_path)
