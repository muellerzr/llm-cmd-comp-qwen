# Shell completion using LLM (Qwen3)

This is a fork of [llm-cmd-comp](https://github.com/CGamesPlay/llm-cmd-comp) that adds direct support for Qwen3 and its thinking tokens when hosted by providers like llama.cpp. The main advantage of this fork is that it can handle Qwen3's explicit thinking process tokens and execute commands directly.

Use LLM to generate and execute commands in your shell.

https://github.com/user-attachments/assets/c10d7a0f-48c3-4904-bb1b-4a1ce9f9ff8d

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-cmd-comp-qwen
```
Then install the shell integration for your preferred shell.

- **Fish**: place `share/llm-cmd-comp.fish` in `~/.config/fish/conf.d/`.
- **Zsh**: source `share/llm-cmd-comp.zsh` in your `~/.zshrc`.
- **Bash**: source `share/llm-cmd-comp.bash` in your `~/.bashrc`.

## Usage

There are two ways to use this plugin:

### 1. Direct Command Generation and Execution
Simply use the `llm term` command followed by your natural language description:
```bash
llm term "list all files larger than 100MB"
```
The command will be generated and executed automatically.

### 2. Interactive Shell Integration
1. Start typing a command.
2. Activate the key binding (Ctrl+k by default).
3. Wait for the LLM to complete the command.
4. Press enter if you are happy. Otherwise give feedback on the command and repeat from step 3.
5. The LLM's command replaces the previous command you were writing.

## Examples

Here are some ways you can use this feature:

- **Type a command in English, convert it to bash.**<br />
  `llm term "find all files larger than 100MB"`<br />
  🪄 `find . -type f -size +100M`
- **Give extra instructions as comments.**<br />
  `llm term "replace 'foo' with 'bar' in all Python files recursively"`<br />
  🪄 `find . -name '*.py' -exec sed -i 's/foo/bar/g' {} +`

## Features

- Direct command execution with `llm term`
- Support for Qwen3's thinking process tokens
- Compatible with llama.cpp and other LLM providers
- Interactive shell completion with customizable keybindings
- Works with bash, zsh, and fish shells

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-cmd-comp-qwen
python3 -m venv venv
source venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
pip install llm
llm install -e .
```
