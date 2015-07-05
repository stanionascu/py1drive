# -*- coding: utf-8 -*-

# Item.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

from ..types import ItemReference, IdentitySet
from ..facets import Folder


class Item(object):
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.parentReference = ItemReference(**kwargs['parentReference'])
        self.createdBy = IdentitySet(**kwargs['createdBy'])
        self.createdDateTime = kwargs['createdDateTime']
        self.lastModifiedDateTime = kwargs['lastModifiedDateTime']
        self.size = kwargs['size']
        if 'children' in kwargs:
            self.children = list()
            for child in kwargs['children']:
                self.children.append(Item(**child))
        if 'folder' in kwargs:
            self.folder = Folder(**kwargs['folder'])