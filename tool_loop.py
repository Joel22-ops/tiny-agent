import os
from datetime import datetime
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_time():
    """Returns the current local time."""
    return datetime.now().strftime("%H:%M on %d %B %Y")

tools = {"get_time": get_time}

config = types.GenerateContentConfig(
    tools=[get_time],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

# The context: a list of messages we keep and resend every call
contents = [
    types.Content(role="user", parts=[types.Part(text="What time is it right now?")])
]

# Call 1: the model asks for the tool
response = client.models.generate_content(
    model="gemini-3.8-flash", contents=contents, config=config
)
call = response.function_calls[0]
print("Model asked for:", call.name)

# Your script runs the real function
result = tools[call.name]()
print("Script ran it, got:", result)

# Put the model's request and our result into the context
contents.append(response.candidates[0].content)
contents.append(
    types.Content(
        role="user",
        parts=[types.Part.from_function_response(
            name=call.name, response={"result": result}
        )],
    )
)

# Call 2: the model reads the result and answers
final = client.models.generate_content(
    model="gemini-3.8-flash", contents=contents, config=config
)
print("Final answer:", final.text)
