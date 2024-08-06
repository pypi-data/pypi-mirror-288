#!/bin/env python3
from pathlib import Path
import json
import sys,os
from openai import OpenAI
from rich.console import Console
from .gai_docker_start import docker_start
from .gai_docker_stop import docker_stop
from .gai_init import init
from .gai_pull import pull
from .gai_news import news
from .gai_search import search

console=Console()

from gai.lib.common.utils import this_dir
here = this_dir(__file__)

def app_dir():
    with open(Path("~/.gairc").expanduser(), "r") as file:
        rc=file.read()
        jsoned = json.loads(rc)
        return Path(jsoned["app_dir"]).expanduser()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Gai CLI Tool')
    parser.add_argument('command', choices=['init', 'pull', 'news', 'search','docker'], help='Command to run')
    parser.add_argument('-f', '--force', action='store_true', help='Force initialization')
    parser.add_argument('extra_args', nargs='*', help='Additional arguments for commands')

    args = parser.parse_args()

    if args.command == "init":
        print("Initializing...by force" if args.force else "Initializing...")
        init(force=args.force)
    elif args.command == "pull":
        if args.extra_args:
            pull(console, args.extra_args[0])
        else:
            console.print("[red]Model name not provided[/]")
    elif args.command == "news":
        if args.extra_args:
            news(args.extra_args[0])
        else:
            news()
    elif args.command == "search":
        if args.extra_args:
            search(args.extra_args[0])
        else:
            console.print("[red]Search term not provided[/]")
    elif args.command == "docker":
        if args.extra_args:
            if args.extra_args[0] == "start":
                docker_start(here)
            elif args.extra_args[0] == "stop":
                docker_stop(here)
            else:
                console.print("[red]Invalid docker command[/]")


if __name__ == "__main__":
    main()
