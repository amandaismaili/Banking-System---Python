from fastapi import FastAPI, Path, Query, HTTPException, APIRouter
from typing import Optional, List
from pydantic import BaseModel
from creation import app
from bank import Customer, AccountManagement, SavingsAccount, CheckingAccount, BusinessAccount
from exceptions import *

router = APIRouter(prefix="/accounts")

# connection with json files
personal_manager = AccountManagement("customers.json", [])
info = personal_manager.load_data()

savings_manager = AccountManagement("savingsacc.json", [])
savings_manager.load_data()

checking_manager = AccountManagement("checkingacc.json", [])
checking_manager.load_data()

business_manager = AccountManagement("businessacc.json", [])
business_manager.load_data()

#classes

class Customermodel(BaseModel):
    name: str
    surname: str
    email: str
    phone_number: str
    main_id: int

class UpdateCustomer(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None

class Savingsmodel(BaseModel):
    owner: str
    main_id: int
    interest: float
    years: int
    balance: float

class SavingsTransactions(BaseModel):
    amount: float

class Checkingmodel(BaseModel):
    owner: str 
    main_id: int
    overdraft_limit: float
    fee: float
    balance: float

class CheckingTransactions(BaseModel):
    amount: float

class Businessmodel(BaseModel):
    owner: str
    main_id: int
    business_name: str
    authorized_users: List[int]

class UserAuthorization(BaseModel):
    acc_id: int

class BusinessTransactions(BaseModel):
    user_id: int
    amount: float
    
class Transfers(BaseModel):
    user_id: int
    amount: float
    other_id: int

class Loan(BaseModel):
    user_id: int
    amount: float
    intr: float
    years: int

class DelBusiness(BaseModel):
    user_id: int

#URLS FOR CUSTOMER ACCOUNTS

@router.post("/customer")
def create_customer_account(customer: Customermodel):
    try:
        account = Customer( 
            customer.name,
            customer.surname,
            customer.email,
            customer.phone_number,
            customer.main_id
        )

        personal_manager.add(account)

        return {
            "message": "Account created successfully",
            "main_id": customer.main_id
        }
         
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/customer/{acc_id}")
def get_customer(acc_id : int = Path(description="Enter the id of your account: ")):
    account_info = personal_manager.find(acc_id, key="main_id")
    if not account_info:
        raise HTTPException(status_code=404, detail="Account not found.")

    acc = Customer.obj_form(account_info)
    return acc

@router.put("/customer/{acc_id}/update")
def update_customer_account(acc_id: int, account: UpdateCustomer):

    acc = personal_manager.find(acc_id, key="main_id")

    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    customer = Customer.obj_form(acc)

    customer.update(
        email = account.email,
        phone_number = account.phone_number
    )
    personal_manager.save_data()
    
    return {
        "message": "Account updated successfully."
    }
    
@router.delete("/customer/{acc_id}")
def delete_customer_account(acc_id: int):
    done = personal_manager.delete(acc_id, "main_id")

    if not done:
        raise HTTPException(status_code=404, detail="Account not found")

    personal_manager.save_data()
        
    return {
        "message": "Account deleted successfully."
    }   

# URLS FOR SAVINGS ACCOUNTS

@router.post("/savings")
def create_savings_account(savings: Savingsmodel):
    try:
        account = SavingsAccount(
            savings.owner,
            savings.main_id,
            savings.interest,
            savings.years,
            savings.balance
        )

        savings_manager.add(account)

        return {
            "message": "Account created successfully.",
            "main_id": savings.main_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/savings/{acc_id}")
def get_savings(acc_id: int = Path(description="Enter account id.")):
    account_data = savings_manager.find(acc_id, key="id")
    
    if not account_data:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    acc = SavingsAccount.obj_form(account_data)
    return acc

@router.post('/savings/{acc_id}/withdraw')
def withdraw_savings(acc_id: int, req: SavingsTransactions):
    account_data = savings_manager.find(acc_id, key="id")
    if not account_data:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    acc = SavingsAccount.obj_form(account_data)

    try: 
        acc.withdraw(req.amount)
        savings_manager.save_data()
        return {
            "message": "Amount withdrawn successfully."
        }
    except PositiveNumber:
        raise HTTPException(status_code=400, detail="Amount must be positive.")
    except InsufficientFunds:
        raise HTTPException(status_code=400, detail="Insufficient funds.")
    except DailyLimit:
        raise HTTPException(status_code=400, detail="Amount exceeds daily limit.")
    
@router.post('/savings/{acc_id}/deposit')
def deposit_savings(acc_id: int, req: SavingsTransactions):
    account_data = savings_manager.find(acc_id, key="id")
    if not account_data:
        raise HTTPException(status_code = 404, detail="Account not found.")
    
    acc = SavingsAccount.obj_form(account_data)
    
    try:
        acc.deposit(req.amount)
        savings_manager.save_data()
        return {
            "message": "Amount deposited successfully."
        }
    except PositiveNumber:
        raise HTTPException(status_code=400, detail="Amount must be positive.")

@router.delete('/savings/{acc_id}')
def delete_savings_account(acc_id: int):
    done = savings_manager.delete(acc_id, key="id")
    if not done:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    savings_manager.save_data()
    
    return {
        "message": "Account deleted successfully."
    }

# URLS FOR CHECKING ACCOUNTS

@router.post('/checking')
def create_checking_account(checking: Checkingmodel):
    try:
        account = CheckingAccount(
            checking.owner,
            checking.main_id,
            checking.overdraft_limit,
            checking.fee,
            checking.balance
        )
        checking_manager.add(account)

        return{
            "messgae": "Account created successfully.",
            "main_id": checking.main_id
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/checking/{acc_id}/deposit')    
def deposit_checking(acc_id: int, req: CheckingTransactions):
    account_info = checking_manager.find(acc_id)

    if not account_info:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account = CheckingAccount.obj_form(account_info)

    try:
        account.deposit(req.amount)
        checking_manager.save_data()

        return{
            "message": "Amount deposited successfully."
        }
    except PositiveNumber:
        raise HTTPException(status_code=400, detail="Cannot deposit a negative amount.")
    
@router.post('/checking/{acc_id}/withdraw')
def withdraw_checking(acc_id: int, req: CheckingTransactions):
    account_info = checking_manager.find(acc_id)

    if not account_info:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account = CheckingAccount.obj_form(account_info)

    try:
        account.withdraw(req.amount)
        checking_manager.save_data()
        return {
            "message": "Amount withdrawal done successfully."
        }
    except OverdraftLimit:
        raise HTTPException(status_code=400, detail="Daily limit exceeded.")
    except PositiveNumber:
        raise HTTPException(status_code=400, detail="Cannot withdraw negative amounts.")
    
@router.get('/checking/{acc_id}')
def get_checking(acc_id: int):
    account_info = checking_manager.find(acc_id)
    if not account_info:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account = CheckingAccount.obj_form(account_info)
    return account

@router.delete('/checking/{acc_id}')
def delete_checking_account(acc_id: int):
    done = checking_manager.delete(acc_id)

    if not done:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    checking_manager.save_data()
    return {"message": "Account deleted successfully."}

# URLS FOR BUSINESS ACCOUNTS

@router.post('/business')
def create_business_account(business: Businessmodel):
    try:
        account = BusinessAccount(
           business.owner,
           business.main_id,
           business.business_name, 
           business.authorized_users
        )

        business_manager.add(account)

        return{
            "message": "Account creted successfully.",
            "main_id": business.main_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/business/{main_id}/authorize')
def authorize_user(main_id: int, req: UserAuthorization):
    account_info = business_manager.find(main_id)

    if not account_info:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account = BusinessAccount.obj_form(account_info)

    account.authorize_user(req.acc_id)
    business_manager.save_data()

    return {"message": "User authorized successfully."}

@router.post('/business/{main_id}/deposit')
def deposit_business(main_id: int, req: BusinessTransactions):
    account_info = business_manager.find(main_id)

    if not account_info:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account = BusinessAccount.obj_form(account_info) 
    if req.user_id not in account.authorized_users:
        raise HTTPException(status_code=403, detail="User not authorized.")
    
    try:
        account.deposit(req.amount)
        business_manager.save_data()
        return {"message": "Amount deposited successfully."}
    
    except PositiveNumber:
        raise HTTPException(status_code=400, detail="Cannot deposit a negative amount.")
    
@router.post('/business/{main_id}/withdraw')
def withdraw_business(main_id: int, req: BusinessTransactions):
    account_info = business_manager.find(main_id)

    if not account_info:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account = BusinessAccount.obj_form(account_info)

    if req.user_id not in account.authorized_users:
        raise HTTPException(status_code=403, detail="User not authorized.")

    try:
        account.withdraw(req.amount)
        business_manager.save_data()
        return {"message": "Withdrawal completed successfully."}
    
    except PositiveNumber:
        raise HTTPException(status_code=400, detail="Cannot withdraw a negative amount.")
    except InsufficientFunds:
        raise HTTPException(status_code=400, detail="Not enough funds to complete withdrawal.")
    
@router.post('/business/{main_id}/transfer')
def transfer(main_id: int, req: Transfers):
    account1_info = business_manager.find(main_id)
    account2_info = business_manager.find(req.other_id)

    if not account1_info or not account2_info:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account1 = BusinessAccount.obj_form(account1_info)

    if req.user_id not in account1.authorized_users:
        raise HTTPException(status_code=403, detail="User not authorized.")

    try:
        account1.transfers_out(req.other_id, req.amount)
        business_manager.save_data()
        return {"message": "Transfer completed successfully."}
    except PositiveNumber:
        raise HTTPException(status_code=400, detail="Cannot transfer a negative amount.")
    except InsufficientFunds:
        raise HTTPException(status_code=400, detail="Not enough funds for completing this transaction.")
    
@router.post('/business/{main_id}/loan')
def take_loan(main_id: int, req: Loan):
    account_info = business_manager.find(main_id)

    if not account_info:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account = BusinessAccount.obj_form(account_info)
    if req.user_id not in account.authorized_users:
        raise HTTPException(status_code=403, detail="User not authorized.")

    try:
        account.take_loan(req.amount, req.intr, req.years)
        account.loan_payment()
        business_manager.save_data()

        return {
            "message": "Loan takes successfully. Payment process has begun."
        }
    except InvalidLoan as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete('/business/{main_id}')
def delete_business_account(main_id: int, req: DelBusiness):
    account_info = business_manager.find(main_id)
    if not account_info:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    account = BusinessAccount.obj_form(account_info)

    if req.user_id not in account.authorized_users:
        raise HTTPException(status_code=403, detail="User not authorized.")

    business_manager.delete(main_id)

    business_manager.save_data()
    return {"message": "Account deleted successfully."}