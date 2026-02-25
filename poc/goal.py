import uuid
import requests


USER_ID = "876822d6-091c-5188-80b7-f781dc93ae22"
BASE_URL = "http://localhost:8000/api/v1"


_NAMESPACE = uuid.UUID('12345678-1234-5678-1234-567812345678')

def generate_goal_id(goal_name: str, user_id: str) -> str:
    sanitized = goal_name.replace(" ", "").lower()
    mapping = f"{user_id}_{sanitized}"
    return str(uuid.uuid5(_NAMESPACE, mapping))


GOALS = [
    {"goal_name": "Emergency Fund",          "goal_description": "6 months of living expenses as a safety net",                "goal_target_amount": 15000.00},
    {"goal_name": "Vacation to Japan",        "goal_description": "Two-week trip to Tokyo and Kyoto in summer 2027",           "goal_target_amount": 5000.00},
    {"goal_name": "New Laptop",               "goal_description": "High-end laptop for work and creative projects",             "goal_target_amount": 2500.00},
    {"goal_name": "Wedding Fund",             "goal_description": "Saving up for a dream wedding ceremony and reception",       "goal_target_amount": 20000.00},
    {"goal_name": "Down Payment on House",    "goal_description": "20% down payment for a home purchase",                      "goal_target_amount": 50000.00},
    {"goal_name": "Car Replacement",          "goal_description": "Replace the old car with a reliable used vehicle",           "goal_target_amount": 12000.00},
    {"goal_name": "Master's Degree Fund",     "goal_description": "Save for tuition and living costs during grad school",       "goal_target_amount": 30000.00},
    {"goal_name": "Home Renovation",          "goal_description": "Kitchen and bathroom remodel for the current apartment",    "goal_target_amount": 8000.00},
    {"goal_name": "Investment Starter",       "goal_description": "Initial capital to open a brokerage investment account",    "goal_target_amount": 3000.00},
    {"goal_name": "Gaming PC Build",          "goal_description": "Custom high-performance gaming desktop build",               "goal_target_amount": 1800.00},
    {"goal_name": "Retirement Boost",         "goal_description": "Extra contributions on top of employer retirement plan",    "goal_target_amount": 25000.00},
    {"goal_name": "Charity Donation Goal",    "goal_description": "Annual donation to selected charities and NGOs",             "goal_target_amount": 1000.00},
    {"goal_name": "Side Business Fund",       "goal_description": "Capital to launch a small online business",                 "goal_target_amount": 4000.00},
    {"goal_name": "Health & Fitness",         "goal_description": "Gym membership, equipment, and wellness coaching",           "goal_target_amount": 1200.00},
    {"goal_name": "Books & Learning",         "goal_description": "Budget for online courses, books, and workshops this year",  "goal_target_amount": 600.00},
    {"goal_name": "New Smartphone",           "goal_description": "Upgrade to the latest flagship phone",                      "goal_target_amount": 1100.00},
    {"goal_name": "Pet Expenses Reserve",     "goal_description": "Vet bills and care fund for my dog",                         "goal_target_amount": 2000.00},
    {"goal_name": "Holiday Gifts Budget",     "goal_description": "Christmas and Eid gifts for family and friends",             "goal_target_amount": 800.00},
    {"goal_name": "Travel Backpack Trip",     "goal_description": "Southeast Asia backpacking trip on a budget",                "goal_target_amount": 2200.00},
    {"goal_name": "Camera & Photography",     "goal_description": "DSLR camera body, lenses, and accessories",                 "goal_target_amount": 3500.00},
]


def seed_goals():
    print(f"Seeding {len(GOALS)} goals for user: {USER_ID}\n")
    success, failed = 0, 0

    for goal in GOALS:
        goal_id = generate_goal_id(goal["goal_name"], USER_ID)
        payload = {
            "goal_name": goal["goal_name"],
            "goal_description": goal["goal_description"],
            "goal_target_amount": goal["goal_target_amount"],
        }
        url = f"{BASE_URL}/goals/{USER_ID}"
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"  ✅  [{goal_id}]  {goal['goal_name']}  →  {response.json()}")
                success += 1
            else:
                print(f"  ❌  [{goal_id}]  {goal['goal_name']}  →  {response.status_code}: {response.text}")
                failed += 1
        except Exception as e:
            print(f"  💥  {goal['goal_name']}  →  {e}")
            failed += 1

    print(f"\nDone — {success} succeeded, {failed} failed.")


if __name__ == "__main__":
    seed_goals()
