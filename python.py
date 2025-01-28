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