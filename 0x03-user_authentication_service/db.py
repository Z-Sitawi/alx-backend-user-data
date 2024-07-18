#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a new user to the database. """
        try:
            user_object = User(email=email, hashed_password=hashed_password)
            self._session.add(user_object)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user_object = None

        return user_object

    def find_user_by(self, **kwargs) -> User:
        """ Finds a user based on a set of filters."""
        key, val = [], []

        for k, v in kwargs.items():
            if hasattr(User, k):
                key.append(getattr(User, k))
                val.append(v)
            else:
                raise InvalidRequestError()
        user = self._session.query(User).filter(tuple_(*key).in_([tuple(val)])).first()

        if user is None:
            raise NoResultFound()
        return user
