#!/usr/bin/env python3
""" Module doc here """
from bcrypt import gensalt, hashpw, checkpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_pwd = str(_hash_password(password))
            user = self._db.add_user(email=email, hashed_password=hashed_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if a user's login details are valid. """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return checkpw(password.encode('utf-8'),
                               user.hashed_password)
        except NoResultFound:
            return False
        return False


def _hash_password(password: str) -> bytes:
    """
        hashes a password
    :param password: the pwd to hash
    :return: hashed pwd in bytes
    """
    salt = gensalt()
    return hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """
        Generates a new uuid.
    :return: a string representation of a new UUID
    """
    return str(uuid.uuid4())
