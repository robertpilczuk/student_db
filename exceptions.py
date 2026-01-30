class StudentDbError(Exception):
    pass


class ValidationError(StudentDbError):
    pass


class NotFoundError(StudentDbError):
    pass


class DuplicateError(StudentDbError):
    pass


class StorageError(StudentDbError):
    pass
