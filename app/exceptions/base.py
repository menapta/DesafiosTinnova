class BusinessException(Exception):
    def __init__(self, message: str):
        self.message = message

class EntityNotFoundException(BusinessException):
    pass

class DuplicateEntryException(BusinessException):
    pass

class InvalidYearException(BusinessException):
    pass