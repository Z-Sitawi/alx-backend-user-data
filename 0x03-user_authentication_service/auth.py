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
            hashed_pwd = _hash_password(password)
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

    def create_session(self, email: str) -> str:
        """ Creates a new session for a user. """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                sid = _generate_uuid()
                self._db.update_user(user_id=user.id, session_id=sid)
                return sid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """ Find user by session ID """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroys a session """
        self._db.update_user(user_id=user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Generate reset password token """
        try:
            user = self._db.find_user_by(email=email)
            unique_id = _generate_uuid()
            self._db.update_user(user_id=user.id, reset_token=unique_id)
            return unique_id
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates a user's password """
        if reset_token is None or password is None:
            raise ValueError()

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        pwd = _hash_password(password.encode('utf-8'))
        self._db.update_user(user_id=user.id, hashed_password=pwd,
                             reset_token=None)


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
