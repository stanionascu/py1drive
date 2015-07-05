# -*- coding: utf-8 -*-

# Identity.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

class Identity(object):
	id = str()
	displayName = str()

	def __init__(self, id=str(), displayName=str()):
		self.id = id
		self.displayName = displayName
