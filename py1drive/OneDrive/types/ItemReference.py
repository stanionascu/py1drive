# -*- coding: utf-8 -*-

# ItemReference.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class ItemReference(object):
    def __init__(self, id, driveId, path):
        self.id = id
        self.driveId = driveId
        self.path = path
