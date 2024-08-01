#!/usr/bin/env python3

import json
import os
import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

parser = ArgumentParser()
parser.add_argument("cl", nargs="?", default=None)

parser.add_argument(
    "-v", "--verbose", help="Enable verbose output", action="store_true"
)
parser.add_argument("--json", help="Output status in JSON format", action="store_true")
parser.add_argument("--qsub", help="Submit nvci verify to qsub", action="store_true")
parser.add_argument(
    "--keep-going",
    help="Continue running verification even if tasks fail",
    action="store_true",
)

parser.add_argument(
    "--crystal", help="Use a crystal workspace synced to TOT", action="store_true"
)
parser.add_argument(
    "--golden",
    help="Use a flexclone workspace synced to the latest golden CL",
    action="store_true",
)
parser.add_argument(
    "--golden_prebuilt",
    help="Use a prebuilt flexclone workspace synced to the latest golden CL",
    action="store_true",
)
parser.add_argument(
    "--golden_crystal",
    help="Use a crystal workspace synced to the latest golden CL",
    action="store_true",
)

parser.add_argument("--sync", dest="sync", help="Sync to TOT", action="store_true")
parser.add_argument(
    "--no-sync", dest="sync", help="Do not sync to TOT", action="store_false"
)
parser.set_defaults(sync=True)

parser.add_argument(
    "--name",
    help="Specify workspace name (default 'nvgpu_asbtest')",
    default="nvci_asbtest",
)
parser.add_argument(
    "--resolve-cmd",
    help="Special command to resolve workspace conflicts after applying shelvelist",
)
parser.add_argument(
    "--pre-verify-cmd", help="Additional command to run before nvci verify"
)
parser.add_argument(
    "--post-verify-cmd", help="Additional command to run after nvci verify"
)

parser.add_argument(
    "--bar",
    action="append",
    help="Bar to run using nvci verify. May be specified multiple times",
)
parser.add_argument(
    "--task",
    action="append",
    help="Tasks to run using nvci verify. May be specified multiple times",
)

parser.add_argument(
    "--as2-submit", help="Submit to AS2 if verification passes", action="store_true"
)
parser.add_argument("--as2-submit-args", help="AS2 submission arguments")

parser.add_argument("--buildrules", help="Path to alternate asb buildrules")

args = None


# ---------------------------------------------------------
def main() -> None:
    global args
    args = parser.parse_args()
    if args.golden:
        # Golden sync-only flexclone workspace from GCS
        workspace_type = "ghw-infra/nvgpu/gcs_sync"
    elif args.golden_crystal:
        # Golden sync-only crystal workspace from GCS
        workspace_type = "ghw-infra/nvgpu/gcs_sync_cfs"
    elif args.golden_prebuilt:
        # Golden prebuilt flexclone workspace from GCS
        workspace_type = "ghw-infra/nvgpu/gcs"
    else:
        if args.crystal:
            workspace_type = "ghw-nvci/nvgpu/asbtest_cfs"
        else:
            workspace_type = "ghw-nvci/nvgpu/asbtest"

    result = runCmd(
        f"nvci --json create {workspace_type} --name {args.name}", args, True
    )

    # cd to workspace tree
    workspace_root = json.loads(result)["root"]
    print(f"Created workspace: {workspace_root}")

    tree_path = Path(workspace_root) / "hw/nvgpu"
    os.chdir(tree_path)

    if args.cl is not None:
        # Unshelve changelist into workspace
        runCmd(f"p4 unshelve -s {args.cl}", args)

    if args.sync:
        # sync to TOT
        runCmd("p4 sync", args)

    # resolve and merge all files without conflicts
    resolve_failed: Any = False
    if args.resolve_cmd:
        result = runCmd(args.resolve_cmd, args)
        resolve_failed = re.search("failed", result)
    else:
        result = runCmd("p4 resolve -am", args)
        resolve_failed = re.search("resolve skipped", result)

    if resolve_failed:
        print("Resolve failed; skipping verification.")
        exit(1)

    if args.pre_verify_cmd:
        runCmd(args.pre_verify_cmd, args)

    if args.qsub:
        qsub = "--qsub"
    else:
        qsub = ""

    cmd = f"nvci verify {qsub} --bar asbtest"

    # Run verification
    if args.bar:
        for bar in args.bar:
            cmd += f" --bar {bar}"
    elif args.task:
        for task in args.task:
            cmd += f" --task {task}"
    else:
        cmd += " --set asb_trigger true"

    if args.buildrules:
        cmd += f" --set asb.buildrules {args.buildrules}"

    if args.keep_going:
        cmd += " --keep-going"

    execCmd(cmd, args)

    if args.post_verify_cmd:
        runCmd(args.post_verify_cmd, args)

    if args.as2_submit:
        # Submit to AS2
        acmd = "as2 submit "
        if args.as2_submit_args:
            acmd += args.as2_submit_args
        execCmd(acmd, args)


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
