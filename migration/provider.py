#!env python
# -*- coding: utf-8 -*-
from .helper import set_encoding

set_encoding()


class Provider:
    def __init__(self, username, password, repo_name):
        self._username = username
        self._password = password
        self._repo_name = repo_name

    def create_url(self):
        pass

    def parsing(self):
        pass
