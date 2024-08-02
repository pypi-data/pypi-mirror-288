# Bash Wizard 🧙
[![Test Bash Wizard](https://github.com/alexandreprates/bash_wizard/actions/workflows/test.yml/badge.svg)](https://github.com/alexandreprates/bash_wizard/actions/workflows/test.yml)

`bash_wizard` is a command line wizard that helps you generate bash commands. It leverages the power of AI (llama3) to provide explanations and generate bash commands based on user queries.

## Features

- Generate bash commands based on natural language queries.
- Provide explanations for bash commands.
- Easy to use and integrate into your workflow.

### Dependencies

* [Ollama](https://github.com/ollama/ollama)
Bash Wizard uses the Ollama endpoint to run the AI ​​model

## Installation

```sh
pip install bash_wizard
```

## Usage

To use `bash_wizard`, simply run the command with your query as an argument:

```sh
bash_wizard <task description>
```

### Arguments

`<task description>`: describe what you want the command to do.


## Example
```sh
bash_wizard remove all __pycache__ dir include subdirs
```

The bash_wizard will suggest the best command to perform the requested action.

If the suggested command does not meet your needs, try changing the description to get a better answer.

# Contributing
Contributions are welcome! Please open an issue or submit a pull request.

# License
This project is licensed under the MIT License.
