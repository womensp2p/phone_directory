
import datetime
import re

import sqlalchemy
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from phone_directory_actions import PhoneDirectoryActions
from util import validate_phone_number


Base = declarative_base()

def bind_engine(engine):
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=True)


class User(Base):
    __tablename__ = 'users'

    user_id = Column('user_id', Integer, primary_key=True)
    phone = Column('crm_type', String(100))
    name = Column('name', String(100))

    updated_at = Column('updated_at', DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now, index=True)
    created_at = Column('created_at', DateTime, default=datetime.datetime.now, index=True)


class PhoneHistory(Base):
    __tablename__ = 'phone_history'
    id = Column('id', Integer, index=True, primary_key=True)
    user_id = Column('user_id', Integer, index=True)
    phone = Column('phone', String(100))
    updated_at = Column('updated_at', DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now, index=True)
    created_at = Column('created_at', DateTime, default=datetime.datetime.now, index=True)


class SqlitePhoneDirectoryActions(PhoneDirectoryActions):
    '''
    Data stored in a sqliteDB.
    '''

    def __init__(self, database="sqlite:///test.db"):
        engine = sqlalchemy.create_engine(
            database # TODO: better path to database
        )

        self._SessionMaker = bind_engine(engine)

    def _get_user_by_id(self, user_id):
        session = self._SessionMaker()
        res = session.query(User).filter(User.user_id == user_id).all()
        session.close()

        if len(res) != 1:
            raise KeyError
        else:
            return res[0]

    def user_exists(self, user_id):
        '''
        Return true if user_id exists, false if not
        '''
        user = self._get_user_by_id(user_id)
        return (user != None) # truthy

    def get_phone_number(self, user_id):
        '''
        Return phone number for given user_id. Throw KeyError if user doesn't exist.
        '''
        user = self._get_user_by_id(user_id)
        return user.phone

    def get_name(self, user_id):
        '''
        Return username for given user_id. Throw KeyError if user doesn't exist.
        '''
        user = self._get_user_by_id(user_id)
        return user.name

    def update_phone_number(self, user_id, new_number):
        '''
        If user_id exists, update its phone number and archive the old number.
        If user_id does not exist, throw KeyError
        If new phone number is not valid, throw
        '''
        user = self._get_user_by_id(user_id)
        validate_phone_number(new_number)
        old_number = user.phone
        user.phone = new_number

        session = self._SessionMaker()

        history = PhoneHistory()
        history.user_id = user.user_id
        history.phone = old_number

        session.add(user)
        session.add(history)
        session.commit()

    def _add_a_user(self, user_id, phone, name):
        validate_phone_number(phone)

        session = self._SessionMaker()

        user = User()
        user.name = name
        user.user_id = user_id
        user.phone = phone

        session.add(user)
        session.commit()


if __name__ == '__main__':
    sq = SqlitePhoneDirectoryActions(database="sqlite:///:memory:")
    sq._add_a_user(user_id=1122, phone='1'*10, name='ben')

    # some quick tests
    assert sq.user_exists(1122)
    assert sq.get_name(1122) == 'ben'
    assert sq.get_phone_number(1122) == '1'*10
    sq.update_phone_number(user_id=1122, new_number='2'*10)
    assert sq.get_phone_number(1122) == '2'*10


