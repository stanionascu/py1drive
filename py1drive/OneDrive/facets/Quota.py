# -*- coding: utf-8 -*-

# Quota.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class Quota(object):
	def __init__(self, total=0, used=0, remaining=0, deleted=0, state=None):
		self.total = total
		self.used = used
		self.remaining = remaining
		self.deleted = deleted
		self.state = state
