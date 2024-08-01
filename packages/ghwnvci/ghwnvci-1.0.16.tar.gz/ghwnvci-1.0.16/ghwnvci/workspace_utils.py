#!/usr/bin/env python3

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from shutil import rmtree
from typing import Any, NoReturn, Optional, Union

import click
import yaml
from p4mapper import P4Mapper

from ghwnvci import conman

debug = False
manifest_file = "manifest.yml"

DEFAULT_PATH_PADDING = 80

p4 = "/home/nv/utils/crucible/1.0/bin/p4 -d `/bin/pwd`"
crystal = "/home/nv/utils/crystal_cli/current/bin/crystal"

flexapi_dir = "/home/nv/utils/flexclone/FlexAPI/RELEASE"
cloneline_get_info = f"{flexapi_dir}/bin/cloneline_get_info.pl"
cloneline_admin = f"{flexapi_dir}/bin/cloneline_admin.pl"
clist = f"{flexapi_dir}/bin/clist.pl"
flexcl = f"{flexapi_dir}/bin/flexcl"

rule_engine = "/home/nv/utils/flexclone/RuleEngine/RELEASE/bin/rule_engine"

golden_cl = "/home/nv/utils/GoldenCl/v2_latest/bin/golden_cl"
rules_cl = "/home/nv/utils/quasar/bin/rules_cl.pl"

nvctdb = "/home/nv/bin/nvctdb"
projectname = "/home/nv/utils/nvchip/bin/projectname"
nvprojectname = "/home/nv/bin/nvprojectname"

crystal = "/home/nv/utils/crystal_cli/current/bin/crystal"
crystal_opts = "--override_uname_requirement"

# wm_ver = "2.1.0"
# workspace_manager = f"/home/nv/utils/ci/workspace_manager/{wm_ver}/bin/workspace_manager"
# Pick this up from the user's path
workspace_manager = "workspace_manager"

# ---------------------------------------------------------
# Standard ghw-nvci naming convention
# centralized here to make changes easier


def clientName(base: str, p4depot: str) -> str:
    # Add the p4depot (hw,sw) to form a client name
    return f"{base}-{p4depot}"


def snapshotName(data: Any, prefix: str, name: str, suffix: str) -> str:
    cloneline = getCloneline(data)
    site = getSite()
    revstr = getRevisionString(data)
    tag = getTag(data)

    if prefix:
        pre = prefix
    elif cloneline:
        pre = cloneline
    else:
        pre = name

    if suffix:
        suf = "_" + suffix
    elif tag:
        suf = "_" + tag
    else:
        suf = ""

    snapshotname = f"{pre}_{site}_{revstr}{suf}"
    return snapshotname


def isScratch(data: Any) -> bool:
    # returns True if this is a scratch space
    storage_type = data.get("storage_type")
    if storage_type == "scratch":
        return True
    else:
        return False


def isCloneable(data: Any) -> bool:
    # returns True if this is a clone volume (flexclone or cfs)
    storage_type = data.get("storage_type")
    if storage_type == "scratch":
        return False
    if storage_type == "flexclone" or storage_type == "cfs":
        return True
    else:
        # Default to true for legacy compatability
        return True


def isFlexclone(data: Any) -> bool:
    # returns True if this is a flexclone storage type
    storage_type = data.get("storage_type")
    if storage_type == "flexclone":
        return True
    else:
        return False


def newCFSName(base: str) -> str:
    username = userName()
    timestamp = getCurrentTimestring()
    return f"{username}_{base}_{timestamp}"


def mainCFSName(data: Any, name: str) -> str:
    main_pad_length = data.get("path_padding", DEFAULT_PATH_PADDING)
    main_pad_prefix = "_m"
    main_pad_string = "0"
    pad_seperator = "_"
    pad_seperator_interval = 10

    username = userName()
    site = getSite()
    cloneline = getCloneline(data)
    mainname = f"{username}_{site}_{cloneline}_{name}"

    return padName(
        mainname,
        main_pad_length,
        main_pad_prefix,
        main_pad_string,
        pad_seperator,
        pad_seperator_interval,
    )


def padName(
    name: str,
    pad_length: Any,
    pad_prefix: str,
    pad_string: str,
    pad_separator: str,
    pad_separator_interval: int,
) -> str:
    # Calculate the current total length after adding the pad_prefix
    current_length = len(name) + len(pad_prefix)

    # Check if the current total length is less than the required pad_length
    if current_length < pad_length:
        # Calculate the number of characters needed to reach pad_length
        needed_length = pad_length - current_length

        # Generate repeated pad_strings to ensure it's long enough
        repeated_pad_string = pad_string * ((needed_length // len(pad_string)) + 1)

        # Insert pad_separator at every pad_separator_interval in the repeated_pad_string
        segments = []
        for i in range(0, len(repeated_pad_string), pad_separator_interval):
            segments.append(repeated_pad_string[i : i + pad_separator_interval])
        full_pad_string = pad_separator.join(segments)

        # Adjust full_pad_string to fit exactly the needed_length
        full_pad_string = full_pad_string[:needed_length]

        # Combine name, prefix, and the necessary amount of pad_string
        name = name + pad_prefix + full_pad_string

    return name


def cloneName(base: str) -> str:
    username = userName()
    timestamp = getCurrentTimestring()
    return f"{username}_{base}_{timestamp}"


def userName() -> Any:
    user: Any = os.environ.get("USER")
    # Squash service account names
    username = user.replace("svc-ghw-", "sg")
    # All dashes (-) must be removed from clone names
    return username.replace("-", "")


def cloneNameFromPath(path: Any) -> Any:
    clonename = Path(path).name
    return clonename


def clonelinePath(data: Any) -> Any:
    # Returns the base path of the cloneline

    # Find the index of the main directory
    path = sourcePath(data)
    m_index = None
    if path is not None:
        for i, part in enumerate(path.parts):
            if part == "m":
                m_index = i
                break

    # Extract the path up to the main directory
    if m_index is not None:
        truncated_path = path.parts[:m_index]
        return str(Path(*truncated_path))
    else:
        exitWithError(f"main directory not found in {path}")


def clonePath(data: Any, clonename: str) -> str:
    # Returns the path to the specified clone
    clonelinepath = clonelinePath(data)
    path = f"{clonelinepath}/c/{clonename}"
    return path


def CFSNameFromPath(path: Any) -> Any:
    cfsname = Path(path).name
    return cfsname


def revisionFromCloneName(clonename: str, p4depot: str) -> Any:
    # Returns CL for p4depot from clone name
    pattern = rf"_{p4depot}(\d+)_"
    match = re.search(pattern, clonename)
    if match:
        return match.group(1)
    else:
        exitWithError(f"no revision for {p4depot} found in {clonename}")


def setPath(data: Any, path: Any) -> None:
    printStderr(f"setting path = {path}")
    data["path"] = path


def sourcePath(data: Any) -> Any:
    p = data.get("path")
    if p:
        path = Path(p)
        if path.exists():
            return path
        else:
            exitWithError(f"sourcePath {path} does not exist!")
    else:
        exitWithError("sourcePath not found!")


def clonelineName(data: Any) -> Any:
    # Extracts the cloneline name from the source path
    clonelinepath = sourcePath(data)
    return clonelinePrefix(clonelinepath)


def getCloneline(data: Any) -> Any:
    if "cloneline" in data:
        cloneline = data.get("cloneline", "")
    else:
        cloneline = clonelineName(data)
    return cloneline


def getTag(data: Any) -> Any:
    if "snapshot_tag" in data:
        tag = data.get("snapshot_tag", "")
    else:
        tag = ""
    return tag


def clonelinePrefix(clonelinepath: Any) -> str:
    parts = Path(clonelinepath).parts
    return parts[2].replace("f_", "")


def clonelineClientName(data: Any, p4depot: str) -> str:
    clonelinename = clonelineName(data)
    return clientName(f"{clonelinename}", p4depot)


def clonelineMainClientName(data: Any) -> str:
    clonelinename = clonelineName(data)
    return f"{clonelinename}-main"


# ---------------------------------------------------------
def hwTreeName(data: Any) -> Any:
    # Determine the name of the HW tree from the prefix of the p4hw Crucible ViewTemplate
    view_templates = data.get("view_templates")
    hwtemp = view_templates.get("p4hw")
    for t in hwtemp:
        match = re.search(r"^(\S+)\.\S+", hwtemp[0])
        if match:
            hwtree = match.group(1)
            # printStderr(f"Found HW tree: {hwtree}")
            return hwtree
    # Not found
    printStderr(
        "Warning: HW tree name could not be determined from p4hw view_templates"
    )
    return None


# ---------------------------------------------------------
def latestSnapshot(clonelinename: str, filt: str = "") -> str:
    if filt:
        filtstr = f"-snapshot_filter {filt}"
    else:
        filtstr = ""
    snapshotname = runCmdOutput(
        f"{cloneline_get_info} -cloneline {clonelinename} -latest_snapshot {filtstr}"
    )
    return snapshotname.strip()


def latestSnapshotCFS(clonelinename: str, tag: str = "") -> str:
    if tag:
        tagstr = f"--tag {tag}"
    else:
        tagstr = ""
    snapshotname = runCmdOutput(
        f"{crystal} snapshots --cl {clonelinename} {tagstr} | tail -1"
    )
    return snapshotname.strip()


# ---------------------------------------------------------
def exists(result: Any) -> bool:
    # Returns true if result is nonzero else false
    exists = int(result)
    if exists:
        return True
    else:
        return False


def snapshotExists(clonelinename: str, snapshotname: str) -> bool:
    result = runCmdStdout(
        f"{cloneline_get_info} -cloneline {clonelinename} -latest_snapshot -snapshot_filter {snapshotname} | grep {snapshotname} | wc -l"
    )
    return exists(result)


def snapshotCFSExists(clonelinename: str, snapshotname: str) -> bool:
    result = runCmdStdout(
        f"{crystal} snapshots --cl {clonelinename} --name {snapshotname} | wc -l"
    )
    return exists(result)


def getSnapshotList(clonelinename: str) -> None:
    out = runCmdOutput(f"{clist} {clonelinename} -json")
    out_json = json.loads(out)
    tffs = out_json.get("tffs", {})

    volume_name = next(iter(tffs.keys()), None)

    volume = tffs.get(volume_name, {})

    clonelines = volume.get("clonelines")
    cloneline = clonelines.get(clonelinename)
    snapshot_total = float(cloneline.get("snapshot_disk_usage_total", 0))
    snapshot_max = float(cloneline.get("snapshots_disk_space_GiB_max", 0))

    snapshots = cloneline.get("snapshots", {})

    # soft_max is 80% of max to leave room for clones
    snapshot_max_pct = 0.80
    snapshot_soft_max = snapshot_max * snapshot_max_pct
    print("Snapshot disk usage total: %5.2f" % (snapshot_total))
    print(
        "Snapshot total: %5.2f max:%5.2f max_pct:%.2f soft_max:%5.2f"
        % (snapshot_total, snapshot_max, snapshot_max_pct, snapshot_soft_max)
    )

    # Sort snapshot keys by the 'days_old' field
    sorted_snapshot_keys = sorted(
        snapshots.keys(),
        key=lambda k: int(snapshots[k].get("days_old", 0)),
        reverse=True,
    )

    for snapshot in sorted_snapshot_keys:
        snapshot_info = snapshots.get(snapshot)
        clone_count = int(snapshot_info.get("clone_count", 0))
        days_old = int(snapshot_info.get("days_old"), 0)
        disk_usage = float(snapshot_info.get("disk_usage", 0))

        if snapshot_total < snapshot_soft_max:
            print(
                "Snapshot total size %5.2f is under %d%% of the max %5.2f"
                % (snapshot_total, snapshot_max_pct * 100, snapshot_soft_max)
            )
            break

        if clone_count == 0:
            snapshot_total = snapshot_total - disk_usage
            print(
                "Would remove %s days_old:%s  size:%5.2f new total:%5.2f"
                % (snapshot, days_old, disk_usage, snapshot_total)
            )


def getCloneList(clonelinename: str) -> Any:
    out = runCmdOutput(f"{clist} {clonelinename} -json")
    out_json = json.loads(out)
    tffs = out_json.get("tffs", {})

    volume_name = next(iter(tffs.keys()), None)
    volume = tffs.get(volume_name, {})
    clonelines = volume.get("clonelines")
    cloneline = clonelines.get(clonelinename)
    snapshots = cloneline.get("snapshots", {})

    # Sort snapshots by days_old
    sorted_snapshots = sorted(
        snapshots.keys(),
        key=lambda k: int(snapshots[k].get("days_old", 0)),
        reverse=True,
    )

    clone_dict: Any = {}
    for snapshot in sorted_snapshots:
        snapshot_info = snapshots.get(snapshot)
        clones = snapshot_info.get("clones", {})
        # Sort clones by days_old
        sorted_clones = sorted(
            clones.keys(), key=lambda k: int(clones[k].get("days_old", 0)), reverse=True
        )
        for clone in sorted_clones:
            clone_info = clones.get(clone)
            owner = clone_info.get("owner")
            days_old = int(clone_info.get("days_old"), 0)
            root = f"/home/f_{clonelinename}/c/{clone}"
            # print("%4d %-20s %s" % (days_old, owner, root))

            if owner not in clone_dict.keys():
                clone_dict[owner] = []

            clone_dict[owner].append({"root": root, "days_old": days_old})
            # clone_dict[clone] = { 'root': root, 'owner':owner, 'days_old':days_old }

    return clone_dict


def okToCreateClone(team: str, owner: str, clonelinename: str, clonename: str) -> bool:
    cmd = f"{rule_engine} --json --team {team} run-rules --owner {owner} --cloneline {clonelinename} --clone {clonename}"
    printStderr(cmd)
    out = runCmdOutput(cmd)
    out_json = json.loads(out)
    actions = out_json.get("actions", [])
    general_header = out_json.get("general_header", "")
    message = out_json.get("message", "")
    result_header = out_json.get("result_header", "")

    # If the rule_engine returns a 'create' action, it's OK for this user to create a new clone
    if "create" in actions:
        printStderr("OK to create clone")
        return True
    else:
        rules = out_json.get("rules", [])
        failed_rules = rules.get("failed", [])
        printStderr(result_header)
        for failed_rule in failed_rules:
            name = failed_rule.get("name", "")
            items = failed_rule.get("items", [])
            conditions = failed_rule.get("conditions", [])
            if conditions:
                printStderr(f"Failed rule: {name}")
                for condition in conditions:
                    printStderr("   " + condition)
                printStderr("")
                for item in items:
                    cloneline = item.get("cloneline", "")
                    clone = item.get("clone", "")
                    age = item.get("age", 0)
                    printStderr(
                        f"   clone {clone} in cloneline {cloneline} is {age} days old"
                    )
                printStderr("")
        printStderr(general_header)
        printStderr(message)
        printStderr("NOT OK to create clone")
        return False


def getCloneCount(clonelinename: str, user: str) -> int:
    count = runCmdOutput(
        f"{cloneline_get_info} -cloneline {clonelinename} -user_clone_count -user {user}"
    )
    return int(count.strip())


def listWorkspaces(user: str) -> str:
    return runCmdOutput(f"{workspace_manager} list --user {user}")


def listFilteredWorkspaces(use: str, filt: str, user: str) -> str:
    return runCmdOutput(f"{workspace_manager} list --user {user} | grep {filt}")


# ---------------------------------------------------------
def getTime() -> Any:
    # Return the current timestamp
    timestamp = time.time()
    return timestamp


def getDateTime(timestamp: Any) -> Any:
    tz = currentTZ()
    # Return a datetime object given a timestamp
    dtime = datetime.fromtimestamp(timestamp, tz)
    return dtime


def getLocalTimestamp() -> Any:
    # Return the time for the local timezone
    timestamp = getTime()
    dtime = getDateTime(timestamp)
    timestring = dtime.strftime("%c %Z")
    return (timestamp, timestring)


def getCurrentTimestring() -> Any:
    # Get current time formatted as timestamp string
    dtime = getDateTime(getTime())
    return dtime.strftime("%y%m%d_%H%M%S")


def currentTZ() -> Any:
    if time.daylight:
        return timezone(timedelta(seconds=-time.altzone), time.tzname[1])
    else:
        return timezone(timedelta(seconds=-time.timezone), time.tzname[0])


# ---------------------------------------------------------
def exitWithError(msg: str) -> NoReturn:
    printStderr(f"ERROR: {msg}")
    exit(1)


def exitWithMsg(msg: str) -> None:
    printStderr(msg)
    exit(0)


# ---------------------------------------------------------
def getCfgData(cfg: Any, source: Any) -> Any:
    if cfg and source:
        if Path(cfg).exists():
            config_data = yaml.safe_load(Path(cfg).read_text())
            data = config_data["workspace_source"].get(source)
            if data:
                return data
            else:
                exitWithError(f"cfg {cfg} does not contain source {source}")
        else:
            exitWithError(f"cfg {cfg} does not exist")
    else:
        exitWithError("must provide cfg and source")


def depotPath(base: Any, p4depot: Any) -> Any:
    path = Path(base) / Path(p4depot)
    return path


def mainWorkspaceDepotPath(name: str, p4depot: Any, data: Any) -> Any:
    path = sourcePath(data) / p4depot
    return path


# ---------------------------------------------------------
def getP4PortFromMain(data: Any) -> str:
    # Get flexclone port from main volume
    path = sourcePath(data)
    return getFlexcloneP4Port(path)


def getFlexcloneP4Port(path: Any) -> str:
    # Look for existing .p4config in path
    if os.path.exists(f"{path}/.p4config"):
        # Use the existing port
        p4port = getP4PortFromPath(path)
    else:
        # Call p4mapper
        p4m = P4Mapper.from_uri()
        p4port = str(
            p4m.best_connection_str(specialty="flexclone", port_complex="p4hw")
        )
    return p4port


def getP4Port(data: Any, p4complex: Any) -> str:
    # Get port for p4complex
    path = sourcePath(data)
    return getP4PortFromConfig(path, p4complex)


def getP4PortFromClone(data: Any, clonename: str) -> str:
    # Get the p4port from the clone directory
    path = clonePath(data, clonename)
    p4port = getP4PortFromConfig(path, None)
    return p4port


def getP4PortFromConfig(path: Any, p4complex: Any) -> str:
    if p4complex is not None:
        p4depot = getP4Depot(p4complex)
        cpath = f"{path}/{p4depot}"
    else:
        cpath = path
        p4complex = "p4hw"

    if os.path.exists(f"{cpath}/.p4config"):
        return getP4PortFromPath(cpath)
    else:
        return getP4PortFromMapper(p4complex)


def getP4PortFromPath(path: Any) -> str:
    # Get p4port currently in use under specified path
    p4set = runCmdOutput(f"cd {path} && {p4} set -q P4PORT")
    p4port = p4set.split("=")
    return p4port[1]


def getP4PortFromMapper(p4complex: Any) -> str:
    # Get port from p4mapper
    p4m = P4Mapper.from_uri()
    p4port = str(p4m.best_connection_str(port_complex=p4complex))
    checkP4Ticket(p4port)
    return p4port


# ---------------------------------------------------------
def getP4Depot(p4complex: Any) -> Any:
    p4depot = p4complex.replace("p4", "")
    return p4depot


def createP4Config(clientname: Any, p4port: Any, path: Any, p4user: Any = None) -> None:
    p4config_data = f"P4CLIENT={clientname}\n" + f"P4PORT={p4port}\n"
    if p4user is not None:
        p4config_data += f"P4USER={p4user}\n"
    Path(path / ".p4config").write_text(p4config_data)


def getP4Vars() -> Any:
    cmd = f"{p4} set -q"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p4vars = {}

    if p.stdout is not None:
        for line in p.stdout:
            var, val = line.decode().strip().split("=")
            p4vars[var] = val
    return p4vars


def printVar(var: Any, val: Any) -> None:
    print("%-8s : %s" % (var, val))


# ---------------------------------------------------------
def createMainClient(data: Any) -> None:
    cloneline = clonelineName(data)
    clonelinepath = sourcePath(data)
    flexcloneport = getFlexcloneP4Port(clonelinepath)
    user = os.environ.get("USER")

    # create flexclone main client
    if user is not None:
        wpath = "hw/nv/utils/ghw-nvci/doc"
        wfile = "ghw-nvci.workspace"
        clientname = clonelineMainClientName(data)
        createP4Client(
            flexcloneport,
            clientname,
            user,
            f"main client for the {cloneline} cloneline",
            clonelinepath,
            "View",
            [f"//{wpath}/{wfile}  //{clientname}/{wfile}"],
        )
        createP4Config(clientname, flexcloneport, clonelinepath)
        syncP4Client(clonelinepath, flexcloneport, clientname)


def deleteMainClient(data: Any, force: Any) -> None:
    flexcloneport = getP4PortFromMain(data)
    clientname = clonelineMainClientName(data)
    p4port = getP4PortFromMain(data)
    if clientExists(p4port, clientname):
        deleteP4Client(flexcloneport, clientname)


def deleteMainWorkspace(data: Any, path: Any) -> None:
    # clonelinepath = sourcePath(data)
    # Delete everything except the .clone file
    for root, dirs, files in os.walk(path):
        for d in dirs:
            rmtree(Path(f"{root}/{d}"))
        for f in files:
            if f != ".clone":
                Path(f"{root}/{f}").unlink()


def deleteWorkspaceDir(path: Any) -> None:
    # Delete .workspace dir created by workspace_manager
    wdir = Path(f"{path}/.workspace")
    if wdir.exists():
        printStderr(f"Deleting workspace dir: {wdir}")
        rmtree(wdir)


# ---------------------------------------------------------
def checkP4Ticket(p4port: Any) -> None:
    cmd = f"p4 -p {p4port} "
    p4user = os.environ.get("P4USER") or os.environ.get("USER")
    if p4user:
        cmd += f"-u {p4user} "
    cmd += "login -s"
    cp = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    out = cp.stdout.decode().strip()
    status = cp.returncode
    printStderr(out)

    if status:
        exitWithError(
            f"P4 ticket for {p4user} P4PORT={p4port} is NOT valid!  Please login with:\n"
            f"    p4 -p {p4port} login -a"
        )
    else:
        printStderr(f"P4 ticket for {p4user} P4PORT={p4port} is valid.")


def createP4Client(
    p4port: Any,
    clientname: Any,
    owner: Any,
    description: Any,
    root: Any,
    viewtype: Any,
    view: Any,
) -> None:
    options = "noallwrite clobber nocompress unlocked nomodtime rmdir noaltsync"
    clientspec = (
        f"Client: {clientname}\n"
        + f"Owner: {owner}\n"
        + f"Description: {description}\n"
        + f"Root: {root}\n"
    )

    if options:
        clientspec += f"Options: {options}\n"

    clientspec += f"{viewtype}:\n"
    for v in view:
        clientspec += f"\t{v}\n"

    cfile = ".clientspec"
    Path(cfile).write_text(clientspec)
    runCmdOutput(f"{p4} -p {p4port} client -i < {cfile}")
    Path(cfile).unlink(missing_ok=True)


def syncP4Path(path: Any, cl: Any = 0) -> None:
    clopt = ""
    if cl:
        clopt = "@" + str(cl)
    runCmdOutput(f"cd {path} && {p4} sync {clopt} > p4sync.log")


def syncP4Client(path: Any, p4port: Any, clientname: Any) -> None:
    runCmdOutput(f"cd {path} && {p4} -p {p4port} -c {clientname} sync > p4sync.log")


def revertP4Client(p4port: Any, clientname: Any) -> None:
    runCmdOutput(f"{p4} -p {p4port} -c {clientname} revert //...")


def deleteP4Client(p4port: Any, clientname: Any) -> None:
    runCmdOutput(cmd=f"{p4} -p {p4port} client -d {clientname}", warnings_only=True)


def revertOpenFiles(p4port: Any, depotpath: Any, clientname: str) -> None:
    # revert any files files open for edit
    runCmdOutput(cmd=f"cd {depotpath} && {p4} -p {p4port} revert -k //...")


def clientExists(p4port: Any, clientname: str) -> bool:
    # Verify that the client exists
    result = runCmdOutput(f"{p4} -p {p4port} clients -e {clientname}")
    if result.splitlines():
        return True
    else:
        return False


def clientIsSafeToDelete(p4port: Any, clientname: str) -> bool:
    # Verify no files are open
    opened = runCmdStderr(f"{p4} -p {p4port} opened -C {clientname}")
    notopen = re.search("not opened", opened)

    # Verify no shelved changes
    result = runCmdOutput(f"{p4} -p {p4port} changes -c {clientname} -s shelved")
    shelved_changes = [line.split()[1] for line in result.splitlines() if line]

    if notopen and not shelved_changes:
        return True
    else:
        return False


def deleteShelves(p4port: Any, depotpath: Any, clientname: str) -> None:
    # Delete shelves and pending changelists
    result = runCmdOutput(cmd=f"{p4} -p {p4port} changes -c {clientname} -s shelved")
    shelved_changes = [line.split()[1] for line in result.splitlines() if line]
    for change in shelved_changes:
        runCmdOutput(cmd=f"cd {depotpath} && {p4} -p {p4port} shelve -d -c {change}")
        runCmdOutput(cmd=f"cd {depotpath} && {p4} -p {p4port} change -d {change}")


def revertAndDeleteP4Client(p4port: Any, depotpath: Any, clientname: str) -> None:
    # Safely revert then delete p4 client
    if depotpath.exists():
        printStderr(f"Revert open files for p4 client {clientname}")
        revertOpenFiles(p4port, depotpath, clientname)
        printStderr(f"Delete shelves for p4 client {clientname}")
        deleteShelves(p4port, depotpath, clientname)

    if clientExists(p4port, clientname):
        if clientIsSafeToDelete(p4port, clientname):
            printStderr(f"Deleting client: {clientname}")
            deleteP4Client(p4port, clientname)
        else:
            exitWithError(f"Cannot delete client {clientname}")
    else:
        printStderr(f"Skipping delete of non-existent p4 client {clientname}")


def syncP4Metadata(path: Any, p4port: Any, clientname: str, revision: Any) -> None:
    # Sync metadata only to match clone revision
    runCmdOutput(
        f"cd {path} && {p4} -p {p4port} -c {clientname} sync -k @{revision} > p4syncmeta.log"
    )


def snapshotMain(data: Any, snapshotname: str) -> None:
    p4port = getP4PortFromMain(data)
    clientname = clonelineMainClientName(data)
    runCmdOutput(f"{p4} -p {p4port} _clone -snapshot {clientname} {snapshotname}")


def deleteSnapshot(data: Any, snapshotname: str) -> None:
    clonelinename = clonelineName(data)
    runCmdOutput(f"{flexcl} --cloneline {clonelinename} delete -s {snapshotname}")


def deleteClone(clonename: str, p4port: Any) -> None:
    runCmdOutput(f"{p4} -p {p4port} _clone -d {clonename}")


def createClone(data: Any, snapshotname: str, clonename: str) -> str:
    p4port = getP4PortFromMain(data)
    out = runCmdOutput(f"{p4} -p {p4port} _clone {snapshotname} {clonename}")
    clonepath = out.split(" @ ", 1)[1].strip()
    return clonepath


def pathP4Revision(path: Any) -> Optional[str]:
    # Get client revision for cwd client
    revision = runCmdOutput(f"cd {path} && {p4} _revision --fullSync")
    match = re.search(r"revision: (\d+)", revision)
    if match:
        return match.group(1)
    else:
        exitWithError(f"no p4 revision found for path {path}")


def updateSyncCl(path: Any) -> Any:
    # Check revision and update .sync_cl file
    sync_cl = pathP4Revision(path)
    writeSyncCl(path, sync_cl)
    return sync_cl


def writeSyncCl(path: Any, sync_cl: Any) -> Any:
    # write directly to .sync_cl file
    sync_cl_file = Path(path) / ".sync_cl"
    sync_cl_file.write_text(sync_cl)
    return sync_cl


def getSyncCl(path: Any) -> Any:
    # Read .sync_cl file
    sync_cl_file = Path(path) / ".sync_cl"
    if sync_cl_file.exists():
        sync_cl = sync_cl_file.read_text()
        return sync_cl
    else:
        printStderr(f"WARNING: {sync_cl_file} not found")
        return None


def clientP4Revision(p4port: Any, clientname: str) -> str:
    revision = runCmdOutput(f"{p4} -p {p4port} _revision --fullSync {clientname}")
    # printStderr(revision)
    match = re.search(r"revision: (\d+)", revision)
    if match:
        return match.group(1)
    else:
        exitWithError(f"no p4 revision found for client {clientname}")


def codepSWCl(p4hw_cl: str, tag: str) -> str:
    p4sw_cl = runCmdOutput(
        f"{nvctdb} get_limits --lower --cl p4hw={p4hw_cl} --server p4sw --tag {tag}"
    )
    return p4sw_cl.strip()


def getRevisionString(data: Any) -> str:
    view_templates = data.get("view_templates")
    rev = []
    for p4complex in view_templates:
        p4port = getP4Port(data, p4complex)
        p4depot = getP4Depot(p4complex)
        clientname = clonelineClientName(data, p4depot)
        revision = clientP4Revision(p4port, clientname)
        rev.append(f"{p4depot}{revision}")
    return "_".join(rev)


def extractP4Revision(name: str, p4depot: str) -> Optional[str]:
    # Extract the revision CL from the given name for the specified p4depot
    match = re.search(p4depot + r"(\d+)", name)
    if match:
        cl = match.group(1)
        return cl
    else:
        return None


def nvciEnvWorkingDir(name: str, source: str) -> Path:
    # Set path to nvci-env working_dir
    homedir = Path.home()
    envdir = f"{source}/{name}"
    wd = Path(homedir, "nvci-env", envdir)
    wd.mkdir(parents=True, exist_ok=True)

    if wd.exists:  # type: ignore
        printStderr(f"Created nvci-env working dir {wd}")
        return wd
    else:
        exitWithError(f"nvci-env working dir {wd} does not exist")


def nvciEnvDir() -> Path:
    homedir = Path.home()

    wd = Path(f"{homedir}/nvci-env")

    wd.mkdir(parents=True, exist_ok=True)

    if wd.exists:  # type: ignore
        printStderr(f"Created nvci-env dir {wd}")
        return wd
    else:
        exitWithError(f"nvci-env dir {wd} does not exist")


def logDeleteTime(path: Any) -> None:
    # Log time of deletion to ~/nvci-env/delete.log
    user = os.environ.get("USER")
    (timestamp, timestring) = getLocalTimestamp()
    env_dir = nvciEnvDir()
    delete_logfile = f"{env_dir}/delete.log"
    line = f"{timestring} : {user} deleted {path}"
    with open(delete_logfile, "a") as file:
        file.write(line + "\n")


# ---------------------------------------------------------
def getNvciEnv(key: Any, wd: Any = "~/nvci-env") -> Union[None, str, bool]:
    # Get value from nvci environment
    val = runCmdOutput(f"nvci-env --working-dir {wd} get {key}")

    # Return true/false for boolean values
    if val == "true":
        return True
    elif val == "false":
        return False
    elif val == "null":
        return None
    else:
        return val


# ---------------------------------------------------------
def createPatchCloneFile(data: Any) -> None:
    cwd = Path.cwd()
    workspacepath = sourcePath(data)

    tot_dirs = data.get("tot_dirs")
    if not tot_dirs:
        tot_dirs = ["hw/" + hwTreeName(data)]

    patch_clone_paths = "bin/tmakelibs/patch_clone_paths.pl"

    patch_cmds = []
    afiles = ""
    for tdir in tot_dirs:
        ptdir = workspacepath / tdir
        os.chdir(ptdir)
        # Look for abspath_list.txt files in .tmake* directories
        for directory in Path(".").iterdir():
            if directory.name.startswith(".tmake"):
                afile = directory / "abspath_list.txt"
                if afile.is_file():
                    afiles = afiles + " " + str(afile)
        os.chdir(cwd)
        if afiles:
            patch_cmds.append(
                f"(cd {tdir} && cat {afiles} | sort -u > .abspath_full.txt && {patch_clone_paths} -filelist .abspath_full.txt )"
            )

    if patch_cmds:
        # Write .patch_clone script
        Path(workspacepath / ".patch_clone").write_text("\n".join(patch_cmds) + "\n")


def patchClone() -> None:
    cwd = Path.cwd()
    if Path(cwd / ".patch_clone").exists():
        printStderr("Patching abs paths in clone")
        runCmdOutput("sh .patch_clone > patch_clone.log")


# ---------------------------------------------------------
def validate_cl(ctx: Any, param: Any, value: Any) -> Any:
    sync_cl = {}
    for v in value:
        match = re.search(r"(\D+)(\d+)", v)
        if match:
            sync_cl[match.group(1)] = match.group(2)
        else:
            raise click.BadParameter(
                "--cl options should look like 'hw1234567' or 'sw7654321'"
            )
    return sync_cl


# ---------------------------------------------------------
def getGoldenCL(customer: Any, type: Any) -> Any:
    gcl = runCmdOutput(
        f"{golden_cl} get --customer {customer} --type {type}", warnings_only=True
    )
    if gcl:
        return gcl
    else:
        return 0


def getTOTRulesCL() -> str:
    # In order to query the rules CL of the live AS2 DB, run from a host at SC
    rcl = runCmdOutput(f"ssh cadbuild-05 {rules_cl} --simple")
    return rcl


# ---------------------------------------------------------
def runCmd(cmd: str) -> None:
    # run shell command; redirect stdout to stderr
    if debug:
        printStderr(cmd)
    output = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    print(output.stdout.decode(), file=sys.stderr, end="")
    print(output.stderr.decode(), file=sys.stderr, end="")


# ---------------------------------------------------------
def runCmdOutput(cmd: str, warnings_only: bool = False) -> str:
    if debug:
        printStderr(cmd)

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode:
        if result.stdout:
            printStderr(result.stdout)
        if result.stderr:
            printStderr(result.stderr)

        if warnings_only:
            # Treat errors as warnings
            printStderr(
                f"Warning: Command '{cmd}' failed with status {result.returncode} (ignored)"
            )
        else:
            if debug:
                result.check_returncode()
            else:
                printStderr(
                    f"ERROR: Command '{cmd}' failed with status {result.returncode}"
                )
                exit(result.returncode)

    return result.stdout.strip()


def runCmdStdout(cmd: str) -> str:
    # run shell command and return stdout only
    if debug:
        printStderr(cmd)
    output = subprocess.check_output(cmd, shell=True)
    return output.decode()


def runCmdStderr(cmd: str) -> str:
    # run shell command and return stdout/stderr
    if debug:
        printStderr(cmd)
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    out = output.decode().strip()
    return out


def printStderr(msg: str) -> None:
    print(msg, file=sys.stderr)


# ---------------------------------------------------------
def isCrystalHost() -> bool:
    try:
        # Run the command `crystal help` and capture the output and error
        # Allow the command to fail with a non-zero exit code
        result = subprocess.run(
            [crystal, "help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        # Check if the specific error message is in the standard error output
        if (
            "ERROR: This machine does not support running crystal commands"
            in result.stderr
        ):
            return False
        else:
            return True
    except FileNotFoundError:
        # Handle the case where the `crystal` command is not found
        return False


def checkCrystalHost() -> None:
    if isCrystalHost():
        printStderr("Running on a crystal-enabled host")
    else:
        exitWithError("Must run on a crystal-enabled host")


def createCrystalQsubenv(path: Any = ".") -> None:
    # Create a .qsubenv file that will ensure qsub jobs will run on crystal hosts
    runCmd(f"cd {path} && echo 'QSUB_SELECT_UPDATE: crystal' > ./.qsubenv")


def isCFS(path: Any) -> Any:
    return re.search(r"^\/crystal\/", str(path))


def checkCFSExists(cfsname: str) -> bool:
    result = runCmdStdout(f"{crystal} cfss --name {cfsname} | wc -l")
    return exists(result)


def checkCFSBound(cfsname: str) -> Any:
    result = runCmdStdout(f"{crystal} --json cfs -o {cfsname}")
    result_json = json.loads(result)
    message = result_json.get("message")
    bound = message.get("Bound p4 clients", "")
    return bound


def checkCFSClonelineExists(cloneline: str) -> bool:
    result = runCmdStdout(f"{crystal} clonelines --name {cloneline} | wc -l")
    return exists(result)


def createCFSCloneline(cloneline: str) -> None:
    if not checkCFSClonelineExists(cloneline):
        runCmdStdout(
            f"{crystal} cloneline --description '{cloneline} cloneline' {cloneline}"
        )


def getCFSPath(cfsname: str) -> Path:
    return Path(f"/crystal/{cfsname}")


def createCFS(cfsname: str, group: str) -> None:
    runCmdStdout(f"{crystal} cfs {crystal_opts} -g {group} {cfsname}")


def createCFSClone(snapshotname: str, clonename: str, group: str) -> None:
    runCmd(f"{crystal} cfs {crystal_opts} -s {snapshotname} {clonename}")


def createCFSCloneFromCloneline(
    cloneline: str, clonename: str, group: str, tag: str = ""
) -> None:
    cmd = f"{crystal} cfs {crystal_opts} --cl {cloneline}"
    if tag:
        cmd += f" --snapshot_tag {tag}"
    cmd += f" {clonename}"
    runCmd(cmd)


def bindCFS(cfsname: str, p4port: Any, suffix: str) -> None:
    runCmd(f"{crystal} cfs --p4_bind_suffix {p4port},{suffix} {cfsname}")


def deleteCFS(cfsname: str) -> None:
    os.chdir("/tmp")
    runCmd(f"{crystal} cfs -f -d {cfsname}")


def tagCFS(snapshotname: str, tag: str) -> None:
    runCmd(f"{crystal} snapshot --tag {tag} {snapshotname}")


def createNewCFSCloneline(clonelinename: str) -> None:
    runCmd(f"{crystal} cloneline {clonelinename}")


def addSnapshotToCFSCloneline(snapshotname: str, clonelinename: str) -> None:
    runCmd(f"{crystal} cloneline --add {snapshotname} {clonelinename}")


def snapshotCFS(cfsname: str, snapshotname: str, tag: str = "") -> Path:
    if tag:
        tagstr = f" --tag {tag}"
    else:
        tagstr = ""

    (timestamp, snaptime) = getLocalTimestamp()
    dstr = f" --description 'Snapshot created on {snaptime} ({timestamp})'"

    runCmd(
        f"{crystal} snapshot -c {cfsname}{tagstr}{dstr} --exempt_active_mounts {snapshotname}"
    )
    return getCFSPath(snapshotname)


# ---------------------------------------------------------
# def createStorageCFR(tree):
#    tf = FF(test_name='cfrtest',config_path=".")
#    storage = tf.create_storage(active_trees=tree)
#    return storage


def getGroup(data: Any) -> Any:
    return data.get("security_group")


# ---------------------------------------------------------
def getNamespaceContent(data: Any) -> list:
    namespaces = data.get("conman_download")
    conmandir = Path.cwd() / "conman"
    conman_paths = []
    if namespaces:
        for path in namespaces:
            (namespace, version) = conman.path_version(path)
            downloaded_version = conman.download_desired_version(
                namespace, conmandir, True, version
            )
            conman_paths.append(path + "@" + downloaded_version)
        # Link conman Makefile for convenience in updating Content Manager directly from the workspace
        runCmd(
            f"cd {conmandir} && ln -f -s /home/nv/utils/ghw-nvci/latest/conman/Makefile ."
        )
    return conman_paths


# ---------------------------------------------------------
def getSite() -> str:
    perl = "/home/utils/perl-5.24/5.24.2-005/bin/perl"
    sitecmd = "use lib '/home/nv/lib/perl5'; use NV::Site qw(); print NV::Site::site();"
    site = runCmdOutput(perl + " -e " + '"' + sitecmd + '"')
    return site.strip()


# ---------------------------------------------------------
def createProjectTeamFile(path: Any, project_team: str) -> None:
    runCmdOutput(
        f"cd {path} && {projectname} -noresolve -novalidate -project_team {project_team}"
    )


def getProjectTeam(path: Any) -> Optional[str]:
    # resolve the nvprojectname, and return the PROJECT_TEAM
    projectname = runCmdOutput(f"cd {path} && {nvprojectname} resolve")
    # the PROJECT_TEAM is everything after the second underscore
    parts = projectname.split("_", 2)
    if len(parts) >= 3:
        return parts[2]

    else:
        return None


def resolveProjectName() -> str:
    pnqs = (
        "https://confluence.nvidia.com/display/GPUTree/GPU+Project+Naming+Quick+Start"
    )
    pnerror = f"Please setup project naming in this directory by following these instructions:\n{pnqs}"

    projectname = runCmdOutput(f"{nvprojectname} resolve")
    if projectname:
        isRegistered = runCmdOutput(f"{nvprojectname} is_registered {projectname}")
        if isRegistered != "0":
            return projectname
        else:
            exitWithError(f"Project name '{projectname}' is not registered.\n{pnerror}")
    else:
        exitWithError(f"Project name is not defined.\n{pnerror}")


def setDefaultProjectName(path: Any, projectname: str) -> None:
    runCmdOutput(f"cd {path} && {nvprojectname} save_default . {projectname}")


def setProjectTeam(path: Any, project_team: str) -> None:
    # If the tree.make file exists, update or add the specified PROJECT_TEAM to it
    filename = f"{path}/tree.make"

    if not os.path.exists(filename):
        return

    # Read tree.make
    with open(filename, "r") as file:
        lines = file.readlines()

    # Look for the PROJECT_TEAM
    index = None
    for i, line in enumerate(lines):
        if line.startswith("PROJECT_TEAM"):
            index = i
            break

    # Create or modify the PROJECT_TEAM
    if index is not None:
        lines[index] = f"PROJECT_TEAM := {project_team}\n"
    else:
        lines.append(f"PROJECT_TEAM := {project_team}\n")

    # Write the lines back to tree.make
    with open(filename, "w") as file:
        file.writelines(lines)

    # Run projectteam to create .nvprojectname file from PROJECT_TEAM
    runCmdOutput(f"cd {path} && nvrun projectteam")


# ---------------------------------------------------------
def createManifest(root: Any, mdata: Any, state: Any) -> None:
    (timestamp, timestring) = getLocalTimestamp()
    user = os.environ.get("USER")
    site = getSite()
    command = os.path.abspath(sys.argv[0]) + " " + " ".join(sys.argv[1:])
    manifest = {
        "command": command,
        "site": site,
        "state": state,
        "timestamp": timestamp,
        "timestring": timestring,
        "user": user,
        "workspace": mdata,
    }

    moveManifest(root)
    mfile = f"{root}/{manifest_file}"
    with open(mfile, "w") as file:
        yaml.dump(manifest, file)


def newManifestWorkspaceData() -> dict:
    mdata: dict = {
        "name": None,
        "path": None,
        "source": None,
        "tags": {},
        "sync_cls": {},
    }
    return mdata


def getManifestWorkspaceData() -> Any:
    manifest = readManifest()
    if manifest is not None:
        mdata = manifest["workspace"]
        return mdata
    else:
        return newManifestWorkspaceData()


def moveManifest(root: Any) -> None:
    # if manifest.yml already exists move it
    mfile = f"{root}/{manifest_file}"
    nfile = f"{root}/manifest.prev.yml"
    if os.path.isfile(mfile):
        os.rename(mfile, nfile)


def readManifest() -> Any:
    mfile = findFileUpwards(manifest_file)

    if mfile and os.path.isfile(mfile):
        with open(mfile, "r") as file:
            manifest = yaml.safe_load(file)
        return manifest
    else:
        return None


def pathFromManifest(data: Any) -> Any:
    mdata = getManifestWorkspaceData()
    path = mdata.get("path", None)
    if path is not None:
        setPath(data, path)
        return path
    else:
        path = Path.cwd()
        printStderr(f"WARNING path not found in manifest.yml; returning cwd: {path}")
        return path


def setManifestState(root: Any, state: Any) -> None:
    # Update state in existing manifest
    mdata = getManifestWorkspaceData()
    createManifest(root, mdata, state)


def getManifestState() -> Any:
    manifest = readManifest()
    if manifest is not None:
        return (manifest["state"], manifest["timestamp"])
    else:
        return ("empty", 0)


def cleanupLogs(path: Any) -> None:
    # Cleanup logfiles
    runCmdOutput(
        f"cd {path} && rm -rf TASK.*.out nvci.*.log waiver_manager.*.log core.* *extra_archive_flags cat_task_name* extra_launch_ss_options a.out diag/testgen/results/* diag/testgen/batch_*_fmodel_*"
    )


def cleanupManifest(path: Any) -> None:
    # Cleanup old manifest files that are in the wrong place
    runCmdOutput(f"cd {path} && rm -rf manifest.*")


def verifyNvciYmlExists(path: Any) -> None:
    # Verify nvci.yml exists in the specified directory
    nvci_yml = f"{path}/nvci.yml"
    if Path(nvci_yml).exists():
        printStderr(f"Found nvci.yml at {nvci_yml}")
    else:
        exitWithError(f"Did NOT find nvci.yml at {nvci_yml}")


# ---------------------------------------------------------
def readYamlFile(yfile: Any) -> Any:
    if Path(yfile).exists():
        with open(yfile, "r") as file:
            struct = yaml.safe_load(file)
    else:
        struct = {}
    return struct


def writeYamlFile(yfile: str, struct: Any) -> None:
    # Write new status to the file
    with open(yfile, "w") as file:
        yaml.dump(struct, file)


# ---------------------------------------------------------
def findFileUpwards(filename: str) -> Any:
    current_dir = os.getcwd()

    while True:
        potential_path = os.path.join(current_dir, filename)
        if os.path.isfile(potential_path):
            return os.path.abspath(potential_path)

        parent_dir = os.path.dirname(current_dir)
        if current_dir == parent_dir:  # Reached the root directory
            break

        current_dir = parent_dir

    return None
