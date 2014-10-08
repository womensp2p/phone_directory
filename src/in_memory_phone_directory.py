import re

from collections import defaultdict
from phone_directory_actions import PhoneDirectoryActions


class SimplisticPhoneDirectoryActions(PhoneDirectoryActions):
    '''
    Data stored in a python dict. Data does not persist between app instances.
    '''

    def __init__(self):
        self.archive = defaultdict(list)
        self.directory = {
            1000: {'name': 'Leah', 'phone': '2061234567',},
            1001: {'name': 'Rachel', 'phone': '2061111111',}
        }

    def user_exists(self, userid):
        '''
        Return true if userid exists, false if not
        '''
        return userid in self.directory

    def get_phone_number(self, userid):
        '''
        Return phone number for given userid. Throw KeyError if user doesn't exist.
        '''
        self._verify_userid_exists(userid)
        return self.directory[userid]['phone']

    def get_name(self, userid):
        '''
        Return username for given userid. Throw KeyError if user doesn't exist.
        '''
        self._verify_userid_exists(userid)
        return self.directory[userid]['name']

    def update_phone_number(self, userid, new_number):
        '''
        If userid exists, update its phone number and archive the old number.
        If userid does not exist, throw KeyError
        If new phone number is not valid, throw 
        '''
        self._verify_userid_exists(userid)
        self._validate_phone_number(new_number)
        old_number = self.directory[userid]['phone']
        self.archive[userid].append(old_number)
        self.directory[userid]['phone'] = new_number

    def _verify_userid_exists(self, userid):
        '''
        Throw KeyError if user doesn't exist
        '''
        if userid not in self.directory:
            raise KeyError('User ID {} not found in the directory'.format(userid))

    def _validate_phone_number(number):
        '''
        Raise ValueError if phone number is not a ten digit numeric string
        '''
        if not (re.match(r'^\d+$', number) and len(number) == 10):
            raise ValueError('Phone number {} is not a ten digit numeric string'.format(number))
