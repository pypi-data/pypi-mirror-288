from bashcolor import colorize, LIGHT_PURPLE, BOLD, UNDERLINE

fancy_name = colorize('🧙 Bash Wizard', LIGHT_PURPLE)

help = f"""
Welcome to {fancy_name} 🪄
bash_wizard is an AI-powered wizard that creates bash commands to perform the action you need!

Usage: bash_wizard <command_request>
Arguments:
\t<command_request>: description of what the command should do.

Example:
\tbash_wizard remove all __pycache__ dir include subdirs
\tbash_wizard add a .gitkeep file in all empty subdirs
""".strip()

missing_ollama = "Error connecting to Ollama, check if it is installed correctly and running!"
missing_model = "Downloading Llama3 model! This may take a while, I recommend going for a coffee "
bye = "🧙 Okay bye!"


def thinking(description: str) -> str:
    fancy_description = colorize(description, effects=[UNDERLINE])
    return f"{fancy_name} is thinking 🔮 {fancy_description} 🔮 {colorize('')}"


def output(bash_command: str = None, command_explanation: str = None) -> str:
    fancy_command = colorize(bash_command, effects=[BOLD]) + colorize('')
    return f"""
{fancy_name} suggests the following command:

🪄 {fancy_command}

🧙 Explanation:
{command_explanation}

Do you want to execute 🪄 {fancy_command} (y/[n])?
""".strip()
