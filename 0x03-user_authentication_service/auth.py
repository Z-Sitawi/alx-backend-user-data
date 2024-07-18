#!/usr/bin/env python3
""" Module doc here """
from bcrypt import gensalt, hashpw


def _hash_password(password: str) -> bytes:
    """
        hashes a password
    :param password: the pwd to hash
    :return: hashed pwd in bytes
    """
    salt = gensalt()
    return hashpw(password.encode('utf-8'), salt)
