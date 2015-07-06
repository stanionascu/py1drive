# -*- coding: utf-8 -*-

# CLI.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import py1drive.common as common

class CLI(object):
    def __init__(self, api):
        self.API = api
        if not self.API.is_authorized:
            self.API.authorize()

    def cmd_info(self, **kwargs):
        drive = self.API.get_drive_info()
        print('Owner: ' + drive.owner.user.displayName)
        print('Used Space: ' + common.readable_size(drive.quota.used))
        print('Free Space: ' + common.readable_size(drive.quota.remaining))
        print('Total Space: ' + common.readable_size(drive.quota.total))
        print('Recycle Bin Space: ' + common.readable_size(drive.quota.deleted))
        print('State: ' + drive.quota.state)

    def cmd_list(self, remote_path, **kwargs):
        item_info = self.API.get_item(remote_path)
        items = list()
        if hasattr(item_info, 'folder'):
            item_children = self.API.get_item_children(remote_path)
            items = item_children
        else:
            items.append(item_info)
        print("total %s" % len(items))
        for item in items:
            print("%12s  %s" % (common.readable_size(item.size),  item.name))