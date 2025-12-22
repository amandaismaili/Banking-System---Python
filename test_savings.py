import pytest
from bank import SavingsAccount

@pytest.fixture
def savings_obj():
    account = SavingsAccount('Angela Bellona', 93224, 0.7, 6, 5000)
    return account

def test_deposit(savings_obj):
    balance = savings_obj.balance
    amount = 300
    savings_obj.deposit(amount)
    assert savings_obj.balance == balance + amount

def test_withdraw(savings_obj):
    amount = 100
    savings_obj.withdraw(amount)
    assert savings_obj.balance == 4900

def test_show_balance(savings_obj):
    answ = savings_obj.show_balance()
    assert str(savings_obj.balance) in answ
    assert str(savings_obj.interest) in answ

def test_obj_form(savings_obj):
    account_info = {
        "owner": savings_obj.owner,
        "id": savings_obj.id,
        "balance": savings_obj.balance,
        "interest": savings_obj.interest,
        "years": savings_obj.years
    }

    new = SavingsAccount.obj_form(account_info)
    assert isinstance(new, SavingsAccount)
    assert new.owner == savings_obj.owner
    assert new.id == savings_obj.id
    assert new.balance == savings_obj.balance
    assert new.interest == savings_obj.interest
    assert new.years == savings_obj.years