from abc import ABC, abstractmethod
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import json
from exceptions import PositiveNumber, CheckingFeeValue, InsufficientFunds, DailyLimit, IdValue, OverdraftLimit, InvalidLoan, InsufficientAmount, UnauthorizedUser

        
class BankAccount(ABC):
    def __init__(self, owner, id):
        self.owner = owner
        self._id = id
        self._balance = 0

    def dictform(self):
        return {
            'owner': self.owner,
            'id': self.id,
            'balance': self._balance
        }
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise IdValue
        self._id = value

    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, val):
        if not isinstance(val, (int, float)):
            raise TypeError('The balance should be a numerical value.')
        self._balance = val

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, *args, **kwargs):
        pass

    def show_balance(self):
        today = date.today()
        return f'The balance for {today} is {self.balance}.'

class Customer():
    def __init__(self, name, surname, email, phone_number, main_id):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone_number = phone_number
        self.main_id = main_id

    def __str__(self):
        return f'''{self.name.capitalize()} {self.surname.capitalize()}
Account id: {self.main_id}
Phone number: {self.phone_number}
Email: {self.email}'''
    
    def dictform(self):
        return {
            'name': self.name,
            'surname': self.surname, 
            'email': self.email,
            'phone': self.phone_number,
            'main_id': self.main_id
        }
    
    @classmethod
    def obj_form(cls, data):
        account = cls(data["name"], data["surname"], data["email"], data["phone"], data["main_id"])
        return account

class SavingsAccount(BankAccount):
    def __init__(self, owner, id, interest, years, balance=0):
        super().__init__(owner, id)

        if interest <= 0:
            raise PositiveNumber("Interest rate must be positive.")
        self.interest = float(interest)

        if years <= 0:
            raise PositiveNumber()
        self.years = years

        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise PositiveNumber()
        self.balance += amount
        return self.balance
        
    def withdraw(self, amount):
        if amount <= 0:
            raise PositiveNumber()
        if amount > self._balance:
            raise InsufficientFunds()
        daily_limit = self.balance/24
        if amount > daily_limit:
            raise DailyLimit
        self.balance -= amount
        return self.balance

    def show_balance(self):
        base_balance = super().show_balance()
        return f"{base_balance} The interest rate is {self.interest}."

    def dictform(self):
        base = super().dictform()
        base.update({
            'interest': self.interest,
            'years': self.years,
            'balance': self._balance
        })
        return base

    @classmethod 
    def obj_form(cls, data):
        account = cls(data["owner"], data["id"], data["interest"], data["years"])
        account.balance = data.get("balance", 0.0)
        return account

class CheckingAccount(BankAccount):
    def __init__(self, owner, id,  overdraft_limit, fee, balance = 0):
        super().__init__(owner, id)
        self._overdraft_limit = overdraft_limit
        if not (0<=fee<1):
            raise CheckingFeeValue() 
        self.fee = fee
        self.balance = balance
    
    def dictform(self):
        base = super().dictform()
        base.update({
            'overdraft_limit': self._overdraft_limit,
            'fee': self.fee,
            'balance': self.balance
        })
        return base

    def deposit(self, amount):
        if amount < 0:
            raise PositiveNumber()
        self.balance += amount
        return f'${amount} was the amount deposited for everyday usage' 

    def withdraw(self, amount):
        if amount > self._balance + self._overdraft_limit:
            raise OverdraftLimit()
        if amount <= 0:
            raise PositiveNumber()
        self.balance -= amount
        fee = amount * self.fee
        self.balance -= fee
        return f'${amount} was withdrawn with a fee of {self.fee * 100}%. The balance now: ${self.balance}.'

    def available(self):
        return self._balance + self._overdraft_limit
    
    @classmethod 
    def obj_form(cls, data):
        account = cls(data["owner"], data["id"], data["overdraft_limit"], data["fee"])
        account.balance = data.get("balance", 0.0)
        return account
    
class BusinessAccount(BankAccount):
    def __init__(self, owner, id, business_name, authorized_users = None,):
        super().__init__(owner, id)
        self.business_name = business_name
        self.authorized_users = authorized_users if authorized_users else []
        self.transactions = []
        self.loans = []

    def dictform(self):
        base = super().dictform()
        base.update({
            'business_name': self.business_name,
            'authorized_users': self.authorized_users,
            'transactions': self.transactions,
            'loans': self.loans
        })
        return base

    def authorize_user(self, user, personal_id):
        if not any(u["personal_id"] == personal_id for u in self.authorized_users):
            self.authorized_users.append({"name": user, "personal_id": personal_id})
  
    def deposit(self, amount):
        if amount <= 0:
            raise PositiveNumber()
        self.balance += amount
        return f'${amount} was the amount deposited. The balance now: ${self.balance}.'

    def withdraw(self, user_id, amount):
        if not any(u["personal_id"] == user_id for u in self.authorized_users):
            raise UnauthorizedUser()

        if amount <= 0:
            raise PositiveNumber() 
        if amount > self.balance:
            raise InsufficientFunds()
        self.balance -= amount
        return "Withdrawal was successful."
    
    def save_transaction(self, type, amount):
        self.transactions.append({
                "type": type,
                "amount": amount,
                "date": datetime.now().isoformat(),
                "balance": self.balance             
            })
    
    def transfers_out(self, other_account, amount):
        if amount <= 0:
            raise PositiveNumber() 
        if amount > self.balance:
            raise InsufficientFunds()
        
        self.balance -= amount
        self.save_transaction("transfer out", amount)
        other_account.balance += amount
        other_account.save_transaction("transfer in", amount)

        return f'${amount} was transfered to account with id {other_account.id}.'

    def take_loan(self, amount, interest, years):
        if amount <= 0 or years <= 0:
            raise InvalidLoan()

        self.balance += amount
        monthss = years * 12
        monthly_rate = interest / 12
        taken = datetime.today()

        monthly_payback = amount * (monthly_rate * (1 + monthly_rate) ** monthss) / ((1 + monthly_rate) ** monthss - 1)

        self.loans.append({
            'amount': amount,
            'interest': interest,
            'years': years,
            'remaining_months': monthss,
            'monthly_payback': monthly_payback,
            'date_taken': taken.isoformat(),
            'next_payment': (taken + relativedelta(months=1)).isoformat()
        })
 
    def loan_payment(self):
        today = datetime.today()

        for loan in self.loans:
            next_p = datetime.fromisoformat(loan['next_payment'])

            while next_p <= today and loan['remaining_months'] > 0:
 
                if self._balance >= loan['monthly_payback']:
                    self._balance -= loan['monthly_payback']
                else:
                    raise InsufficientAmount()

                loan['remaining_months'] -= 1
                next_p = next_p + relativedelta(months=1)

            loan['next_payment'] = next_p.isoformat()
    
    @classmethod
    def obj_form(cls, data):
        account = cls(data["owner"], data["id"], data["business_name"], data["authorized_users"])
        account.balance = data.get("balance", 0.0)
        account.transactions = data.get("transactions", [])
        account.loans = data.get("loans", [])
        return account

class AccountManagement:
    def __init__(self, file_name, data_list):
        self.file_name = file_name
        self.data_list = data_list

    def load_data(self):
        try:
            with open(self.file_name, 'r') as file:
                content = file.read().strip()

            self.data_list = json.loads(content) if content else []
        
        except (FileNotFoundError, json.JSONDecodeError):
            print('There was a problem loading this file(not well read or may not exist).')
            self.data_list = []

        return self.data_list

    def save_data(self):
        with open(self.file_name, "w") as file:
            json.dump(self.data_list, file, indent=4)

    def add(self, account):
        self.data_list.append(account.dictform())
        self.save_data()

    def find(self, id, key):
        for acc in self.data_list:
            if acc.get(key) == id:
                return acc
        return None
    
    def delete(self, id, key):
        for acc in self.data_list:
            if acc.get(key) == id:
                self.data_list.remove(acc)
                return True
        return False