"""
Marketing content generator.

Calls OpenAI to write the actual copy when an API key is configured. Falls back
to the deterministic template below when it isn't (or if the API call fails for
any reason), so the app still works for anyone running it without a key --
it just tells you which mode produced the output.

Configure the key via ONE of:
  - environment variable OPENAI_API_KEY, or
  - Streamlit secrets: .streamlit/secrets.toml with OPENAI_API_KEY = "sk-..."
    (on Streamlit Cloud: App settings -> Secrets)

Never commit a real key to the repo -- .streamlit/secrets.toml should be in
.gitignore.
"""

import os

DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = (
    "You are a marketing copywriter for university and community events. "
    "Write concise, energetic, platform-appropriate copy. Return concrete, "
    "ready-to-send copy -- no placeholders, no meta-commentary, no markdown "
    "headers beyond what's requested."
)


def _get_api_key():
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None


def _template_fallback(event_name, event_type, location, date, time, target_audience):
    return f"""
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

#Event #Networking #CampusLife


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


def generate_marketing_content(
    event_name,
    event_type,
    location,
    date,
    time,
    target_audience,
    model=DEFAULT_MODEL,
):
    """
    Returns (content: str, used_ai: bool, note: str | None).
    `used_ai` tells the caller which path produced the content, so the UI can be
    honest about it instead of silently reformatting a template as "AI-generated."
    """
    api_key = _get_api_key()

    if not api_key:
        return (
            _template_fallback(event_name, event_type, location, date, time, target_audience),
            False,
            "No OPENAI_API_KEY configured -- showing the rule-based template instead.",
        )

    prompt = f"""Write marketing content for this event:
Event name: {event_name}
Event type: {event_type}
Location: {location}
Date: {date}
Time: {time}
Target audience: {target_audience}

Produce exactly five sections, each preceded by a line of 30 "=" characters,
the section name in caps, then another line of 30 "=" characters, in this order:
EMAIL INVITATION (include a Subject line), INSTAGRAM CAPTION (include hashtags),
LINKEDIN POST, REMINDER MESSAGE, THANK YOU MESSAGE."""

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=900,
        )
        return response.choices[0].message.content, True, None

    except Exception as e:
        fallback = _template_fallback(event_name, event_type, location, date, time, target_audience)
        return fallback, False, f"AI generation failed ({e}) -- showing the rule-based template instead."


if __name__ == "__main__":
    content, used_ai, note = generate_marketing_content(
        event_name="Data Analytics Networking Night",
        event_type="Networking Event",
        location="University Center",
        date="June 15",
        time="6 PM",
        target_audience="graduate students and young professionals",
    )
    print(f"[used_ai={used_ai}] {note or ''}")
    print(content)
