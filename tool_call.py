import os
from datetime import datetime
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_time():
    """Returns the current local time."""
    return datetime.now().strftime("%H:%M on %d %B %Y")

config = types.GenerateContentConfig(
    tools=[get_time],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="What time is it right now?",
    config=config,
)

print(response.function_calls)
