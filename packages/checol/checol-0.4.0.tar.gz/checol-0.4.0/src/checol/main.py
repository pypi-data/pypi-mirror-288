import os
from os.path import join, dirname

import fire
from halo import Halo
from prompt_toolkit import prompt
from dotenv import load_dotenv

from checol.gpt.claude import Claude
from checol.gpt.chat_gpt import ChatGPT
from checol.vcs import Git

spinner = Halo(text="Loading", spinner="dots")
dotenv_path = join(dirname(__name__), '.env')
load_dotenv(verbose=True, dotenv_path=dotenv_path)


def generate_response(system_message: str, file_text: str) -> None:
    model_name = os.environ.get("API_MODEL", "gpt-4o-mini")
    api_key = os.environ.get("API_KEY")
    match model_name:
        case "gpt-4o-mini":
            model = ChatGPT(
                api_key=api_key, model=model_name, system=system_message
            )
        case "claude-3-haiku-20240307":
            model = Claude(
                api_key=api_key, model=model_name, system=system_message
            )
        case _:
            raise ValueError(f"Model {model_name} is not supported.")
    description = prompt("Description > ", multiline=True)

    sending_message = f"{description}\n\n{file_text}" if description else file_text

    spinner.start()
    message = model.send(sending_message)
    spinner.stop()

    while True:
        print("AI > ", end="")
        for line in message.split("\n"):
            print(line)
        user_message = prompt("You > ", multiline=True)
        spinner.start()
        message = model.send(user_message)
        spinner.stop()


def diff(spec: str = "", cached=False):
    git_path = os.getcwd()
    git = Git(git_path)
    if cached:
        spec = f"{spec} --cached"
    diff = git.diff(spec)
    generate_response(
        "このコード差分を見てプロの目線でコードレビューしてください", diff
    )


def prismaQuery(prisma_schema_file_path: str = ""):
    with open(prisma_schema_file_path) as f:
        prisma_schema = f.read()
    generate_response(
        "Prsimaのスキーマファイルです｡要望に応じてSQLを書いてください", prisma_schema
    )


def main():
    if os.environ.get("API_KEY") is None:
        print("Please set API_KEY environment variable.")
        return
    print("CTRL+C to exit.")
    print("To confirm, type Enter with an empty space.")
    fire.Fire({"diff": diff, "prismaQuery": prismaQuery})


if __name__ == "__main__":
    main()
