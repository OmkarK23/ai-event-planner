import pandas as pd


def generate_recommendations(data_path="../data/event_data.csv"):

    df = pd.read_csv(data_path)

    best_event_type = df.groupby(
        "event_type"
    )["actual_attendance"].mean().idxmax()

    best_promotion = df.groupby(
        "promotion_channel"
    )["actual_attendance"].mean().idxmax()

    best_day = df.groupby(
        "day_of_week"
    )["actual_attendance"].mean().idxmax()

    best_time = df.groupby(
        "start_time"
    )["actual_attendance"].mean().idxmax()

    best_location = df.groupby(
        "location"
    )["actual_attendance"].mean().idxmax()

    avg_attendance = int(df["actual_attendance"].mean())

    recommendation = f"""
### AI Event Optimization Recommendations

**Best Event Type:** {best_event_type}

**Best Promotion Channel:** {best_promotion}

**Best Day:** {best_day}

**Best Start Time:** {best_time}

**Best Location:** {best_location}

**Average Historical Attendance:** {avg_attendance} attendees

### Recommended Strategy

To maximize event turnout, plan a **{best_event_type}** event on **{best_day}** at **{best_time}** in **{best_location}** and promote it through **{best_promotion}**.

### Practical Advice

- Start promotion at least 10–14 days before the event.
- Use reminder messages 3 days before and 1 day before the event.
- Track RSVPs early to estimate turnout risk.
- Use feedback scores from past events to improve engagement quality.
- Compare predicted attendance against actual attendance after every event.
"""

    return recommendation


if __name__ == "__main__":
    print(generate_recommendations())
