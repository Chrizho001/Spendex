from models.user import User
from models.wallet import Wallet
from database import Database
import getpass
import sys
from utils import get_valid_float, get_non_empty_input
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print

console = Console()


class FinanceApp:
    def __init__(self):
        self.db = Database()  # ensures tables are initialized
        self.current_user = None
        self.wallet = None

    # -----------------------------
    # Utility Functions
    # -----------------------------
    def clear_screen(self):
        print("\n" * 5)

    def pause(self):
        input("\nPress Enter to continue...")

    # -----------------------------
    # Authentication Menu
    # -----------------------------
    def auth_menu(self):
        while True:
            console.clear()

            console.print(
                Panel.fit(
                    "[bold cyan]Finance Tracker[/bold cyan]\n[dim]Multi-user CLI System[/dim]",
                    border_style="green"
                )
            )

            choice = questionary.select(
                "Choose an option:",
                choices=[
                    "Register",
                    "Login",
                    "Exit"
                ]
            ).ask()

            if choice == "Register":
                self.register()
            elif choice == "Login":
                self.login()
            elif choice == "Exit":
                console.print("[bold red]Goodbye 👋[/bold red]")
                exit()

    def register(self):
        console.clear()
        console.print(Panel("[bold green]Create Account[/bold green]"))

        username = questionary.text("Username:").ask()
        password = questionary.password("Password:").ask()

        user = User(username=username)

        if user.save(password):
            console.print("[bold green]✔ User registered successfully![/bold green]")
        else:
            console.print("[bold red]✖ Username already exists.[/bold red]")

        questionary.press_any_key_to_continue().ask()

    def login(self):
        console.clear()
        console.print(Panel("[bold cyan]Login[/bold cyan]"))

        username = questionary.text("Username:").ask()
        password = questionary.password("Password:").ask()

        user = User.authenticate(username, password)

        if user:
            self.current_user = user
            self.wallet = Wallet(user)
            console.print("[bold green]✔ Login successful![/bold green]")
            questionary.press_any_key_to_continue().ask()
            self.main_menu()
        else:
            console.print("[bold red]✖ Invalid credentials.[/bold red]")
            questionary.press_any_key_to_continue().ask()
    # -----------------------------
    # Main Application Menu
    # -----------------------------
    def main_menu(self):
        while self.current_user:
            console.clear()

            console.print(
                Panel.fit(
                    f"[bold yellow]Welcome, {self.current_user.username}[/bold yellow]",
                    border_style="blue"
                )
            )

            choice = questionary.select(
                "Select an action:",
                choices=[
                    "Add Income",
                    "Add Expense",
                    "View Balance",
                    "View Transactions",
                    "Logout"
                ]
            ).ask()

            if choice == "Add Income":
                self.add_income()
            elif choice == "Add Expense":
                self.add_expense()
            elif choice == "View Balance":
                self.view_balance()
            elif choice == "View Transactions":
                self.view_transactions()
            elif choice == "Logout":
                self.logout()

    # -----------------------------
    # Actions
    # -----------------------------
    def add_income(self):
        console.clear()

        amount = get_valid_float("Amount:")
        if amount is None:
            return

        category = get_non_empty_input("Category:")
        if category is None:
            return

        description = questionary.text("Description (optional):").ask()

        self.wallet.add_income(amount, category, description)

        console.print("[bold green]✔ Income added successfully![/bold green]")
        questionary.press_any_key_to_continue().ask()

    def add_expense(self):
        console.clear()

        amount = get_valid_float("Amount:")
        if amount is None:
            return

        category = get_non_empty_input("Category:")
        if category is None:
            return

        description = questionary.text("Description (optional):").ask()

        self.wallet.add_expense(amount, category, description)
        console.print("[bold green]✔ Expense added successfully![/bold green]")
        questionary.press_any_key_to_continue().ask()

    def view_balance(self):
        console.clear()

        summary = self.wallet.get_summary()

        table = Table(title="Account Summary")

        table.add_column("Metric", style="cyan")
        table.add_column("Amount", style="green")

        table.add_row("Total Income", str(summary["total_income"]))
        table.add_row("Total Expense", str(summary["total_expense"]))
        table.add_row("Balance", str(summary["balance"]))

        console.print(table)

        questionary.press_any_key_to_continue().ask()

    def view_transactions(self):
        console.clear()

        transactions = self.wallet.get_transactions()

        if not transactions:
            console.print("[bold red]No transactions found.[/bold red]")
        else:
            table = Table(title="Transactions")

            table.add_column("Date", style="dim")
            table.add_column("Type")
            table.add_column("Category")
            table.add_column("Amount", style="green")
            table.add_column("Description")

            for t in transactions:
                table.add_row(
                    t.created_at,
                    t.type.upper(),
                    t.category,
                    str(t.amount),
                    t.description or ""
                )

            console.print(table)

        questionary.press_any_key_to_continue().ask()

    def logout(self):
        self.current_user = None
        self.wallet = None
        print("Logged out.")
        self.pause()


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    app = FinanceApp()
    app.auth_menu()
