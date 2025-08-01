from enum import Enum


MAX_LENGTH_NAME = 200
MAX_LENGTH_AUTHOR_NAME = 100
MAX_LENGTH_ISBN = 13
MAX_LENGTH_SUMMARY = 1000
MAX_LENGTH_UNIQUE_ID = 20


DEFAULT_PAGINATION_SIZE = 10


class LoanStatus(Enum):
    MAINTENANCE = 'm'
    ON_LOAN = 'o'
    AVAILABLE = 'a'
    RESERVED = 'r'


DEFAULT_IMPRINT = 'Penguin Group'
