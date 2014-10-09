
import datetime
import re
import sqlalchemy
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from phone_directory_actions import PhoneDirectoryActions
from util import validate_phone_number


# Creating the base class for database mapped objects,
# see: http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html
Base = declarative_base()

# A helper for binding a database engine for use with declaritive base
def bind_engine(engine):
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=True)

class User(Base):
    """ User model representing a user with a user_id, name, and phone number """
    __tablename__ = 'users'

    user_id = Column('user_id', Integer, primary_key=True)
    phone = Column('crm_type', String(100))
    name = Column('name', String(100))
    updated_at = Column('updated_at', DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now, index=True)
    created_at = Column('created_at', DateTime, default=datetime.datetime.now, index=True)


class PhoneHistory(Base):
    """ PhoneHistory, we store a PhoneHistory entry for each change """
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

    def __init__(self, database="sqlite:///:memory:"):
        engine = sqlalchemy.create_engine(
            database # TODO: better path to database
        )

        self._SessionMaker = bind_engine(engine)

    def _get_user_by_id(self, user_id):
        session = self._SessionMaker()
        users_returned = session.query(User).filter(User.user_id == user_id).all()
        session.close()

        if len(users_returned) != 1:
            raise KeyError("User {} not found".format(user_id))
        else:
            return users_returned[0]

    def user_exists(self, user_id):
        '''
        Return true if user_id exists, false if not
        '''
        try:
            user = self._get_user_by_id(user_id)
            return True
        except KeyError:
            return False

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
        If new phone number is not valid, throw ValueError
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
        session.close()

    def _add_a_user(self, user_id, phone, name):
        validate_phone_number(phone)

        session = self._SessionMaker()

        user = User()
        user.name = name
        user.user_id = user_id
        user.phone = phone

        session.add(user)
        session.commit()
        session.close()


