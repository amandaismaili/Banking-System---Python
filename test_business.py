import pytest
from bank import BusinessAccount

@pytest.fixture
def business_obj1():
    account1 = BusinessAccount("John Berkley", 77766, "Berkley Corp", 
                              [{"name": "John Berkley", "personal_id": 77766}, 
                               {"name": "Mia Berkley", "personal_id": 99987},
                               {"name": "Esla Toorn", "personal_id": 48485}])
    account1.balance = 40000
    return account1

@pytest.fixture
def business_obj2():
    account2 = BusinessAccount("Amis Nesm", 33333, "Factory 55", 
                               [{"name": "Amis Nesm", "personal_id": 33333}])
    account2.balance = 35000
    return account2

def test_authorize_user(business_obj1):
    user = {
        "name": "Brand Tress",
        "personal_id": 38535
    }

    business_obj1.authorize_user(user["name"], user["personal_id"])

    assert user in business_obj1.authorized_users

def test_deposit(business_obj1):
    initial_balance = business_obj1.balance
    amount = 5000
    business_obj1.deposit(amount)

    assert business_obj1.balance == initial_balance + amount

def test_withdrawal(business_obj1):
    user_id = 77766
    amount = 2000
    initial_balance = business_obj1.balance

    business_obj1.withdraw(user_id, amount)

    assert business_obj1.balance == initial_balance - amount

def test_transferts_out(business_obj1, business_obj2):
    transaction = {
        "type": "transfer out",
        "amount": 500,
        "date": "2025-11-30T14:44:32.504137",
        "balance": 30000
    }

    initial_balance1 = business_obj1.balance
    initial_balance2 = business_obj2.balance

    supposed = initial_balance1 - transaction["amount"]
    supposed2 = initial_balance2 + transaction["amount"]

    business_obj1.transfers_out(business_obj2, transaction["amount"])

    last_transaction1 = business_obj1.transactions[-1]

    assert business_obj1.balance == supposed 
    assert business_obj2.balance == supposed2

    assert last_transaction1["type"] == transaction["type"]
    assert last_transaction1["amount"] == transaction["amount"]
    
def test_take_loan(business_obj1):
    amount = 100
    rate = 1.5
    years = 5

    business_obj1.take_loan(amount, rate, years)

    assert amount == business_obj1.loans[-1]["amount"]
    assert rate == business_obj1.loans[-1]["interest"]
    assert years == business_obj1.loans[-1]["years"]

def test_obj_form(business_obj1):
    account_info = {
        "owner": business_obj1.owner,
        "id": business_obj1.id, 
        "business_name": business_obj1.business_name,
        "authorized_users": business_obj1.authorized_users,
        "balance": business_obj1.balance,
        "transactions": business_obj1.transactions,
        "loans": business_obj1.loans
    }
    
    new = BusinessAccount.obj_form(account_info)
    assert isinstance(new, BusinessAccount)
    assert new.owner == business_obj1.owner
    assert new.id == business_obj1.id
    assert new.business_name == business_obj1.business_name
    assert new.authorized_users == business_obj1.authorized_users
    assert new.balance == business_obj1.balance
    assert new.transactions == business_obj1.transactions
    assert new.loans == business_obj1.loans