#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path
from typing import Any

import click
import yaml


# ---------------------------------------------------------
@click.command()
@click.option("--root", "--workspace-root", required=True, help="path to workspace")
@click.option("--wd", "--working-dir", help="dir where temp files can be put")
@click.option("--input_file", "--input", required=True, help="input file")
@click.option("--output_file", "--output", help="output file")
def set_project_team(root: Any, wd: Any, input_file: Any, output_file: Any) -> None:
    config = yaml.safe_load(Path(input_file).read_text())
    nconfig = config.get("ghw-nvci")
    if nconfig:
        default_project_team = nconfig.get("default_project_team")

    env_project_team = os.environ.get("PROJECT_TEAM")

    if env_project_team:
        project_team = env_project_team
    elif default_project_team:
        project_team = default_project_team

    print(f"{project_team}")


def runCmdOutput(cmd: str) -> str:
    output = subprocess.check_output(cmd, shell=True)
    out = output.decode().strip()
    return out


def main() -> None:
    set_project_team()
