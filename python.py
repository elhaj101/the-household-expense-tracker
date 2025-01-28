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
