# -*- coding: utf-8 -*-

# common.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import os


def arg_is_dir(parser, path):
    if (os.path.isdir(path)):
        return path
    else:
        parser.error('%s is not a valid folder' % path)

