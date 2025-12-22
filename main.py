from bank import Customer, SavingsAccount, CheckingAccount, BusinessAccount, AccountManagement
from exceptions import InvalidLoan

personal_manager = AccountManagement("customers.json", [])
personal_manager.load_data()
data = personal_manager.data_list

savings_manager = AccountManagement("savingsacc.json", [])
savings_manager.load_data()
data2 = savings_manager.data_list

checking_manager = AccountManagement("checkingacc.json", [])
checking_manager.load_data()
data3 = checking_manager.data_list

business_manager = AccountManagement("businessacc.json", [])
business_manager.load_data()
data4 = business_manager.data_list

def main():
    menu = '''
    Welcome to the National Bank.
    Please proceed with what you wish to do.'''

    options = [1, 2, 3, 4]

    choices = '''
    1. Personal Account - the one which creates Bank membership
    2. Savings Account - for long term savings
    3. Checking Account - everyday usage
    4. Business Account - for business owners
    '''
    print(menu)
    print(choices)

    while True:
        try:
            choice = int(input('Choose one of the available options by inserting its number(1-4): '))
            if choice in options:
                break
            else:
                print('Choose a number within the given range.')
        except ValueError:
            print('Invalid choice. Please try again.')

    if choice == 1:
        personal_account()
    elif choice == 2:
        savings_account()
    elif choice == 3:
        checking_account()
    else:
        business_account()

def personal_account():
    menu = '''
What do you wish to do(enter only number): 
1. Create a personal account
2. Get account data
3. Edit account data
4. Delete account''' 
    print(menu)
    try:
        num = int(input('Insert choice here: '))
        if num not in [1, 2, 3, 4]:
            print('Invalid choice')
            return
    except ValueError:
        print('Invalid choice, enter a number.')
        return

    if num == 1:
        personal_manager.load_data()

        name = input("Enter your name: ").lower().strip()
        surname = input("Enter your surname: ").lower().strip()
        phone_number = input('Enter your phone number: ')
        email = input('Enter your email address: ').lower().strip()
        try:
            main_id = int(input("Enter your main id as set in the contract: ").strip())
        except ValueError:
            print("Please enter only numbers.")
            return

        new_customer = Customer(name, surname, email, phone_number, main_id)
    
        personal_manager.add(new_customer)

        print('Account created successfully.')

    elif num == 2:
        personal_manager.load_data()

        try:
            mainid = int(input("Enter your main id to view your account: ").strip())
        except ValueError:
            print("Enter a valid id.")
            return

        account_info = personal_manager.find(mainid, key="main_id")

        if not account_info:
            print("Account not found.")
            return

        acc = Customer.obj_form(account_info)
        print(acc)

    elif num == 3:
        personal_manager.load_data()
        try:
            idu = int(input("Enter you id: ").strip())
        except ValueError:
            print("Invalid value.")
            return

        print("You can only change your email or phone number. For more information contact or visit our bank.")
        chc = input("Choose what you want to change(e for email or p for phone number): ").lower().strip()

        account_info = personal_manager.find(idu, key="main_id")

        if not account_info:
            print("Account not found.")
            return

        acc = Customer.obj_form(account_info)

        if chc == "e":
            change = input("Enter your new email: ").lower().strip()
            account_info["email"] = change
            print("Email changed successfully.")
        elif chc == "p":
            change = input("Enter your new phone number: ").strip()
            account_info["phone"] = change
            print("Phone number changed successfully.")
        else:
            print("Invalid choice.")
            return      

        personal_manager.save_data()

    elif num == 4:
        personal_manager.load_data()

        print("To delete your account, first enter your id to verify it's you.")
        try:
            uid = int(input("Enter id: "))
        except ValueError:
            print("Invalid id, try again.")
            return
        
        done = personal_manager.delete(uid, "main_id")
        if done:
            print("Account deleted successfully.")
            personal_manager.save_data()
        else:
            print("Something went wrong. Check your id or try again.")
  

def savings_account():
    menu = '''
Choose what you wish to do:
1. Create a Savings Account
2. Withdraw money
3. Show current balance
4. Delete account'''
    print(menu)
    try:
        num = int(input('Choose a number: ').strip())
        if num not in [1, 2, 3, 4]:
            print('Invalid choice.')
            return
    except ValueError:
        print('Invalid choice, must enter number.')
        return

    if num == 1:
        savings_manager.load_data()
        data2 = savings_manager.data_list

        owner = input("Enter the owner's full name: ").lower().strip()
        try:
            user_id = int(input('Enter your ID: ').strip())
            interest = float(input('Enter interest rate: ').strip())
            years = int(input('Enter years: ').strip())
            deposit = float(input('Emter amount that will be deposited: ').strip())
        except ValueError:
            print('Invalid numeric value.')
            return

        new_acc = SavingsAccount(owner, user_id, interest, years) 
        new_acc.deposit(deposit)

        savings_manager.add(new_acc)

        print('Account created successfully.')
    
    elif num == 2:
        savings_manager.load_data()
        data2 = savings_manager.data_list

        print("To withdraw money, first you must give the account id: ")
        try:
            accid = int(input("Enter id: ").strip())
        except ValueError:
            print("Invalid value.")
            return
  
        account_data = savings_manager.find(accid, key="id")
        
        if not account_data:
            print("No account found.")
            return
    
        account = SavingsAccount.obj_form(account_data)

        try:
            wamount = float(input("Enter amount to be withdrawn: "))
        except ValueError:
            print("Invalid amount.")
            return

        account.withdraw(wamount)
        print("Withdrawal finished successfully.")

        for i in range(len(data2)):
            if data2[i]["id"] == accid:
                data2[i] = account.dictform()

        savings_manager.save_data()

    elif num == 3:
        savings_manager.load_data()
        #data2 = savings_manager.data_list

        try:
            idd = int(input("To view current balance for today, enter your id: ").strip())
        except ValueError:
            print("Invalid value.")
            return

        acc_data = savings_manager.find(idd, key="id")
        
        if not acc_data:
            print("No account found.")
            return

        this_acc = SavingsAccount.obj_form(acc_data)

        print(this_acc.show_balance())

    else:
        savings_manager.load_data()

        print("To delete your account, first enter your id to verify it's you.")
        try:
            id4 = int(input("Enter id: "))
        except ValueError:
            print("Invalid id, try again.")
            return
        
        done = savings_manager.delete(id4, "id")
        if done:
            print("Account deleted successfully.")
            savings_manager.save_data()
        else:
            print("Something went wrong. Check your id or try again.")

def checking_account():
    menu = '''
Choose what you wish to do: 
1. Create a Checking Account
2. Withdraw money
3. View amount available
4. Delete account'''

    print(menu)
    try:
       num = int(input("Enter number: "))
       if num not in [1, 2, 3, 4]:
           print("Invalid choice.")
           return
    except ValueError:
        print("Enter a number.")
        return

    if num == 1:
        checking_manager.load_data()
        data3 = checking_manager.data_list

        owner = input("Enter your name and surname: ").lower().strip()
        
        try: 
            acc_id = int(input("Enter your id: ").strip())
            overdraft_limit = float(input("Enter overdraft limit as set in the contract: ").strip())
            fee = float(input("Enter fee as set in the contract: ").strip())
        except ValueError:
            print("Value must be a number.")
            return
        
        new_acc = CheckingAccount(owner, acc_id, overdraft_limit, fee) 

        try:
            amount = float(input("Enter amount to be deposited on your account: "))
        except ValueError:
            print("Invalid amount.")
            return
        
        print("Account created successfully.")
        print(new_acc.deposit(amount))
        
        checking_manager.add(new_acc)
        checking_manager.save_data()
        
    elif num == 2:
        checking_manager.load_data()
        data3 = checking_manager.data_list

        print("Enter account id and sum you want to withdraw.")
        
        try:
            idd = int(input("Account id: ").strip())
            wamount = float(input("Amount: ").strip())
        except ValueError:
            print("Invalid amount.")
            return

        account_data = checking_manager.find(idd, key="id")
        if not account_data:
            print("No account found.")
            return

        accountt = CheckingAccount.obj_form(account_data)

        print(accountt.withdraw(wamount))
        account_data["balance"] = accountt.balance

        checking_manager.save_data()

    elif num == 3:
        checking_manager.load_data()
        data3 = checking_manager.data_list

        print("Enter account id to see the amount available.")
        try:
            a_id = int(input("Account Id: ").strip())
        except ValueError:
            print("Invalid value.")
            return

        account_data = checking_manager.find(a_id, key="id")
        if not account_data:
            print("No account found.")
            return

        accounty = CheckingAccount(account_data["owner"], account_data["id"], account_data["overdraft_limit"], account_data["fee"])
        accounty.balance = account_data["balance"]
            
        av = accounty.available()

        print(f"The amount available this account is {av}.")

    elif num == 4:
        checking_manager.load_data()

        print("To delete your account, first enter your id to verify it's you.")
        try:
            uid = int(input("Enter id: "))
        except ValueError:
            print("Invalid id, try again.")
            return
        
        done = checking_manager.delete(uid, "id")
        if done:
            print("Account deleted successfully.")
            checking_manager.save_data()
        else:
            print("Something went wrong. Check your id or try again.")

def business_account():
    menu = '''Welcome to your Business Account.
1. Create a business account
2. Authorize users
3. Withdraw money
4. Transfer money
5. Take a loan
6. Delete account'''
    print(menu)
    try:
        choice = int(input("Choose what you wish to do: ").strip())
    except ValueError:
        print("Enter only numbers.")
        return

    if choice not in [1, 2, 3, 4, 5, 6]:
        print("Invalid choice, try again.")
        return

    elif choice == 1:
        business_manager.load_data()
        data4 = business_manager.data_list

        owner = input("Enter the full name of the owner: ").lower().strip()
        try:
            acc_id = int(input("Enter the account id: ").strip())
        except ValueError:
            print("Invalid value.")
            return
        
        business_name = input("Enter business name: ").lower().strip()

        new_acc = BusinessAccount(owner, acc_id, business_name)

        try:
            damount = float(input("Enter amount to be deposited: ").strip())
        except ValueError:
            print("Value must be a number.")
            return
        
        print("New account created successfully.")
        print(new_acc.deposit(damount)) 

        business_manager.add(new_acc)
        business_manager.save_data()


    elif choice == 2:
        business_manager.load_data()
        data4 = business_manager.data_list

        print("To authorize someone, enter their user and their given id.")
        user = input("User: ").lower().strip()
        try:
            user_id = int(input("ID: ").strip())
            account_id = int(input("Enter the id of your account: ").strip())
        except ValueError:
            print("Invalid value.")
            return

        account_data = business_manager.find(account_id, key="id")
        if not account_data:
            print("Account not found.")
            return

        changing = BusinessAccount.obj_form(account_data)
        changing.authorize_user(user, user_id)  
        account_data["authorized_users"] = changing.authorized_users

        print(f"{user.title()} was authorized.")
        
        business_manager.save_data()

    elif choice == 3:
        business_manager.load_data()
        data4 = business_manager.data_list
        
        print("To withdraw money: ")
        try:
            user_idd = int(input("Enter your id: ").strip())
            acc_idd = int(input("Enter account id: ").strip())
            am = float(input("Enter amount to withdraw: "))
        except ValueError:
            print("Invalid value.")
            return
        
        account_info = None

        account_info = business_manager.find(acc_idd, key="id")
        if not account_info:
            print("Account not found.")
            return

        accm = BusinessAccount.obj_form(account_info)

        print(accm.withdraw(user_idd, am))
        account_info["balance"] = accm.balance

        business_manager.save_data()

    elif choice == 4:
        business_manager.load_data()
        data4 = business_manager.data_list

        print("To transfer money to another account you must enter some data.")

        try:
            our_id = int(input("Enter your company's id: ").strip())
            other_id = int(input("Enter the id of the other account: ").strip())
            amnt = float(input("Enter the amount to be transferred: ").strip())
        except ValueError:
            print("Invalid value.")
            return
        
        if our_id == other_id:
            print("You cannot transfer to the same account.")
            return
        
        sender_info = None

        if not any(acc["id"] == other_id for acc in data4):
            print("Enter a valid id for the account to which you will transfer.")
        else:
            for acc in data4:
                if acc["id"] == our_id:
                    sender_info = acc
                    break
            
            if not sender_info:
                print("Account not found.")
                return

            sender_acc = BusinessAccount.obj_form(sender_info)

            recipient_info = business_manager.find(other_id, key="id")
            if not recipient_info:
                print("Account not found.")
                return

            recipient_acc = BusinessAccount.obj_form(recipient_info)

            print(sender_acc.transfers_out(recipient_acc, amnt))
            
            sender_info["balance"] = sender_acc.balance
            sender_info["transactions"] = sender_acc.transactions

            recipient_info["balance"] = recipient_acc.balance
            recipient_info["transactions"] = recipient_acc.transactions

            business_manager.save_data()

    elif choice == 5:
        business_manager.load_data()
        data4 = business_manager.data_list

        try:
            idu = int(input("Enter the account id to take a loan: ").strip())
            amount = float(input("Amount to loan: ").strip())
            intr = float(input("Enter interest as set in the contract: ").strip())
            years = int(input("Enter the amount of years: ").strip())
        except ValueError:
            print("Please enter a valid number.")
            return
        
        account_info = business_manager.find(idu, key="id")
        if not account_info:
            print("Account not found.")
            return

        acc = BusinessAccount.obj_form(account_info)

        try:
            acc.take_loan(amount, intr, years)
        except InvalidLoan as e:
            print(e)
            return

        acc.loan_payment()

        account_info["loans"] = acc.loans
        account_info["balance"] = acc.balance

        print("Loan taken successfully. Payment process has begun.")
        
        business_manager.save_data()

    elif choice == 6:
        business_manager.load_data()

        print("To delete your account, first enter your id to verify it's you.")
        try:
            uid = int(input("Enter id: "))
        except ValueError:
            print("Invalid id, try again.")
            return
        
        done = business_manager.delete(uid, "id")
        if done:
            print("Account deleted successfully.")
            business_manager.save_data()
        else:
            print("Something went wrong. Check your id or try again.")
            
if __name__ == '__main__':
    main()