# Finance Tracker CLI App

A terminal-based, multi-user personal finance tracking application built in Python.  
Track your incomes, expenses, and see balance summaries in a polished, interactive CLI interface.

---

## Features

- Multi-user support with secure password authentication
- Add, update, view, and delete transactions (full CRUD)
- Categorized incomes and expenses
- Monthly financial summaries
- Interactive terminal interface using [Questionary](https://github.com/tmbo/questionary) and [Rich](https://github.com/willmcgugan/rich)
- Input validation and error handling
- SQLite database for easy setup

---

## Installation

1. Clone the repository
2. Create a virtual environment and initialize it:
  python3 -m venv env
  source env/bin/activate   # Linux / Mac
  env\Scripts\activate      # Windows
3. Install dependencies:
  pip install -r requirements.txt
4.  Run the app:
     python main.py




Usage

Register a new user or login

Navigate the main menu using arrow keys

Add income or expense with category and optional description

View balance and transactions in styled tables

Update or delete transactions as needed

Logout when finished



#Tech Stack

Python 3

SQLite

Questionary (interactive CLI)

Rich (terminal styling)

OOP-based architecture


#Project Structure
Spendex/
│
├── main.py
├── database.py
├── requirements.txt
├── finance.db   # auto-created
└── models/
    ├── __init__.py
    ├── user.py
    ├── wallet.py
    └── transaction.py

