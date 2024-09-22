import openai
import json
with open("config/bot_config.json", "r") as f:
    bot_cred = json.load(f)

openai.api_key = bot_cred["openai_api_key"]

def ask_gpt(prompt):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = response.choices[0].text.strip()
    return message

def parse_command(user_input):
    prompt = f"Convert this command into an actionable task: '{user_input}'"
    return ask_gpt(prompt)
