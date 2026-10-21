import os
from datetime import datetime
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3.8-flash"


def get_time():
    """Returns the current local time."""
    return datetime.now().strftime("%H:%M on %d %B %Y")


tools = {"get_time": get_time}

config = types.GenerateContentConfig(
    tools=[get_time],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

# The context. Created ONCE, so it keeps growing across turns.
contents = []

print("Chat started. Type 'quit' to stop.")

while True:
    user_text = input("You: ")
    if user_text.strip().lower() == "quit":
        break

    contents.append(types.Content(role="user", parts=[types.Part(text=user_text)]))

    # Agent loop: keep going until the model answers without asking for a tool
    while True:
        response = client.models.generate_content(
            model=MODEL, contents=contents, config=config
        )
        contents.append(response.candidates[0].content)

        if not response.function_calls:
            break

        parts = []
        for call in response.function_calls:
            result = tools[call.name]()
            print("  [tool ran]", call.name, "->", result)
            parts.append(
                types.Part.from_function_response(
                    name=call.name, response={"result": result}
                )
            )
        contents.append(types.Content(role="user", parts=parts))

    print("AI:", response.text)
