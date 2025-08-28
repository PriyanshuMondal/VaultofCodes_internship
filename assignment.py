import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# File to store expenses
DATA_FILE = "expenses.json"

# ---------------------- FILE HANDLING ---------------------- #
def load_expenses():
    """Load expenses from JSON file"""
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # return empty list if file doesn’t exist

def save_expenses(expenses):
    """Save expenses to JSON file"""
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

# ---------------------- CORE FEATURES ---------------------- #
def add_expense(expenses):
    """Add a new expense"""
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category (Food, Transport, Entertainment, etc.): ")
        date = input("Enter date (YYYY-MM-DD) or leave empty for today: ")
        if not date:
            date = datetime.today().strftime("%Y-%m-%d")

        expense = {"amount": amount, "category": category, "date": date}
        expenses.append(expense)
        save_expenses(expenses)
        print("Expense added successfully!")
    except ValueError:
        print("Invalid input. Try again.")

def view_summary(expenses):
    """View total and category-wise summaries"""
    if not expenses:
        print("No expenses recorded yet.")
        return

    total = sum(exp["amount"] for exp in expenses)
    print(f"\nTotal Spending: {total:.2f}")

    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp["category"]] += exp["amount"]

    print("\nSpending by Category:")
    for category, amt in category_totals.items():
        print(f"  {category}: {amt:.2f}")

def view_spending_over_time(expenses):
    """View daily/monthly spending trends"""
    if not expenses:
        print("No expenses recorded yet.")
        return

    # Group by date
    date_totals = defaultdict(float)
    for exp in expenses:
        date_totals[exp["date"]] += exp["amount"]

    print("\nSpending Over Time:")
    for date, amt in sorted(date_totals.items()):
        print(f"  {date}: {amt:.2f}")

def edit_expense(expenses):
    """Edit an existing expense"""
    if not expenses:
        print("No expenses recorded yet.")
        return

    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. {exp['date']} - {exp['category']} - {exp['amount']}")

    try:
        choice = int(input("Enter the expense number to edit: "))
        if 1 <= choice <= len(expenses):
            exp = expenses[choice - 1]
            print("Leave input empty to keep old value.")

            new_amount = input(f"New amount (old {exp['amount']}): ")
            if new_amount:
                exp["amount"] = float(new_amount)

            new_category = input(f"New category (old {exp['category']}): ")
            if new_category:
                exp["category"] = new_category

            new_date = input(f"New date (old {exp['date']}): ")
            if new_date:
                exp["date"] = new_date

            save_expenses(expenses)
            print("Expense updated successfully!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

def delete_expense(expenses):
    """Delete an expense"""
    if not expenses:
        print("No expenses recorded yet.")
        return

    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. {exp['date']} - {exp['category']} - {exp['amount']}")

    try:
        choice = int(input("Enter the expense number to delete: "))
        if 1 <= choice <= len(expenses):
            removed = expenses.pop(choice - 1)
            save_expenses(expenses)
            print(f"Deleted: {removed['date']} - {removed['category']} - {removed['amount']}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

# ---------------------- BONUS: GRAPHS ---------------------- #
def show_graph(expenses):
    """Show category spending pie chart"""
    if not expenses:
        print("No expenses recorded yet.")
        return

    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp["category"]] += exp["amount"]

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Spending by Category")
    plt.show()

# ---------------------- MAIN MENU ---------------------- #
def main():
    expenses = load_expenses()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. View Spending Over Time")
        print("4. Edit Expense")
        print("5. Delete Expense")
        print("6. Show Graph")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            view_spending_over_time(expenses)
        elif choice == "4":
            edit_expense(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            show_graph(expenses)
        elif choice == "7":
            print("Goodbye! Your expenses are saved.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
