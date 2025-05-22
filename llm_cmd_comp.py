import click
import platform
import os
import llm
import string
import re
from prompt_toolkit import PromptSession
from prompt_toolkit.input import create_input
from prompt_toolkit.output import create_output

SYSTEM_PROMPT = string.Template(
    """Return only the command to be executed as a raw string, no string delimiters wrapping it, no yapping, no markdown, no fenced code blocks, what you return will be passed to the shell directly.
For example, if the user asks: undo last git commit
You return only: git reset --soft HEAD~1
The shell is $shell on $platform
""".strip()
)


@llm.hookimpl
def register_commands(cli):
    @cli.command()
    @click.argument("args", nargs=-1)
    @click.option("-m", "--model", default=None, help="Specify the model to use")
    @click.option("-s", "--system", help="Custom system prompt")
    @click.option("--key", help="API key to use")
    def cmdcomp(args, model, system, key):
        """Generate commands directly in your command line (requires shell integration)"""
        from llm.cli import get_default_model

        prompt = " ".join(args)
        model_id = model or get_default_model()
        model_obj = llm.get_model(model_id)
        if model_obj.needs_key:
            model_obj.key = llm.get_key(key, model_obj.needs_key, model_obj.key_env_var)
        conversation = model_obj.conversation()
        system = system or render_default_prompt()
        interactive_exec(conversation, prompt, system)


def render_default_prompt():
    return SYSTEM_PROMPT.substitute(
        shell=os.path.basename(os.getenv("SHELL") or "sh"), platform=platform.system()
    )


def interactive_exec(conversation, command, system):
    ttyin = create_input(always_prefer_tty=True)
    ttyout = create_output(always_prefer_tty=True)
    session = PromptSession(input=ttyin, output=ttyout)
    system = system or SYSTEM_PROMPT

    command = conversation.prompt(command, system=system)
    while True:
        ttyout.write("$ ")
        for chunk in command:
            ttyout.write(chunk.replace("\n", "\n> "))
        command = command.text()
        ttyout.write("\n# Provide revision instructions; leave blank to finish\n")
        feedback = session.prompt("> ")
        if feedback == "":
            break
        command = conversation.prompt(feedback, system=system)
    # Remove any thinking tags and their contents
    command = re.sub(r"<think>.*?</think>", "", command, flags=re.DOTALL)
    print(command)
