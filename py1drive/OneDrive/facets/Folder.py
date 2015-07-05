# -*- coding: utf-8 -*-

# Folder.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class Folder(object):
    def __init__(self, childCount=0):
        self.childCount = childCount