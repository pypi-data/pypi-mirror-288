class DuplicateEntry(Exception):
    pass

class InvalidForeignKey(Exception):
    pass

class NullEntry(Exception):
    pass

class NoRowFound(Exception):
    pass

class MultipleRowsFound(Exception):
    pass

def get_violation_type(error_cause):
    code = error_cause.pgcode
    # print(code)
    # print(error_cause)
    if code == '23505':
        return DuplicateEntry
    elif code == '23502':
        return NullEntry
    elif code == '23503':
        return InvalidForeignKey
        
    
