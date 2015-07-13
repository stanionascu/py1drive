# -*- coding: utf-8 -*-

# common.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import os, math, time, sys

def readable_size(size):
    if size == 0:
        return '0 B '
    size_units = ('B', 'KB', 'MB', 'GB', 'TB')
    unit = min(math.floor(math.log(size, 1024)), len(size_units) - 1)
    size_fmt = round(size / math.pow(1024, unit), 2)
    return "%s %s" % (size_fmt, size_units[unit])

def arg_is_dir(parser, path):
    if (os.path.isdir(path)):
        return path
    else:
        parser.error('%s is not a valid folder' % path)

class ProgressBar(object):
    def __init__(self, min_val, max_val):
        self.min_val = int(min_val)
        if not max_val is None:
            self.max_val = int(max_val)
        self.cur_val = int(min_val)

    def start(self):
        self.start_time = time.clock()

    def display(self):
        speed = readable_size(self.cur_val//(time.clock() - self.start_time))
        if self.max_val is None:
            sys.stdout.write("\r[%s] %s %s/s" % ('=' * 50, readable_size(self.cur_val), speed))
        else:
            progress = 50 * self.cur_val / self.max_val
            int_progress = int(progress)
            sys.stdout.write("\r%3.1f%% [%s%s] %s of %s %s/s" %
                             ((progress/50*100), '=' * int_progress, ' ' * (50 - int_progress),
                              readable_size(self.cur_val), readable_size(self.max_val), speed))
