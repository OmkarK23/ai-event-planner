def generate_marketing_content(
    event_name,
    event_type,
    location,
    date,
    time,
    target_audience
):
    content = f"""
==============================
EMAIL INVITATION
==============================

Subject: Join Us for {event_name}!

Hello,

We are excited to invite you to our upcoming {event_type}, "{event_name}", happening on {date} at {time} in {location}.

This event is specially designed for {target_audience}. Expect engaging sessions, networking opportunities, and valuable insights.

We hope to see you there!

Best Regards
Event Team


==============================
INSTAGRAM CAPTION
==============================

Exciting news!

Join us for {event_name} — a {event_type} designed for {target_audience}.

Date: {date}
Time: {time}
Location: {location}

Don't miss this opportunity!

#Event #Networking #CampusLife #AI


==============================
LINKEDIN POST
==============================

We are excited to announce "{event_name}" — an engaging {event_type} for {target_audience}.

Join us on {date} at {time} in {location} for learning, collaboration, and professional growth.

Looking forward to connecting with everyone.


==============================
REMINDER MESSAGE
==============================

Reminder!

{event_name} is happening on {date} at {time} in {location}.

We look forward to seeing you there.


==============================
THANK YOU MESSAGE
==============================

Thank you for attending {event_name}.

We appreciate your participation and hope the event provided meaningful value and connections.

Please share your feedback and stay connected for future events.
"""

    return content


if __name__ == "__main__":

    result = generate_marketing_content(
        event_name="Data Analytics Networking Night",
        event_type="Networking Event",
        location="University Center",
        date="June 15",
        time="6 PM",
        target_audience="graduate students and young professionals"
    )

    print(result)
