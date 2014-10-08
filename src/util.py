import re

def validate_phone_number(number):
    '''
    Raise ValueError if phone number is not a ten digit numeric string
    '''
    if not (re.match(r'^\d+$', number) and len(number) == 10):
        raise ValueError('Phone number {} is not a ten digit numeric string'.format(number))
