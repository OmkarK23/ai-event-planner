"""
Synthetic event dataset generator.

v2 change log (fixing the v1 bug):
- v1 generated `actual_attendance` as `expected_audience * random.uniform(0.5, 1.3)`,
  completely independent of event_type, day, time, location, promotion_channel, and
  budget. That meant those 6 features were pure noise relative to the target, so any
  model or "recommendation" built on them was fitting noise, not signal.
- v2 gives each feature a real (if simple, hand-picked) effect on turnout, so the
  attendance model and the recommendation engine have something legitimate to learn.
- v1 also generated feedback_score independently of attendance, then let the model
  use "expected feedback score" as an INPUT to predict attendance -- asking the
  organizer to predict feedback before the event happens. v2 generates feedback_score
  as a downstream consequence of how attendance actually went (turnout ratio), and it
  is no longer used as a predictor of attendance -- it's an outcome, not an input.

This is still a synthetic dataset with hand-picked effect sizes, not real event data.
Treat the resulting model as a demonstration of the ML pipeline, not a validated
real-world predictor -- see README for details.
"""

import random

import numpy as np
import pandas as pd

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

N_ROWS = 1000

# Small built-in name generator, replacing the Faker dependency (Faker was only
# ever used here for a cosmetic event_name string -- not worth an extra dependency).
_ADJECTIVES = [
    "Annual", "Regional", "Campus", "Global", "Open", "Emerging", "Advanced",
    "Collaborative", "Interactive", "Modern", "Applied", "Community",
]
_TOPICS = [
    "Data Science", "AI", "Robotics", "Career", "Design", "Entrepreneurship",
    "Cloud Computing", "Cybersecurity", "Product", "Research", "Networking",
    "Innovation",
]
_FORMATS = ["Summit", "Meetup", "Workshop", "Symposium", "Forum", "Showcase", "Night"]


def fake_event_name():
    return f"{random.choice(_ADJECTIVES)} {random.choice(_TOPICS)} {random.choice(_FORMATS)}"

EVENT_TYPES = [
    "Workshop", "Networking", "Research Talk", "Career Fair",
    "Social Event", "Hackathon", "Seminar",
]
LOCATIONS = ["University Center", "Engineering Hall", "Library", "Online", "Student Center"]
PROMO_CHANNELS = ["Email", "Instagram", "Flyers", "LinkedIn", "Multiple"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
TIMES = ["10AM", "12PM", "2PM", "4PM", "6PM"]

# Hand-picked multiplicative effects on turnout rate (actual / expected audience).
# These are illustrative, not derived from real data -- documented so the numbers
# aren't mysterious.
EVENT_TYPE_EFFECT = {
    "Career Fair": 1.05, "Hackathon": 1.00, "Workshop": 0.95,
    "Social Event": 0.90, "Networking": 0.85, "Seminar": 0.75,
    "Research Talk": 0.70,
}
DAY_EFFECT = {
    "Thursday": 1.05, "Wednesday": 0.95, "Friday": 0.90,
    "Tuesday": 0.85, "Monday": 0.80, "Saturday": 0.75,
}
TIME_EFFECT = {"6PM": 1.05, "4PM": 0.95, "12PM": 0.90, "2PM": 0.85, "10AM": 0.75}
LOCATION_EFFECT = {
    "Online": 1.10, "University Center": 1.00, "Student Center": 0.95,
    "Engineering Hall": 0.90, "Library": 0.80,
}
PROMO_EFFECT = {
    "Multiple": 1.15, "Instagram": 0.90, "Email": 0.85,
    "LinkedIn": 0.85, "Flyers": 0.70,
}

FEEDBACK_PHRASES = {
    "high": [
        "Amazing event and very informative",
        "Loved the speakers and content",
        "Very engaging and useful session",
    ],
    "mid": [
        "Good organization and networking",
        "Interesting but promotion was weak",
        "Average event could improve timing",
    ],
    "low": [
        "Too crowded and poorly managed",
        "Turnout was disappointing, hard to stay engaged",
        "Felt underprepared for the number of attendees",
    ],
}


def budget_effect(budget: float) -> float:
    """Diminishing-returns effect of budget on turnout, capped at +15%."""
    return min(1.15, 0.85 + 0.30 * (budget / 10000))


# The six multiplicative effects above average below 1.0 individually, so their
# product compounds well below 1.0. GLOBAL_SCALE renormalizes so a "typical" event
# (average-ish across all factors) lands near a 90-100% turnout rate, which is a
# more realistic center point than ~55%.
GLOBAL_SCALE = 1.75


def generate_row():
    event_type = random.choice(EVENT_TYPES)
    day = random.choice(DAYS)
    time = random.choice(TIMES)
    location = random.choice(LOCATIONS)
    promo = random.choice(PROMO_CHANNELS)

    expected_audience = random.randint(50, 500)
    budget = random.randint(500, 10000)

    turnout_rate = (
        EVENT_TYPE_EFFECT[event_type]
        * DAY_EFFECT[day]
        * TIME_EFFECT[time]
        * LOCATION_EFFECT[location]
        * PROMO_EFFECT[promo]
        * budget_effect(budget)
        * GLOBAL_SCALE
        * np.random.uniform(0.85, 1.15)  # residual noise -- real events are noisy
    )

    actual_attendance = max(1, int(round(expected_audience * turnout_rate)))

    # Feedback is a downstream OUTCOME of how the event actually went, not an
    # input to predicting attendance. Better-than-expected turnout skews feedback
    # up; being wildly over/under also carries a small penalty (overcrowding /
    # empty-room awkwardness).
    turnout_ratio = actual_attendance / expected_audience
    crowding_penalty = -0.5 * abs(turnout_ratio - 1.0)
    feedback_score = np.clip(
        3.0 + 1.0 * (min(turnout_ratio, 1.2) - 0.9) + crowding_penalty
        + np.random.normal(0, 0.4),
        1.0, 5.0,
    )
    feedback_score = round(float(feedback_score), 1)

    bucket = "high" if feedback_score >= 4.0 else "mid" if feedback_score >= 3.0 else "low"
    feedback_text = random.choice(FEEDBACK_PHRASES[bucket])

    return {
        "event_name": fake_event_name(),
        "event_type": event_type,
        "day_of_week": day,
        "start_time": time,
        "location": location,
        "promotion_channel": promo,
        "expected_audience": expected_audience,
        "actual_attendance": actual_attendance,
        "budget": budget,
        "feedback_score": feedback_score,
        "feedback_text": feedback_text,
    }


def main():
    rows = [generate_row() for _ in range(N_ROWS)]
    df = pd.DataFrame(rows)
    df.to_csv("../data/event_data.csv", index=False)
    print(f"Dataset created successfully! ({len(df)} rows, seed={RANDOM_SEED})")
    print(df.head())


if __name__ == "__main__":
    main()
