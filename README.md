# Banking System

A command-line banking system built in Python that simulates real-world banking operations. Supports multiple account types, customer management, transaction handling, and persistent data storage. Built with a focus on object-oriented design, inheritance, and custom exception handling.

## Features

**Account Types**
- Savings accounts with interest calculation
- Checking accounts with overdraft support
- Business accounts with authorized users and inter-account transfers

**Customer Management**
- Create, view, and manage personal customer profiles
- Link multiple account types to a single customer

**Transactions**
- Deposits, withdrawals, and balance checks
- Business account loan management
- Transfers between business accounts

**System**
- Persistent storage using JSON files
- Input validation throughout
- Custom exception classes for domain-specific errors
- Fully tested with pytest (4 test files covering all account types)

## Project Structure
├── bank.py          # Core banking logic and account classes
├── main.py          # Entry point and CLI interface
├── exceptions.py    # Custom exception definitions
├── api/             # API layer
├── test_customer.py
├── test_savings.py
├── test_checking.py
└── test_business.py

## Concepts Demonstrated

- Object-oriented programming with inheritance and polymorphism
- Custom exception design
- File I/O with JSON
- Unit testing with pytest
- CLI application design

## How to Run

```bash
python main.py
```

No external dependencies required — Python 3.10+ only.
