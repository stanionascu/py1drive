# -*- coding: utf-8 -*-

# Hashes.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class Hashes(object):
    def __init__(self, **kwargs):
        if 'crc32Hash' in kwargs:
            self.crc32 = kwargs['crc32Hash']
        if 'sha1Hash' in kwargs:
            self.sha1 = kwargs['sha1Hash']