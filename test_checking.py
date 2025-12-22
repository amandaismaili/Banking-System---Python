import pytest
from bank import CheckingAccount

@pytest.fixture
def checking_obj():
    account = CheckingAccount("Elis Tween", 11233, overdraft_limit=0.2, fee=0.14, balance=2000)
    return account

def test_deposit(checking_obj):
    balance = checking_obj.balance
    amount = 3000
    checking_obj.deposit(amount)

    assert checking_obj.balance == amount + balance

def test_withdraw(checking_obj):
    balance = checking_obj.balance
    amount = 100
    checking_obj.withdraw(amount)

    assert checking_obj.balance == balance - (amount + amount * checking_obj.fee)

def test_available(checking_obj):
    ans = checking_obj.available()
    total = checking_obj.balance + checking_obj._overdraft_limit

    assert total == ans

def test_obj_form(checking_obj):
    account_info = {
        "owner": checking_obj.owner,
        "id": checking_obj.id,
        "balance": checking_obj.balance,
        "overdraft_limit": checking_obj._overdraft_limit,
        "fee": checking_obj.fee
    }

    new = CheckingAccount.obj_form(account_info)

    assert isinstance(new, CheckingAccount)
    assert new.owner == checking_obj.owner
    assert new.id == checking_obj.id
    assert new.balance == checking_obj.balance
    assert new._overdraft_limit == checking_obj._overdraft_limit
    assert new.fee == checking_obj.fee