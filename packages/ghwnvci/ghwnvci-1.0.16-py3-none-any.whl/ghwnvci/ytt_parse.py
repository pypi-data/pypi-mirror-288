#!/usr/bin/env python3

import subprocess
from pathlib import Path
from typing import Any

import click
import yaml

from ghwnvci import conman


# ---------------------------------------------------------
@click.command()
@click.option("--root", "--workspace-root", required=True, help="path to workspace")
@click.option("--wd", "--working-dir", help="dir where temp files can be put")
@click.option("--input_file", "--input", required=True, help="input file")
@click.option("--output_file", "--output", help="output file")
@click.option("--include", "-i", multiple=True, help="ytt include directories")
def ytt_parse(
    root: str, wd: str, input_file: str, output_file: str, include: str
) -> None:

    print(f"root={root} input={input_file} output={output_file}")

    # Read metadata from input .yml file
    config = yaml.safe_load(Path(input_file).read_text())
    nconfig = config.get("ghw-nvci")
    yconfig = ""
    yincludes = ()
    wincludes = ()
    if nconfig:
        yconfig = nconfig.get("ytt_parse", "")
    if yconfig:
        yincludes = yconfig.get("conman_includes", ())  # type: ignore
        wincludes = yconfig.get("workspace_includes", ())  # type: ignore

    conmandir = Path(f"{root}/conman")

    cmd = f"ytt -f {input_file}"

    test_file = ".pretransform.yml"
    tcmd = f"ytt -f {test_file}"

    # Add specified includes
    if yincludes:
        for inc in yincludes:
            incpath = get_content(conmandir, inc)
            arg = f" -f {conmandir}/{incpath}"
            cmd += arg
            tcmd += arg

    if wincludes:
        for inc in wincludes:
            arg = f" -f {inc}"
            cmd += arg
            tcmd += arg

    for inc in include:
        incpath = get_content(conmandir, inc)
        arg = f" -f {conmandir}/{incpath}"
        cmd += arg
        tcmd += arg

    if output_file:
        cmd += f" > {output_file}"

    runCmdOutput(f"cp {input_file} {test_file}")
    testout = ".pretransform.cmd"
    runCmdOutput(f"echo {tcmd} > {testout}")

    out = runCmdOutput(cmd)
    print(out)


def get_content(conmandir: Any, inc: Any) -> Any:
    (path, version) = conman.path_version(inc)
    if not version:
        version = "latest"
    namespace = path.split("/")[0]
    # print(f"get_content: namespace={namespace} version={version} path={path}")
    conman.download_desired_version(namespace, conmandir, True, version)
    return path


def runCmdOutput(cmd: Any) -> str:
    output = subprocess.check_output(cmd, shell=True)
    out = output.decode().strip()
    return out


def main() -> None:
    ytt_parse()
