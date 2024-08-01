#!/usr/bin/env python3

# import re
import os
from pathlib import Path
from typing import Any, Dict

import click

from ghwnvci import conman
from ghwnvci import workspace_utils as util

# from IPython.lib.pretty import pretty
# from cfr.flow_fixture import FlowFixture as FF

workspace_manager = "workspace_manager"
nvci = "nvci"

localpath = os.environ.get("LOCAL_GHW_NVCI")
conman_path = f"{localpath}/conman"


# ---------------------------------------------------------
@click.group()
def cli() -> None:
    pass


# ---------------------------------------------------------
# @cli.command()
# @click.argument("source", required=True)
# @click.option("--name", required=False)
# @click.option("--local", is_flag=True)
# def new(name, source, local):
#     workspacepath = newWorkspace(name, source, local)
#     print(workspacepath)


# @cli.command()
# @click.argument("source", required=True)
# @click.option("--name", default="auto", required=False)
# def create(source, name):
#     workspacepath = nvciCreate(name, source)
#     print(workspacepath)


@cli.command()
@click.option("--team", required=False, default="gcs", help="Team for rule_engine")
@click.option(
    "--owner", required=False, default=os.environ.get("USER"), help="owner of clone"
)
@click.option("--cloneline", required=True, help="cloneline name")
@click.option("--clone", required=False, default="testclone", help="clone name")
def runrules(team: str, owner: str, cloneline: str, clone: str) -> None:
    ok = util.okToCreateClone(team, owner, cloneline, clone)
    if not ok:
        util.exitWithError("Unable to create a new workspace")


@cli.command()
@click.argument("workspacepath", required=False)
def delete(workspacepath: str) -> None:
    if workspacepath:
        util.wmDelete(workspacepath)  # type: ignore
    else:
        util.wmDelete(Path.cwd())  # type: ignore


@cli.command()
@click.argument("workspacepath", required=False)
def snap(workspacepath: str) -> None:
    print(workspacepath)


# ---------------------------------------------------------
@cli.command()
@click.argument("regex", required=False)
def last(regex: str) -> None:
    workspace = lastWorkspace(regex)
    print(workspace)


# ---------------------------------------------------------
@cli.command()
@click.argument("cloneline", required=True)
def snapshots(cloneline: str) -> None:
    util.getSnapshotList(cloneline)


# ---------------------------------------------------------
@cli.command()
def nagclones() -> None:
    clonelines = [
        "nvgpu_pdx_gcs_3",
        "nvgpu_pdx_gcs_4",
        "nvgpu_sc_gcs_9",
        "nvgpu_sc_gcs_10",
    ]
    # 'nvgpu_pdx_gcs_5', 'nvgpu_pdx_gcs_6', 'nvgpu_pdx_gcs_7', 'nvgpu_pdx_gcs_8',
    nag_clones: Dict[Any, Any] = {}

    for cloneline in clonelines:
        clone_dict = util.getCloneList(cloneline)
        nag_clones = merge_dicts(nag_clones, clone_dict)

    for owner in nag_clones.keys():
        print(owner)
        clone_list = nag_clones[owner]
        for clone in clone_list:
            days_old = clone["days_old"]
            if days_old > 14:
                print("%4d %s" % (days_old, clone["root"]))


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    merged_dict = {}
    for key in set(dict1.keys()).union(dict2.keys()):
        values = []
        if key in dict1:
            values.append(dict1[key])
        if key in dict2:
            values.append(dict2[key])
        merged_dict[key] = values if len(values) > 1 else values[0]
    return merged_dict


# @cli.command()
# @click.argument("source", required=True)
# @click.option("--local", is_flag=True)
# def hwtree(source, local):
#     cfg = getCfg(source, local)
#     data = util.getCfgData(cfg, source)
#     hwtreename = util.hwTreeName(data)
#     print(hwtreename)


@cli.command()
def vars() -> None:
    p4vars = util.getP4Vars()
    pvars = ["P4USER", "P4PORT", "P4CLIENT", "P4ROOT"]
    for pvar in pvars:
        val = p4vars.get(pvar)
        util.printVar(pvar, val)


# @cli.command()
# def cfrtest():
#    tf = FF(test_name='cfrtest',config_path=".")
#    print(pretty(tf))
# storage = tf.create_storage(active_trees="nvgpu_training")
# storage.p4_sync()


@cli.command()
def conman_namespaces() -> None:
    conman.list_namespaces()


@cli.command()
@click.argument("namespace", required=True)
def conman_list_content(namespace: str) -> None:
    conman.list_content(namespace)


@cli.command()
@click.argument("namespace", required=True)
def conman_latest(namespace: str) -> None:
    print(conman.latest_published(namespace))


@cli.command()
@click.argument("namespace", required=True)
@click.argument("version", default="latest")
def conman_download(namespace: str, version: str) -> None:
    conmandir = Path.cwd() / "conman"
    conman.download_desired_version(namespace, conmandir, True, version)


@cli.command()
@click.argument("namespace", required=True)
@click.argument("incr", default="none")
def conman_upload(namespace: str, incr: str) -> None:
    conman.publish_content(namespace, incr)


@cli.command()
@click.argument("namespace", required=True)
@click.argument("incr", default="patch")
def next_version(namespace: str, incr: str) -> None:
    curr_version = conman.latest_published(namespace)
    if curr_version:
        next_version = conman.increment_version(curr_version, incr)
    else:
        next_version = "0.0.1"
    print(next_version)


@cli.command()
def site() -> None:
    site = util.getSite()
    print(site)


# ---------------------------------------------------------
@cli.command()
@click.argument("path", required=True)
def p4Revision(path: str) -> None:
    print(util.pathP4Revision(path))


# ---------------------------------------------------------
@cli.command()
@click.argument("cltype", default="p4hw")
def synccl(cltype: str) -> Any:
    synccl = None
    mdata = util.getManifestWorkspaceData()
    synccls = mdata.get("sync_cls")
    if synccls:
        synccl = synccls.get(cltype, None)
        print(f"{cltype} sync cl= {synccl}")
    return synccl


# ---------------------------------------------------------
@cli.command()
@click.option("--customer", default="nvgpu")
@click.option("--type", default="hw")
def gold(customer: str, type: str) -> None:
    cl = int(util.getGoldenCL(customer, type))
    print(f"golden_cl for customer {customer} type {type} = {cl}")


# ---------------------------------------------------------
@cli.command()
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.option("--source", required=True, help="Workspace source type")
def patch(cfg: str, source: str) -> None:
    data = util.getCfgData(cfg, source)
    workspacepath = util.sourcePath(data)
    print(f"Creating patch file for {workspacepath}...")
    util.createPatchCloneFile(data)
    print("done.")


# ---------------------------------------------------------
def workspace_source(namespace: str, wm_path: str) -> str:
    return f"{conman_path}/{namespace}/{wm_path}/workspace_source.yml"


def wmNew(tree: str) -> str:
    source = tree + "_main"
    name = tree + "_mainline"
    namespace = "ghw-nvci"
    wm_path = f"tree/{tree}/wm"
    cfg = workspace_source(namespace, wm_path)
    out = util.runCmdOutput(
        f"{workspace_manager} new --name {name} --source {source} --file_definition {cfg}"
    )
    return out


def wmDelete(workspacepath: str) -> None:
    util.runCmd(f"{workspace_manager} delete -d {workspacepath}")


# def newWorkspace(namespace, source):
#    tree = "nvgpu"
#    name = "blah"
#    wm_path = f"tree/{tree}/wm"
#    cfg = workspace_source(namespace, wm_path)
#
#    out = util.wmNew(name, source, cfg)
#    match = re.search("Workspace available at (\S+)", out)
#    if match:
#        workspacepath = match.group(1)
#        return workspacepath
#    else:
#        util.exitWithError(f"workspace_manager returned {out}")


# ---------------------------------------------------------


# def nvciCreate(name, source):
#     config = source2config.get(source)
#     cmd = f"{nvci} create {config} --name {name} --source {source}"
#     out = util.runCmdOutput(cmd)
#     match = re.search("Created workspace at (\S+)", out)
#     if match:
#         workspacepath = match.group(1)
#         return workspacepath
#     else:
#         util.exitWithError(f"nvci create exited with {out}")


def lastWorkspace(regex: str = "") -> str:
    cmd = f"{util.workspace_manager} list"
    if regex:
        cmd += f" | grep {regex}"
    cmd += " | tail -1"
    # print(cmd)
    out = util.runCmdOutput(cmd)
    return out.strip()


# ---------------------------------------------------------
if __name__ == "__main__":
    cli()
