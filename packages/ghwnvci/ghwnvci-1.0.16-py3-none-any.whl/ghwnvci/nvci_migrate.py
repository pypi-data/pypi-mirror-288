#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from argparse import ArgumentParser
from typing import Any

import nv_p4

client_tool = "/home/nv/utils/client_tool/5.1.4/bin/client_tool"
p4 = "/home/nv/utils/crucible/1.0/bin/p4 -d `/bin/pwd`"
p4mapper = "/home/nv/utils/p4mapper/latest/bin/p4mapper"

parser = ArgumentParser()
parser.add_argument("--name", required=True, help="Name for migrated workspace")
parser.add_argument(
    "-v", "--verbose", help="Enable verbose output", action="store_true"
)
args = None


# ---------------------------------------------------------
def main() -> None:
    global args
    args = parser.parse_args()
    workspace_dir = runCmd("workspace_manager root -d .", args)
    print(f"The workspace directory is {workspace_dir}")

    client_result = runCmd(f"{client_tool} --json clients --root {workspace_dir}", args)
    client_json = json.loads(client_result)
    complexes = client_json.get("complexes", {})

    # TBD: if --name is not specified, determine name of current workspace and add a unique suffix

    applycls = []
    for p4complex in complexes:
        complexdata = complexes[p4complex]
        p4client = complexdata.get("client_name", None)
        port = complexdata.get("port", None)
        print(f"port={port}  client={p4client}")
        p4port = runCmd(f"{p4mapper} best -p {port}", args)
        desc = f"nvci migrate: shelve open files for client {p4client}"

        p4 = nv_p4.P4(port=p4port, client=p4client, shell=True)
        opened = p4.opened()
        if opened:
            ofiles = opened.files  # type: ignore
            open_files = []
            for ofile in ofiles:
                open_files.append(ofile.depot_file)

            printStruct(open_files)

            changelist = p4.create_change(description=desc, files=open_files)
            print(f"created changelist {changelist}")

            changeobj = p4.get_change(changelist)  # type: ignore
            # shelve open changes
            shelveresult = p4.shelve(changeobj)  # type: ignore
            applycls.append("--apply " + shelveresult.change + "." + p4complex)  # type: ignore

    cmd = f"workspace_manager migrate --no-sync --name {args.name} " + " ".join(
        applycls
    )
    runCmd(cmd, args)


# ---------------------------------------------------------
def execCmd(cmd: str, args: Any) -> None:
    printStderr(cmd)
    result = subprocess.run(cmd, shell=True, text=True)

    if result.returncode:
        if args.verbose:
            result.check_returncode()
        else:
            printStderr(
                f"ERROR: Command '{cmd}' failed with status {result.returncode}"
            )
            exit(result.returncode)


# ---------------------------------------------------------
def runCmd(cmd: str, args: Any, isjson: bool = False) -> str:
    printStderr(cmd)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if isjson:
        jresult = json.loads(result.stdout)
        if "error" in jresult.keys():
            msg = jresult["error"]["Couldn't create workspace"][
                "Failed while creating workspace directory"
            ]["Process error during workspace creation"]["stderr"]
            printStderr(msg)
    else:
        if result.stdout:
            printStderr("stdout: " + result.stdout)
        if result.stderr:
            printStderr("stderr: " + result.stderr)

    if result.returncode:
        if args.verbose:
            result.check_returncode()
        else:
            printStderr(
                f"ERROR: Command '{cmd}' failed with status {result.returncode}"
            )
            exit(result.returncode)

    return result.stdout.strip()


def printStderr(msg: str) -> None:
    print(msg, file=sys.stderr)


def find_workspace_dir() -> Any:
    # Start from the current directory
    current_dir = os.getcwd()

    # Keep traversing up until the root directory
    while True:
        # Check if .workspace directory exists in the current directory
        if ".workspace" in os.listdir(current_dir):
            # Return the parent directory of .workspace
            return current_dir

        # Move up one directory
        parent_dir = os.path.dirname(current_dir)

        # If we reach the root directory without finding .workspace, break
        if current_dir == parent_dir:
            break

        current_dir = parent_dir

    # Return None if .workspace directory is not found
    return None


def printStruct(struc: Any, indent: Any = 0) -> None:
    if isinstance(struc, dict):
        print("  " * indent + "{")
        for key, val in struc.items():
            if isinstance(val, (dict, list, tuple)):
                print("  " * (indent + 1) + str(key) + "=> ")
                printStruct(val, indent + 2)
            else:
                print("  " * (indent + 1) + str(key) + "=> " + str(val))
        print("  " * indent + "}")
    elif isinstance(struc, list):
        print("  " * indent + "[")
        for item in struc:
            printStruct(item, indent + 1)
        print("  " * indent + "]")
    elif isinstance(struc, tuple):
        print("  " * indent + "(")
        for item in struc:
            printStruct(item, indent + 1)
        print("  " * indent + ")")
    else:
        print("  " * indent + str(struc))
