import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

event_types = [
    "Workshop",
    "Networking",
    "Research Talk",
    "Career Fair",
    "Social Event",
    "Hackathon",
    "Seminar"
]

locations = [
    "University Center",
    "Engineering Hall",
    "Library",
    "Online",
    "Student Center"
]

promotion_channels = [
    "Email",
    "Instagram",
    "Flyers",
    "LinkedIn",
    "Multiple"
]

feedback_samples = [
    "Amazing event and very informative",
    "Good organization and networking",
    "Average event could improve timing",
    "Loved the speakers and content",
    "Too crowded and poorly managed",
    "Interesting but promotion was weak",
    "Very engaging and useful session"
]

rows = []

for i in range(1000):

    event_type = random.choice(event_types)
    location = random.choice(locations)
    promotion = random.choice(promotion_channels)

    expected_audience = random.randint(50, 500)
    budget = random.randint(500, 10000)

    actual_attendance = int(
        expected_audience * random.uniform(0.5, 1.3)
    )

    feedback_score = round(
        random.uniform(2.5, 5.0), 1
    )

    rows.append({
        "event_name": fake.catch_phrase(),
        "event_type": event_type,
        "day_of_week": random.choice([
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ]),
        "start_time": random.choice([
            "10AM",
            "12PM",
            "2PM",
            "4PM",
            "6PM"
        ]),
        "location": location,
        "promotion_channel": promotion,
        "expected_audience": expected_audience,
        "actual_attendance": actual_attendance,
        "budget": budget,
        "feedback_score": feedback_score,
        "feedback_text": random.choice(
            feedback_samples
        )
    })

df = pd.DataFrame(rows)

df.to_csv(
    "../data/event_data.csv",
    index=False
)

print("Dataset created successfully!")
print(df.head())
