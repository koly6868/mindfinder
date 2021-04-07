import string



ALLOWED_SYMBOLS = string.ascii_letters + '_.' + string.digits



def is_str_allowed(s : str) -> bool:
    return all([e in ALLOWED_SYMBOLS for e in s])