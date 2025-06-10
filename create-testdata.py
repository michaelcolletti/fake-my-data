import random
from faker import Faker
from datetime import datetime
import pandas as pd

# Initialize Faker for realistic text data
fake = Faker()

# Generate synthetic data columns
data = {
    'id': [f"{random.randint(1, 10**6)}" for _ in
range(2000)],
    'name': [fake.name() for _ in range(2000)],
    'email': [fake.email() for _ in range(2000)],
    'age': [random.randint(18, 100) for _ in
range(2000)],
    # Signup date as YYYY-MM-DD
    'signup_date': [f"{date.strftime('%Y-%m-%d')}"
for date in (fake.date() for _ in range(2000))],
    # Numeric column with two decimal places
    'score': [round(random.uniform(0, 100), 2) for _
in range(2000)]
}

# Create a DataFrame and export to CSV
df = pd.DataFrame(data)
df.to_csv('large_test.csv', index=False)
