#!/usr/bin/env python3

import json
import os
import subprocess
from pathlib import Path
from typing import Any

import click
import yaml


# ---------------------------------------------------------
@click.command()
@click.option("--root", "--workspace-root", help="path to workspace")
@click.option("--wd", "--working-dir", help="dir where temp files can be put")
@click.option("--input_file", "--input", required=True, help="input file")
@click.option("--output_file", "--output", help="output file")
def xform(root: Any, wd: Any, input_file: Any, output_file: Any) -> None:
    transformer = "ytt_parse"
    source = "n/a"

    # Look in input yml file for transformer name/version
    cversion = ""
    config = yaml.safe_load(Path(input_file).read_text())
    if config:
        nconfig = config.get("ghw-nvci")
        if nconfig:
            cversion = nconfig.get("version")
            ctransformer = nconfig.get("transformer")
            if ctransformer:
                transformer = ctransformer

    uselocal = os.environ.get("USE_LOCAL_GHW_NVCI")
    local = os.environ.get("LOCAL_GHW_NVCI")
    if uselocal and local:
        # Use transformer from local virtual environment
        source = "LOCAL_GHW_NVCI"
        bindir = f"{local}/.venv/bin"
    else:
        # Use transformer from released version of ghw-nvci
        version = ""

        # Look for version in OS enviornment
        eversion = os.environ.get("GHW_NVCI_VERSION")

        # Look for version in nvci environment
        nversion = json.loads(runCmdOutput("nvci env get ghw_nvci.version"))

        if eversion:
            # version set in OS enviornment
            version = eversion
            source = "GHW_NVCI_VERSION"
        elif nversion:
            # version set in nvci environment
            version = nversion
            source = "nvci-env"
        elif cversion:
            # version set in input yaml file
            version = cversion
            source = "input file"
        else:
            # default to latest version
            version = "latest"
            source = "default"

        bindir = f"/home/nv/utils/ghw-nvci/{version}/bin"

    xform = f"{bindir}/{transformer}"

    print(f"xform.py: Running transfomer {xform} from {source}\n")
    runCmdOutput(
        f"{xform} --root {root} --wd {wd} --input {input_file} --output {output_file}"
    )


def runCmdOutput(cmd: str) -> str:
    output = subprocess.check_output(cmd, shell=True)
    out = output.decode().strip()
    return out


def main() -> None:
    xform()
