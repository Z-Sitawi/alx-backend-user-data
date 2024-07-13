#!/usr/bin/env python3
""" Module of class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ method doc here """
        return False

    def authorization_header(self, request=None) -> str:
        """ method doc here. """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ method doc here. """
        return request
