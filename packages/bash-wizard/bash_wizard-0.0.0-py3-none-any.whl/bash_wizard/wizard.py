import httpx
import ollama
import json
import sys
import subprocess

from bash_wizard import messages

model = 'llama3'
ollama_args = {
    "model": model,
    "format": "json",
    "stream": False,
    "options": {
        "temperature": 2.5,
        "top_p": 0.99,
        "top_k": 100,
        "seed": 23265971542
    },
}
response_template = '{"bash_command": "", "command_explanation": ""}'


def pull_model():
    status = ""
    for progress in ollama.pull(model, stream=True):
        if status != progress['status']:
            print('☕️ ', end="", flush=True)
            status = progress['status']
    print(' done! 🙌', flush=True)


def check_model():
    try:
        ollama.show(model)
    except httpx.ConnectError:
        print(messages.missing_ollama)
        exit(1)
    except ollama._types.ResponseError:
        print(messages.missing_model, end="")
        pull_model()


def args_description():
    description = ' '.join(sys.argv[1:])
    if not description or description == '-h':
        print(messages.help)
        exit(0)

    return description


def generate(description: str) -> dict:
    prompt = f"""
You are a linux bash command line wizard, please answer how can I do:

{description}.

Use the following template: {response_template}.
"""
    response = ollama.generate(prompt=prompt.strip(), **ollama_args)
    data = json.loads(response['response'])

    return {key: value.strip() for key, value in data.items()}


def run():
    check_model()

    description = args_description()
    print(messages.thinking(description))

    response = generate(description)
    user_input = input(messages.output(**response)).strip().lower()
    if user_input == 'y':
        print(f"\n\n{response['bash_command']}")
        subprocess.run(response['bash_command'], shell=True)
    else:
        print(messages.bye)
