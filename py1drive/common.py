# -*- coding: utf-8 -*-

# common.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import os, math

def readable_size(size):
    if size == 0:
        return '0 B '
    size_units = ('KB', 'MB', 'GB', 'TB')
    unit = int(math.floor(math.log(size, 1024)))
    if unit >= len(size_units):
        unit = len(size_units) - 1
    size = round(size / math.pow(1024, unit), 2)
    return "%s %s" % (size, size_units[unit])

def arg_is_dir(parser, path):
    if (os.path.isdir(path)):
        return path
    else:
        parser.error('%s is not a valid folder' % path)

