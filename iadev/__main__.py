import argparse
from os import path, makedirs
from shutil import rmtree

from iadev.LLM.Agent import Agent
from iadev.LLM.Server import *

servers = {
    "pasteur": PasteurLibreChat,
    "local": OllamaLocal
}

def parse_args():
    parser = argparse.ArgumentParser(description="IADEV - IA Development Environment")
    parser.add_argument("--project", '-p', type=argparse.FileType("r"), default="./project.md",
        help="Path to the description of the project to be developed.")
    parser.add_argument("--outdir", '-o', type=str,
        help="Path to the directory where the project will be created. default='<project>_out/")
    parser.add_argument("--server", type=str, choices=["pasteur"], default="pasteur",
        help="AI server to use.")
    args = parser.parse_args()

    if args.outdir is None:
        args.outdir = path.splitext(args.project.name)[0] + "_out"
    if path.exists(args.outdir):
        rmtree(args.outdir)
    args.outdir = path.abspath(args.outdir)
    makedirs(args.outdir, exist_ok=True)

    return args

def main():
    args = parse_args()

    # Join the AI server
    server = servers[args.server]()
    server.connect()

    # Project loading
    project_content = args.project.read()
    args.project.close()

    # Ask the supervisor to handle the project
    supervisor = server.agent_from_yaml("agents/supervisor.yaml")
    answer = supervisor.ask("Here is the project description:\n" + project_content)
    with open(path.join(args.outdir, "log.txt"), "w") as log:
        print(answer, file=log)

    return 0

if __name__ == "__main__":
    main()