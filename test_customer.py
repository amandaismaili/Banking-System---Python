from bank import Customer

def test_str_func():
    new_customer = Customer("amelia", "smith", "ameliasmith@yahoo.com", "054 347 4927", 53853)
    print(new_customer)
    expected = (
        "Amelia Smith\n"
        "Account id: 53853\n"
        "Phone number: 054 347 4927\n"
        "Email: ameliasmith@yahoo.com" 
    )
    assert str(new_customer) == expected

def test_obj_form():
    account_info = {
        "name": "amelia",
        "surname": "smith",
        "email": "ameliasmith@yahoo.com",
        "phone": "054 347 4927",
        "main_id": 53853
    }

    new = Customer.obj_form(account_info)

    assert isinstance(new, Customer)
    assert new.name == "amelia"
    assert new.surname == "smith"
    assert new.email == "ameliasmith@yahoo.com"
    assert new.phone_number == "054 347 4927"
    assert new.main_id == 53853