import re


def validate_email(email):
    email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    valid = re.match(email_pattern, email)
    return {'success': True, 'error': ''} if valid else {'success': False, 'error': email + ' is not a valid Email ID'}


def validate_phone(phone):
    phone_pattern = r"^(?:\+91|91|0)?[-\s]?[6-9]\d{2}[-\s]?\d{3}[-\s]?\d{4}$"
    valid = re.match(phone_pattern, phone)
    return {'success': True, 'error': ''} if valid else {'success': False,
                                                         'error': phone + ' is not a valid Phone Number'}
