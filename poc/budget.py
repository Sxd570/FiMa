import uuid
import requests


USER_ID = "876822d6-091c-5188-80b7-f781dc93ae22"
BASE_URL = "http://localhost:8000/api/v1"


_NAMESPACE = uuid.UUID('12345678-1234-5678-1234-567812345678')

def generate_budget_id(user_id: str, budget_name: str, allocated_month: str) -> str:
    mapping = f"{user_id}_{budget_name}_{allocated_month}"
    return str(uuid.uuid5(_NAMESPACE, mapping))


BUDGETS = [
    # ── February 2026 ──
    {"budget_name": "Groceries",          "budget_month": "2026-02", "budget_limit": 500.00,  "description": "Weekly grocery shopping"},
    {"budget_name": "Rent",               "budget_month": "2026-02", "budget_limit": 1200.00, "description": "Monthly apartment rent"},
    {"budget_name": "Utilities",          "budget_month": "2026-02", "budget_limit": 150.00,  "description": "Electricity, water, internet"},
    {"budget_name": "Transport",          "budget_month": "2026-02", "budget_limit": 200.00,  "description": "Fuel and public transport"},
    {"budget_name": "Entertainment",      "budget_month": "2026-02", "budget_limit": 180.00,  "description": "Movies, concerts, games"},
    {"budget_name": "Dining Out",         "budget_month": "2026-02", "budget_limit": 250.00,  "description": "Restaurants and takeaways"},
    {"budget_name": "Healthcare",         "budget_month": "2026-02", "budget_limit": 100.00,  "description": "Medicines, doctor visits"},
    {"budget_name": "Clothing",           "budget_month": "2026-02", "budget_limit": 150.00,  "description": "Apparel and accessories"},
    {"budget_name": "Subscriptions",      "budget_month": "2026-02", "budget_limit": 80.00,   "description": "Netflix, Spotify, etc."},
    {"budget_name": "Education",          "budget_month": "2026-02", "budget_limit": 120.00,  "description": "Online courses and books"},
    # ── March 2026 ──
    {"budget_name": "Groceries",          "budget_month": "2026-03", "budget_limit": 520.00,  "description": "Weekly grocery shopping"},
    {"budget_name": "Rent",               "budget_month": "2026-03", "budget_limit": 1200.00, "description": "Monthly apartment rent"},
    {"budget_name": "Utilities",          "budget_month": "2026-03", "budget_limit": 140.00,  "description": "Electricity, water, internet"},
    {"budget_name": "Transport",          "budget_month": "2026-03", "budget_limit": 210.00,  "description": "Fuel and public transport"},
    {"budget_name": "Entertainment",      "budget_month": "2026-03", "budget_limit": 200.00,  "description": "Movies, concerts, games"},
    {"budget_name": "Dining Out",         "budget_month": "2026-03", "budget_limit": 270.00,  "description": "Restaurants and takeaways"},
    {"budget_name": "Healthcare",         "budget_month": "2026-03", "budget_limit": 90.00,   "description": "Medicines, doctor visits"},
    {"budget_name": "Clothing",           "budget_month": "2026-03", "budget_limit": 160.00,  "description": "Apparel and accessories"},
    {"budget_name": "Subscriptions",      "budget_month": "2026-03", "budget_limit": 80.00,   "description": "Netflix, Spotify, etc."},
    {"budget_name": "Personal Care",      "budget_month": "2026-03", "budget_limit": 70.00,   "description": "Haircuts, cosmetics, grooming"},
    # ── April 2026 ──
    {"budget_name": "Groceries",          "budget_month": "2026-04", "budget_limit": 510.00,  "description": "Weekly grocery shopping"},
    {"budget_name": "Rent",               "budget_month": "2026-04", "budget_limit": 1200.00, "description": "Monthly apartment rent"},
    {"budget_name": "Utilities",          "budget_month": "2026-04", "budget_limit": 130.00,  "description": "Electricity, water, internet"},
    {"budget_name": "Transport",          "budget_month": "2026-04", "budget_limit": 195.00,  "description": "Fuel and public transport"},
    {"budget_name": "Entertainment",      "budget_month": "2026-04", "budget_limit": 220.00,  "description": "Movies, concerts, games"},
    {"budget_name": "Dining Out",         "budget_month": "2026-04", "budget_limit": 230.00,  "description": "Restaurants and takeaways"},
    {"budget_name": "Savings",            "budget_month": "2026-04", "budget_limit": 400.00,  "description": "Monthly savings contribution"},
    {"budget_name": "Gym & Fitness",      "budget_month": "2026-04", "budget_limit": 60.00,   "description": "Gym membership and classes"},
    {"budget_name": "Subscriptions",      "budget_month": "2026-04", "budget_limit": 80.00,   "description": "Netflix, Spotify, etc."},
    {"budget_name": "Miscellaneous",      "budget_month": "2026-04", "budget_limit": 100.00,  "description": "Unexpected small expenses"},
]


def seed_budgets():
    print(f"Seeding {len(BUDGETS)} budgets for user: {USER_ID}\n")
    success, failed = 0, 0

    for budget in BUDGETS:
        budget_id = generate_budget_id(USER_ID, budget["budget_name"], budget["budget_month"])
        payload = {
            "budget_name": budget["budget_name"],
            "budget_month": budget["budget_month"],
            "budget_limit": budget["budget_limit"],
            "description": budget["description"],
        }
        url = f"{BASE_URL}/budget/{USER_ID}/create"
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"  ✅  [{budget_id}]  {budget['budget_name']} ({budget['budget_month']})  →  {response.json()}")
                success += 1
            else:
                print(f"  ❌  [{budget_id}]  {budget['budget_name']} ({budget['budget_month']})  →  {response.status_code}: {response.text}")
                failed += 1
        except Exception as e:
            print(f"  💥  {budget['budget_name']}  →  {e}")
            failed += 1

    print(f"\nDone — {success} succeeded, {failed} failed.")


if __name__ == "__main__":
    seed_budgets()
