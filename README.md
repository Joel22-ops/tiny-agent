# tiny-agent

A small Python project where I learned how AI agents work.

- `first_call.py`: one prompt to an LLM
- `tool_call.py`: the model asks for a tool
- `tool_loop.py`: my script runs the tool and returns the result
- `chat_agent.py`: a chat version with memory and a loop

## What I learned
- The model only writes a text request. My script runs the tool.
- The model has no memory. The script resends the conversation each turn.
- Keep API keys out of code (use an environment variable).

## Run it
Set `GEMINI_API_KEY` in your terminal, then run a script with `python <file>`.
