# -*- coding: utf-8 -*-

# IdentitySet.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from .Identity import Identity

class IdentitySet(object):
	user = None
	application = None
	device = None

	def __init__(self, user=None, application=None, device=None):
		self.user = Identity(**user)
		if (self.application):
			self.application = Identity(**application)
		if (self.device):
			self.device = Identity(**device)
