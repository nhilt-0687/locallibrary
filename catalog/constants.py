from enum import Enum
<<<<<<< HEAD

=======
>>>>>>> a2457d3 (Django Tutorial Part 5: Creating Our Home Page (#9))
MAX_LENGTH_NAME = 200
MAX_LENGTH_AUTHOR_NAME = 100
MAX_LENGTH_ISBN = 13
MAX_LENGTH_SUMMARY = 1000
MAX_LENGTH_UNIQUE_ID = 20

class LoanStatus(Enum):
    MAINTENANCE = 'm'
    ON_LOAN = 'o'
    AVAILABLE = 'a'
    RESERVED = 'r'

DEFAULT_IMPRINT = 'Penguin Group'
