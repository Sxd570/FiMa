import uuid
import requests
from datetime import datetime

USER_ID = "876822d6-091c-5188-80b7-f781dc93ae22"
BASE_URL = "http://localhost:8000/api/v1"

BUDGET_IDS: dict = {}

_NAMESPACE = uuid.UUID('12345678-1234-5678-1234-567812345678')

def generate_budget_id(user_id: str, budget_name: str, allocated_month: str) -> str:
    mapping = f"{user_id}_{budget_name}_{allocated_month}"
    return str(uuid.uuid5(_NAMESPACE, mapping))

def generate_transaction_id(
    user_id: str,
    budget_id: str,
    transaction_type: str,
    transaction_date: str,
    amount: float
) -> str:
    current_time = datetime.now().isoformat()
    mapping = f"{user_id}_{budget_id}_{transaction_type}_{transaction_date}_{amount}_{current_time}"
    return str(uuid.uuid5(_NAMESPACE, mapping))


def resolve_budget_id(budget_name: str, month: str) -> str:
    key = f"{budget_name}_{month}"
    if key in BUDGET_IDS:
        return BUDGET_IDS[key]
    # fall back to deterministic generation
    return generate_budget_id(USER_ID, budget_name, month)



TRANSACTIONS = [
    # ── February 2026 – expenses ──
    {"budget_key": ("Groceries",     "2026-02"), "transaction_type": "expense", "transaction_info": "Supermarket weekly run",           "transaction_amount": 87.50,   "transaction_date": "2026-02-03"},
    {"budget_key": ("Groceries",     "2026-02"), "transaction_type": "expense", "transaction_info": "Farmers market vegetables",         "transaction_amount": 32.00,   "transaction_date": "2026-02-10"},
    {"budget_key": ("Groceries",     "2026-02"), "transaction_type": "expense", "transaction_info": "Online grocery order",               "transaction_amount": 115.75,  "transaction_date": "2026-02-17"},
    {"budget_key": ("Rent",          "2026-02"), "transaction_type": "expense", "transaction_info": "February rent payment",              "transaction_amount": 1200.00, "transaction_date": "2026-02-01"},
    {"budget_key": ("Utilities",     "2026-02"), "transaction_type": "expense", "transaction_info": "Electricity bill",                   "transaction_amount": 65.00,   "transaction_date": "2026-02-05"},
    {"budget_key": ("Utilities",     "2026-02"), "transaction_type": "expense", "transaction_info": "Internet bill",                      "transaction_amount": 45.00,   "transaction_date": "2026-02-05"},
    {"budget_key": ("Transport",     "2026-02"), "transaction_type": "expense", "transaction_info": "Monthly metro pass",                 "transaction_amount": 75.00,   "transaction_date": "2026-02-01"},
    {"budget_key": ("Transport",     "2026-02"), "transaction_type": "expense", "transaction_info": "Fuel refill",                         "transaction_amount": 55.20,   "transaction_date": "2026-02-12"},
    {"budget_key": ("Entertainment", "2026-02"), "transaction_type": "expense", "transaction_info": "Cinema tickets",                     "transaction_amount": 28.00,   "transaction_date": "2026-02-08"},
    {"budget_key": ("Entertainment", "2026-02"), "transaction_type": "expense", "transaction_info": "Video game purchase",                 "transaction_amount": 59.99,   "transaction_date": "2026-02-14"},
    {"budget_key": ("Dining Out",    "2026-02"), "transaction_type": "expense", "transaction_info": "Valentine's dinner",                  "transaction_amount": 95.00,   "transaction_date": "2026-02-14"},
    {"budget_key": ("Dining Out",    "2026-02"), "transaction_type": "expense", "transaction_info": "Lunch with colleagues",               "transaction_amount": 22.50,   "transaction_date": "2026-02-19"},
    {"budget_key": ("Healthcare",    "2026-02"), "transaction_type": "expense", "transaction_info": "Pharmacy – cold medicine",            "transaction_amount": 18.75,   "transaction_date": "2026-02-07"},
    {"budget_key": ("Subscriptions", "2026-02"), "transaction_type": "expense", "transaction_info": "Netflix subscription",                "transaction_amount": 15.99,   "transaction_date": "2026-02-02"},
    {"budget_key": ("Subscriptions", "2026-02"), "transaction_type": "expense", "transaction_info": "Spotify Premium",                    "transaction_amount": 9.99,    "transaction_date": "2026-02-02"},
    {"budget_key": ("Education",     "2026-02"), "transaction_type": "expense", "transaction_info": "Udemy course – Python advanced",     "transaction_amount": 19.99,   "transaction_date": "2026-02-11"},
    {"budget_key": ("Clothing",      "2026-02"), "transaction_type": "expense", "transaction_info": "Winter jacket sale",                  "transaction_amount": 89.00,   "transaction_date": "2026-02-20"},
    # ── February 2026 – income ──
    {"budget_key": None,                         "transaction_type": "income",  "transaction_info": "Monthly salary",                     "transaction_amount": 3500.00, "transaction_date": "2026-02-01"},
    {"budget_key": None,                         "transaction_type": "income",  "transaction_info": "Freelance project payment",           "transaction_amount": 450.00,  "transaction_date": "2026-02-18"},
    # ── March 2026 – expenses ──
    {"budget_key": ("Groceries",     "2026-03"), "transaction_type": "expense", "transaction_info": "Supermarket weekly run",           "transaction_amount": 92.00,   "transaction_date": "2026-03-03"},
    {"budget_key": ("Groceries",     "2026-03"), "transaction_type": "expense", "transaction_info": "Organic store haul",                  "transaction_amount": 45.50,   "transaction_date": "2026-03-10"},
    {"budget_key": ("Rent",          "2026-03"), "transaction_type": "expense", "transaction_info": "March rent payment",                 "transaction_amount": 1200.00, "transaction_date": "2026-03-01"},
    {"budget_key": ("Utilities",     "2026-03"), "transaction_type": "expense", "transaction_info": "Electricity bill",                   "transaction_amount": 58.00,   "transaction_date": "2026-03-05"},
    {"budget_key": ("Transport",     "2026-03"), "transaction_type": "expense", "transaction_info": "Fuel refill",                         "transaction_amount": 60.00,   "transaction_date": "2026-03-08"},
    {"budget_key": ("Transport",     "2026-03"), "transaction_type": "expense", "transaction_info": "Taxi to airport",                    "transaction_amount": 35.00,   "transaction_date": "2026-03-22"},
    {"budget_key": ("Entertainment", "2026-03"), "transaction_type": "expense", "transaction_info": "Concert tickets",                    "transaction_amount": 75.00,   "transaction_date": "2026-03-15"},
    {"budget_key": ("Dining Out",    "2026-03"), "transaction_type": "expense", "transaction_info": "Birthday dinner",                    "transaction_amount": 130.00,  "transaction_date": "2026-03-20"},
    {"budget_key": ("Dining Out",    "2026-03"), "transaction_type": "expense", "transaction_info": "Weekend brunch",                     "transaction_amount": 38.00,   "transaction_date": "2026-03-07"},
    {"budget_key": ("Healthcare",    "2026-03"), "transaction_type": "expense", "transaction_info": "Annual checkup copay",               "transaction_amount": 30.00,   "transaction_date": "2026-03-12"},
    {"budget_key": ("Subscriptions", "2026-03"), "transaction_type": "expense", "transaction_info": "Netflix subscription",                "transaction_amount": 15.99,   "transaction_date": "2026-03-02"},
    {"budget_key": ("Personal Care", "2026-03"), "transaction_type": "expense", "transaction_info": "Haircut",                             "transaction_amount": 25.00,   "transaction_date": "2026-03-14"},
    {"budget_key": ("Personal Care", "2026-03"), "transaction_type": "expense", "transaction_info": "Skincare products",                  "transaction_amount": 40.00,   "transaction_date": "2026-03-18"},
    # ── March 2026 – income ──
    {"budget_key": None,                         "transaction_type": "income",  "transaction_info": "Monthly salary",                     "transaction_amount": 3500.00, "transaction_date": "2026-03-01"},
    {"budget_key": None,                         "transaction_type": "income",  "transaction_info": "Stock dividend payout",              "transaction_amount": 120.00,  "transaction_date": "2026-03-25"},
    # ── April 2026 – expenses ──
    {"budget_key": ("Groceries",     "2026-04"), "transaction_type": "expense", "transaction_info": "Supermarket weekly run",           "transaction_amount": 98.00,   "transaction_date": "2026-04-02"},
    {"budget_key": ("Rent",          "2026-04"), "transaction_type": "expense", "transaction_info": "April rent payment",                 "transaction_amount": 1200.00, "transaction_date": "2026-04-01"},
    {"budget_key": ("Utilities",     "2026-04"), "transaction_type": "expense", "transaction_info": "Electricity bill",                   "transaction_amount": 52.00,   "transaction_date": "2026-04-05"},
    {"budget_key": ("Transport",     "2026-04"), "transaction_type": "expense", "transaction_info": "Monthly metro pass",                 "transaction_amount": 75.00,   "transaction_date": "2026-04-01"},
    {"budget_key": ("Entertainment", "2026-04"), "transaction_type": "expense", "transaction_info": "Theme park visit",                   "transaction_amount": 110.00,  "transaction_date": "2026-04-12"},
    {"budget_key": ("Dining Out",    "2026-04"), "transaction_type": "expense", "transaction_info": "Rooftop restaurant dinner",          "transaction_amount": 85.00,   "transaction_date": "2026-04-18"},
    {"budget_key": ("Savings",       "2026-04"), "transaction_type": "expense", "transaction_info": "Transfer to savings account",       "transaction_amount": 400.00,  "transaction_date": "2026-04-01"},
    {"budget_key": ("Gym & Fitness", "2026-04"), "transaction_type": "expense", "transaction_info": "Gym monthly membership",             "transaction_amount": 55.00,   "transaction_date": "2026-04-01"},
    {"budget_key": ("Subscriptions", "2026-04"), "transaction_type": "expense", "transaction_info": "YouTube Premium",                   "transaction_amount": 13.99,   "transaction_date": "2026-04-02"},
    {"budget_key": ("Miscellaneous", "2026-04"), "transaction_type": "expense", "transaction_info": "Stationery and office supplies",    "transaction_amount": 24.50,   "transaction_date": "2026-04-09"},
    # ── April 2026 – income ──
    {"budget_key": None,                         "transaction_type": "income",  "transaction_info": "Monthly salary",                     "transaction_amount": 3500.00, "transaction_date": "2026-04-01"},
    {"budget_key": None,                         "transaction_type": "income",  "transaction_info": "Cashback reward payout",             "transaction_amount": 35.00,   "transaction_date": "2026-04-20"},
]



def seed_transactions():
    print(f"Seeding {len(TRANSACTIONS)} transactions for user: {USER_ID}\n")
    success, failed = 0, 0

    for txn in TRANSACTIONS:
        if txn["budget_key"] is not None:
            budget_name, month = txn["budget_key"]
            budget_id = resolve_budget_id(budget_name, month)
        else:
            budget_id = None

        payload = {
            "budget_id": budget_id,
            "transaction_type": txn["transaction_type"],
            "transaction_info": txn["transaction_info"],
            "transaction_amount": txn["transaction_amount"],
            "transaction_date": txn["transaction_date"],
        }
        url = f"{BASE_URL}/transactions/{USER_ID}"
        label = f"{txn['transaction_info']} ({txn['transaction_date']})"
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"  ✅  {label}  →  {response.json()}")
                success += 1
            else:
                print(f"  ❌  {label}  →  {response.status_code}: {response.text}")
                failed += 1
        except Exception as e:
            print(f"  💥  {label}  →  {e}")
            failed += 1

    print(f"\nDone — {success} succeeded, {failed} failed.")


if __name__ == "__main__":
    seed_transactions()
