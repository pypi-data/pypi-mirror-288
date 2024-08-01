#!/usr/bin/env python3

import subprocess

import click


@click.command()
@click.option("--prefix", help="Prefix for snapshot name")
@click.option("--suffix", help="Suffix for snapshot name")
@click.option(
    "--verbose", "-v", is_flag=True, default=False, help="Enable verbose output"
)
def nvci_snapshot(prefix: str, suffix: str, verbose: str) -> None:

    args = ""
    if prefix:
        args += f"--prefix {prefix}"
    if suffix:
        args += f" --suffix {suffix}"

    verb = ""
    if verbose:
        verb = "--verbose"

    cmd = f"workspace_manager {verb} run snapshot {args}"
    subprocess.run(cmd, shell=True, check=True)


def main() -> None:
    nvci_snapshot()
