# -*- coding: utf-8 -*-

# IdentitySet.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from .Identity import Identity

class IdentitySet(object):
    def __init__(self, **kwargs):
        if 'user' in kwargs:
            self.user = Identity(**kwargs['user'])
        if 'application' in kwargs:
            self.application = Identity(**kwargs['application'])
        if 'device' in kwargs:
            self.device = Identity(**kwargs['device'])
