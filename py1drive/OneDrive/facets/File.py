# -*- coding: utf-8 -*-

# File.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from ..types import Hashes


class File(object):
    def __init__(self, **kwargs):
        self.mimeType = kwargs['mimeType']
        self.hashes = Hashes(**kwargs['hashes'])