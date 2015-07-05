# -*- coding: utf-8 -*-

# Drive.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from ..types import IdentitySet
from ..facets import Quota


class Drive(object):
    def __init__(self, id=None, driveType=None, owner=None, quota=None, **kwargs):
        self.id = id
        self.driveType = driveType
        self.owner = IdentitySet(**owner)
        self.quota = Quota(**quota)
