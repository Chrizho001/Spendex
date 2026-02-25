import questionary
from rich import print


def get_valid_float(prompt):
    while True:
        value = questionary.text(prompt).ask()

        if value is None:
            print("[red]Operation cancelled.[/red]")
            return None

        try:
            amount = float(value)

            if amount <= 0:
                print("[bold red]Amount must be greater than 0.[/bold red]")
                continue

            return amount

        except ValueError:
            print("[bold red]Invalid number. Please enter a valid amount.[/bold red]")


def get_non_empty_input(prompt):
    while True:
        value = questionary.text(prompt).ask()

        if value is None:
            print("[red]Operation cancelled.[/red]")
            return None

        value = value.strip()

        if not value:
            print("[bold red]This field cannot be empty.[/bold red]")
        else:
            return value
