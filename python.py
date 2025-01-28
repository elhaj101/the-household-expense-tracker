import datetime
import colorama
from colorama import Fore, Style
import gspread
from google.oauth2.service_account import Credentials

# Initialize colorama for colored terminal output
colorama.init(autoreset=True)

# Google Sheets API setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("expense_tracker")

# Predefined spending categories
SPENDING_CATEGORIES = [
    "Housing",  # Rent or mortgage payments
    "Utilities",  # Electricity, gas, water, and trash services
    "Groceries",  # Food and household supplies
    "Transportation",  # Fuel, public transport, or vehicle maintenance
    "Insurance",  # Health, home, auto, or life insurance premiums
    "Healthcare",  # Out-of-pocket medical expenses, prescriptions, and dental care
    "Childcare/Education",  # Tuition, daycare, or extracurricular activities for children
    "Internet and Phone",  # Monthly bills for internet service and mobile phone plans
    "Entertainment",  # Subscriptions (like Netflix), dining out, and recreational activities
    "Personal Care"  # Toiletries, haircuts, and other cosmetics
]

# Global variables to store user data
user_data = {
    "name": "",
    "salary": 0,
    "spending": {}
}

def greet_user():
    """Greet the user based on the time of day."""
    current_time = datetime.datetime.now()
    hour = current_time.hour

    if 5 <= hour < 12:
        greeting = "morning"
    elif 12 <= hour < 18:
        greeting = "afternoon"
    else:
        greeting = "evening"

    print(f"\nHello, it's a good {greeting}!")
    print("Welcome to 'The Personal Household Expense Tracker'.\n")

def display_spending_categories():
    """Display the list of spending categories with descriptions and prompt the user to continue."""
    print("\nHere's your household spending categories. Take a look at them before providing data:")
    
    # List of categories with descriptions
    categories_with_descriptions = [
        ("Housing", "Rent or mortgage payments"),
        ("Utilities", "Electricity, gas, water, and trash services"),
        ("Groceries", "Food and household supplies"),
        ("Transportation", "Fuel, public transport, or vehicle maintenance"),
        ("Insurance", "Health, home, auto, or life insurance premiums"),
        ("Healthcare", "Out-of-pocket medical expenses, prescriptions, and dental care"),
        ("Childcare/Education", "Tuition, daycare, or extracurricular activities for children"),
        ("Internet and Phone", "Monthly bills for internet service and mobile phone plans"),
        ("Entertainment", "Subscriptions (like Netflix), dining out, and recreational activities"),
        ("Personal Care", "Toiletries, haircuts, and other cosmetics")
    ]

    # Display categories with descriptions
    for category, description in categories_with_descriptions:
        print(f"- {category}: {description}")

    # Prompt the user to continue
    while True:
        response = input("\nType 'Y' to continue: ").strip().upper()
        if response == "Y":
            break
        else:
            print(Fore.RED + "Invalid input! Please type 'Y' to continue.")

def collect_user_info():
    """Collect the user's name and monthly salary."""
    global user_data

    while True:
        name = input("Enter your name: ").strip()
        if name.replace(" ", "").isalpha():  # Check if the name contains only letters and spaces
            user_data["name"] = name
            break
        else:
            print(Fore.RED + "Invalid input! Name must contain only letters and spaces.")

    while True:
        try:
            salary = float(input("Enter your monthly salary (in USD): "))
            if salary >= 0:
                user_data["salary"] = salary
                break
            else:
                print(Fore.RED + "Invalid input! Salary must be a positive number.")
        except ValueError:
            print(Fore.RED + "Invalid input! Please enter a number.")

    print("\nGreat, your data will remain private.\n")

    # Display spending categories and prompt to continue
    display_spending_categories()

def collect_spending():
    """Collect spending amounts for predefined categories."""
    global user_data

    print("Please enter your monthly spending for each category (enter 0 if not applicable):\n")

    for category in SPENDING_CATEGORIES:
        while True:
            try:
                amount = float(input(f"{category}: "))
                if amount >= 0:
                    user_data["spending"][category] = amount
                    break
                else:
                    print(Fore.RED + "Invalid input! Amount must be a positive number or 0.")
            except ValueError:
                print(Fore.RED + "Invalid input! Please enter a number.")

    print("\nSpending data collected successfully.\n")

def display_menu():
    """Display the sticky menu with action options."""
    print(Fore.CYAN + "\n--- Menu ---")
    print("a. Calculate current monthly/annual savings")
    print("b. Analyze potential savings by category")
    print("c. Forecast 12-month spending/savings")
    print("d. Save data to database")
    print("e. Load data from database")
    print("f. Reset and restart system")
    print("g. Quit system")
    print(Fore.CYAN + "------------\n")

def calculate_current_savings():
    """Calculate and display current monthly and annual expenses and savings."""
    total_spending = sum(user_data["spending"].values())
    monthly_savings = user_data["salary"] - total_spending
    annual_savings = monthly_savings * 12
    annual_spending = total_spending * 12

    print(Fore.CYAN + "\n--- Current Savings ---")
    print(Fore.GREEN + f"Monthly Salary: ${user_data['salary']:.2f}")
    print(Fore.RED + f"Monthly Expenses: ${total_spending:.2f}")
    print(Fore.GREEN + f"Monthly Savings: ${monthly_savings:.2f}")
    print(Fore.CYAN + "-----------------------")
    print(Fore.GREEN + f"Annual Salary: ${user_data['salary'] * 12:.2f}")
    print(Fore.RED + f"Annual Expenses: ${annual_spending:.2f}")
    print(Fore.GREEN + f"Annual Savings: ${annual_savings:.2f}")
    print(Fore.CYAN + "-----------------------\n")

def analyze_potential_savings():
    """Analyze potential savings by reducing spending in selected categories."""
    print("\nSelect categories to reduce spending:")
    for i, category in enumerate(SPENDING_CATEGORIES, 1):
        print(f"{i}. {category}")

    selected_categories = input("\nEnter the numbers of categories (comma-separated): ").strip().split(",")
    potential_savings = 0

    for idx in selected_categories:
        try:
            idx = int(idx.strip()) - 1  # Convert to zero-based index
            if 0 <= idx < len(SPENDING_CATEGORIES):
                category = SPENDING_CATEGORIES[idx]
                current_spending = user_data["spending"][category]

                # Prompt for reduction percentage
                while True:
                    try:
                        reduction_percent = float(input(f"Enter the percentage reduction for {category} (e.g., 10 for 10%): "))
                        if 0 <= reduction_percent <= 100:
                            savings = current_spending * (reduction_percent / 100)
                            potential_savings += savings
                            print(Fore.GREEN + f"Potential savings for {category}: ${savings:.2f}")
                            break
                        else:
                            print(Fore.RED + "Invalid input! Percentage must be between 0 and 100.")
                    except ValueError:
                        print(Fore.RED + "Invalid input! Please enter a number.")
            else:
                print(Fore.RED + f"Invalid category number: {idx + 1}")
        except ValueError:
            print(Fore.RED + "Invalid input! Please enter valid category numbers.")

    print(Fore.GREEN + f"\nTotal potential savings: ${potential_savings:.2f}\n")

def forecast_savings():
    """
    Forecast the accumulation of savings and expenses over the next 12 months.
    Expenses are displayed in red, and savings are displayed in green.
    """
    total_spending = sum(user_data["spending"].values())
    monthly_savings = user_data["salary"] - total_spending
    annual_savings = monthly_savings * 12
    annual_spending = total_spending * 12

    print(Fore.CYAN + "\n--- 12-Month Forecast ---")
    print(Fore.GREEN + f"Monthly Salary: ${user_data['salary']:.2f}")
    print(Fore.RED + f"Monthly Expenses: ${total_spending:.2f}")
    print(Fore.GREEN + f"Monthly Savings: ${monthly_savings:.2f}")
    print(Fore.CYAN + "-------------------------")

    # Initialize cumulative totals
    cumulative_savings = 0
    cumulative_expenses = 0

    # Loop through each month and calculate cumulative totals
    for month in range(1, 13):
        cumulative_savings += monthly_savings
        cumulative_expenses += total_spending
        print(Fore.CYAN + f"Month {month}:")
        print(Fore.GREEN + f"  Cumulative Savings: ${cumulative_savings:.2f}")
        print(Fore.RED + f"  Cumulative Expenses: ${cumulative_expenses:.2f}")

    print(Fore.CYAN + "-------------------------")
    print(Fore.GREEN + f"Total Annual Savings: ${annual_savings:.2f}")
    print(Fore.RED + f"Total Annual Expenses: ${annual_spending:.2f}")
    print(Fore.CYAN + "-------------------------\n")

def save_data():
    """Save user data to the database."""
    try:
        sheet = SHEET.get_worksheet(0)
        row = [user_data["name"], user_data["salary"]] + list(user_data["spending"].values())
        sheet.append_row(row)
        print(Fore.GREEN + f"\nData saved to database: {sheet.title}\n")
    except Exception as e:
        print(Fore.RED + f"\nError saving data: {e}\n")

def load_data():
    """Load user data from the database based on the user's name."""
    global user_data

    name = input("Enter your name to load your data: ").strip()
    try:
        sheet = SHEET.get_worksheet(0)
        records = sheet.get_all_records()
        user_record = None
        for record in records:
            if record["Name"].strip().lower() == name.lower():
                user_record = record
                break
        if user_record:
            user_data["name"] = user_record["Name"]
            user_data["salary"] = float(user_record["Monthly Salary"])
            user_data["spending"] = {
                "Housing": float(user_record["Housing"]),
                "Utilities": float(user_record["Utilities"]),
                "Groceries": float(user_record["Groceries"]),
                "Transportation": float(user_record["Transportation"]),
                "Insurance": float(user_record["Insurance"]),
                "Healthcare": float(user_record["Healthcare"]),
                "Childcare/Education": float(user_record["Childcare/Education"]),
                "Internet and Phone": float(user_record["Internet and Phone"]),
                "Entertainment": float(user_record["Entertainment"]),
                "Personal Care": float(user_record["Personal Care"])
            }
            print(Fore.GREEN + "\nData loaded successfully!\n")
        else:
            print(Fore.RED + f"\nNo data found for user: {name}\n")
    except Exception as e:
        print(Fore.RED + f"\nError loading data: {e}\n")
