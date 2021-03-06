# -*- coding: utf-8 -*-

# OneDriveClient.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import os, sys, json, yaml
from pprint import pprint
import py1drive.common as common
from py1drive.OneDrive import resources
from urllib.parse import quote


class OneDriveClient(object):
    config = []
    key_store = None
    session = dict()
    api_url = 'https://api.onedrive.com/v1.0'
    auth_base_url = 'https://login.live.com/oauth20_authorize.srf'
    auth_token_url = 'https://login.live.com/oauth20_token.srf'
    auth_scope = ['wl.offline_access', 'onedrive.readwrite']
    client = None
    is_authorized = False

    def __init__(self, config, key_store_dir):
        from requests_oauthlib import OAuth2Session

        self.config = config
        self.key_store = key_store_dir + '/oauth2_session_onedrive'
        if (os.path.exists(self.key_store)):
            self.session = yaml.load(open(self.key_store, 'r'))
        if (self.session == None):
            self.session = dict()

        self.is_authorized = ('oauth2_token' in self.session)
        self.client = OAuth2Session(self.config['client_id'],
            scope=self.auth_scope,
            redirect_uri='',
            token=self.session['oauth2_token'],
            auto_refresh_kwargs={
                'client_id': self.config['client_id'],
                'client_secret': self.config['client_secret']
            },
            auto_refresh_url=self.auth_token_url,
            token_updater=self._token_saver)

    def authorize(self, **kwargs):
        from urllib.parse import urlparse, parse_qs
        auth_url, state = self.client.authorization_url(self.auth_base_url)
        print("To allow access to your data, please open this URL in a web browser: %s" % auth_url)
        redirect_response = input('Paste the URL of the empty page: ')
        self.session['oauth2_state'] = state;
        token = self.client.fetch_token(
            self.auth_token_url,
            authorization_response=redirect_response,
            client_secret=self.config['client_secret'])
        self._token_saver(token)

    def get_drive_info(self):
        drive = resources.Drive(**self._get('/drive').json())
        return drive

    def get_item(self, remote_path):
        r = resources.Item(**self._get("/drive/root:%s" % quote(remote_path)).json())
        return r

    def get_item_children(self, remote_path=None, id=None, **kwargs):
        if remote_path:
            r = self._get("/drive/root:%s:/children" % quote(remote_path)).json()
        elif id:
            r = self._get("/drive/items/%s/children" % id).json()
        items = list()
        for value in r['value']:
            items.append(resources.Item(**value))
        return items

    def get_item_content(self, id, **kwargs):
        r = self._get("/drive/items/%s/content" % id, stream=True)
        return r

    def create_dir(self, parent_path, dir_name):
        r = self._post("/drive/root:%s:/children" % quote(parent_path),
                       data_json={"name": dir_name, "folder": {}})
        return resources.Item(**r.json())

    def _token_saver(self, token):
        self.session['oauth2_token'] = token;
        open(self.key_store, 'w').write(yaml.dump(self.session))

    def _make_url(self, method):
        return "%s%s" % (self.api_url, method)

    def _get(self, method, stream=False):
        r = self.client.get(self._make_url(method), stream=stream)
        r.raise_for_status()
        return r

    def _post(self, method, data_json=None, stream=False):
        headers = None
        data = None
        if data_json:
            data = json.dumps(data_json)
            headers = {'Content-Type' : 'application/json'}
        r = self.client.post(self._make_url(method), data=data, stream=stream, headers=headers)
        r.raise_for_status()
        return r
