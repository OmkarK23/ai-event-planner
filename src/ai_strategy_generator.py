def generate_event_strategy(
    event_type,
    target_audience,
    expected_audience,
    budget,
    location,
    day_of_week,
    start_time,
    promotion_channel
):
    strategy = f"""
1. Event Strategy
Plan a {event_type} for {target_audience} at {location}. Since the expected audience is {expected_audience}, arrange seating, registration, and check-in support in advance.

2. Best Promotion Plan
Use {promotion_channel} as the main promotion method. Start promotion 2 weeks before the event, send reminders 3 days before and 1 day before the event.

3. Possible Risks
Low attendance, poor timing, lack of engagement, and budget overruns.

4. Risk Mitigation Plan
Use RSVP tracking, reminder emails, backup speakers, and a clear event checklist.

5. Engagement Ideas
Add icebreakers, polls, Q&A sessions, networking breaks, and small giveaways.

6. Reminder Message
Reminder: Join us for our upcoming {event_type} on {day_of_week} at {start_time} in {location}. We look forward to seeing you there!

7. Post-Event Follow-Up Plan
Send a thank-you email, collect feedback, analyze attendance, and document lessons learned for future events.
"""
    return strategy


if __name__ == "__main__":
    strategy = generate_event_strategy(
        event_type="Networking",
        target_audience="Graduate students interested in data analytics",
        expected_audience=120,
        budget=1500,
        location="University Center",
        day_of_week="Thursday",
        start_time="6PM",
        promotion_channel="Email and LinkedIn"
    )

    print(strategy)
