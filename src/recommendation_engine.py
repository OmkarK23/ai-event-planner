import pandas as pd


def _best_by_turnout_rate(df, column):
    """
    Rank categories by mean turnout rate (actual / expected audience) rather than
    raw actual_attendance. Raw attendance can be confounded by a category happening
    to have larger events on average; turnout rate isolates "does this category tend
    to outperform its own expectation," which is the thing organizers actually want
    to know when choosing between options.
    """
    rate = df["actual_attendance"] / df["expected_audience"]
    return df.assign(_turnout_rate=rate).groupby(column)["_turnout_rate"].mean().idxmax()


def generate_recommendations(data_path="../data/event_data.csv"):

    df = pd.read_csv(data_path)

    best_event_type = _best_by_turnout_rate(df, "event_type")
    best_promotion = _best_by_turnout_rate(df, "promotion_channel")
    best_day = _best_by_turnout_rate(df, "day_of_week")
    best_time = _best_by_turnout_rate(df, "start_time")
    best_location = _best_by_turnout_rate(df, "location")

    avg_attendance = int(df["actual_attendance"].mean())

    recommendation = f"""
### Event Optimization Recommendations

*Based on {len(df)} historical events in the dataset, ranked by turnout rate (actual ÷ expected attendance).*

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
