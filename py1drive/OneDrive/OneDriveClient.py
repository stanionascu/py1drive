# -*- coding: utf-8 -*-

# OneDriveClient.py -- part of py1drive
# Copyright (C) 2015 Stanislav Ionascu

# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import os, sys, json, yaml
from pprint import pprint
import py1drive.common as common

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

    def info(self, **kwargs):
        response = self._get('/drive').json()
        pprint(response)

    def _token_saver(self, token):
        self.session['oauth2_token'] = token;
        open(self.key_store, 'w').write(yaml.dump(self.session))

    def _make_url(self, method):
        return "%s%s" % (self.api_url, method)

    def _get(self, method, stream=False):
        r = self.client.get(self._make_url(method), stream=stream)
        r.raise_for_status()
        return r

