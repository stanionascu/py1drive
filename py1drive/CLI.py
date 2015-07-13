# -*- coding: utf-8 -*-

# CLI.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import py1drive.common as common
from py1drive.common import ProgressBar, absolute_to_relative
import os, hashlib, sys


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
            item_children = self.API.get_item_children(id=item_info.id)
            items = item_children
        else:
            items.append(item_info)
        print("total %s" % len(items))
        for item in items:
            print("%12s  %s" % (common.readable_size(item.size), item.name))

    def cmd_download(self, local_path, remote_path):
        item_info = self.API.get_item(remote_path)
        if local_path == None:
            local_path = os.getcwd()

        if not os.path.exists(local_path):
            os.mkdir(local_path)

        items = self.create_download_queue(item_info)

        print('Downloading to: ' + local_path)
        print('Downloading from: ' + remote_path)
        for item in items:
            relative_path = absolute_to_relative(local_path, remote_path,
                                                item.parentReference.path + '/' + item.name)
            if hasattr(item, 'file'):
                path, file = os.path.split(relative_path)
                print("Downloading %s to %s" % (file, path))
                if not os.path.exists(path):
                    os.makedirs(path)
            self.download_item(item, relative_path)

    def cmd_upload(self, local_path, remote_path):
        pass

    def create_download_queue(self, item_info):
        items = list()
        if hasattr(item_info, 'folder'):
            children = self.API.get_item_children(id=item_info.id)
            for item in children:
                items.extend(self.create_download_queue(item))
        else:
            items.append(item_info)
        return items

    def download_item(self, item, destination_dir):
        if hasattr(item, 'folder'):
            os.mkdir(destination_dir)
        else:
            if hasattr(item.file.hashes, 'sha1'):
                item_hash = hashlib.sha1()
                item_remote_hash = item.file.hashes.sha1.lower()
            r = self.API.get_item_content(item.id)
            total_size = r.headers.get('content-length')
            bar = ProgressBar(0, total_size)
            bar.start()
            with open(destination_dir, 'wb') as out:
                for chunk in r.iter_content(chunk_size=10240):
                    if chunk:
                        bar.cur_val += len(chunk)
                        out.write(chunk)
                        item_hash.update(chunk)
                    bar.display()
                out.flush()
            print('')
            if item_hash.hexdigest().lower() != item_remote_hash:
                raise Exception('Checksum mismatch!')

    def cmd_mkdir(self, remote_path, **kwargs):
        while remote_path.endswith('/'):
            remote_path = remote_path[:len(remote_path) - 1]
        parent_path, dir_name = os.path.split(remote_path)
        if not dir_name:
            sys.exit('Please provide a path e.g.: onedrive:///path/to/folder')
        else:
            self.API.create_dir(parent_path, dir_name)
