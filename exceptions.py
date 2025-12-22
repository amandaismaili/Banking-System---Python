class PositiveNumber(Exception):
    def __init__(self, message="The value must be positive."):
        super().__init__(message)

class CheckingFeeValue(Exception):
    def __init__(self, message="The value of the fee must be between 0 and 1."):
        super().__init__(message)

class InsufficientFunds(Exception):
    def __init__(self, message="Insufficient funds for this action."):
        super().__init__(message)

class DailyLimit(Exception):
    def __init__(self, message="Withdrawal cannot be complete, daily limit exceeded."):
        super().__init__(message)

class IdValue(Exception):
    def __init__(self, message="ID must only contain numbers."):
        super().__init__(message)

class OverdraftLimit(Exception):
    def __init__(self, message="'Withdrawal cannot be completed, overdraft limit has been reached.'"):
        super().__init__(message)

class InvalidLoan(Exception):
    def __init__(self, message="Invalid loan credentials(time or year)."):
        super().__init__(message)

class InsufficientAmount(Exception):
    def __init__(self, message="Amount not sufficient."):
        super().__init__(message)

class UnauthorizedUser(Exception):
    def __init__(self, message="This user is not authorized."):
        super().__init__(message)