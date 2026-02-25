from models.transaction import Transaction
from utils import get_valid_float, get_non_empty_input


class Wallet:
    def __init__(self, user):
        self.user = user

    # -----------------------------
    # Add Income
    # -----------------------------
    def add_income(self, amount, category, description=None):
        transaction = Transaction(
            user_id=self.user.id,
            amount=amount,
            category=category,
            transaction_type="income",
            description=description,
        )
        return transaction.save()

    # -----------------------------
    # Add Expense
    # -----------------------------
    def add_expense(self, amount, category, description=None):
        transaction = Transaction(
            user_id=self.user.id,
            amount=amount,
            category=category,
            transaction_type="expense",
            description=description,
        )
        return transaction.save()

    # -----------------------------
    # Get All Transactions
    # -----------------------------
    def get_transactions(self):
        return Transaction.get_all_by_user(self.user.id)

    # -----------------------------
    # Get Transactions by Category
    # -----------------------------
    def get_transactions_by_category(self, category):
        return Transaction.get_by_category(self.user.id, category)

    # -----------------------------
    # Calculate Totals
    # -----------------------------
    def get_total_income(self):
        transactions = self.get_transactions()
        return sum(t.amount for t in transactions if t.type == "income")

    def get_total_expense(self):
        transactions = self.get_transactions()
        return sum(t.amount for t in transactions if t.type == "expense")

    @property
    def balance(self):
        return self.get_total_income() - self.get_total_expense()

    # -----------------------------
    # Monthly Summary (Optional Extension)
    # -----------------------------
    def get_summary(self):
        return {
            "total_income": self.get_total_income(),
            "total_expense": self.get_total_expense(),
            "balance": self.balance,
        }
    
    # -----------------------------
    # get monthly summary 
    # -----------------------------
    def get_monthly_summary(self, year, month):
        transactions = Transaction.get_by_month(self.user.id, year, month)

        income = sum(t.amount for t in transactions if t.type == "income")
        expense = sum(t.amount for t in transactions if t.type == "expense")

        return {
            "income": income,
            "expense": expense,
            "balance": income - expense
        }
