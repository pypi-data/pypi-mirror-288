#!/usr/bin/env python3

import os
import sys
from shutil import rmtree
from typing import Any

import click

from ghwnvci import workspace_utils as util


# ---------------------------------------------------------
@click.group()
def cli() -> None:
    pass


# ---------------------------------------------------------
# Create main workspace
# ---------------------------------------------------------
@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.pass_context
def create_main(ctx: click.Context, name: str, source: str, cfg: str) -> None:
    # Flexclone create_main
    create_main_workspace(ctx, name, source, cfg, False)


@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.pass_context
def create_mainCFS(ctx: click.Context, name: str, source: str, cfg: str) -> None:
    # Crystal create_main
    util.checkCrystalHost()
    create_main_workspace(ctx, name, source, cfg, True)


def create_main_workspace(
    ctx: click.Context, name: str, source: str, cfg: str, use_crystal: bool
) -> None:
    data = util.getCfgData(cfg, source)

    # Determine if main volume should be deleted first
    delete_main_before_create = data.get("delete_main_before_create", False)

    # Resolve the nvproject name
    projectname = util.resolveProjectName()
    util.printStderr(f"resolved projectname = {projectname}")

    # Determine main workspace dir
    if use_crystal:
        cloneline = data.get("cloneline", "")
        if cloneline:
            if util.checkCFSClonelineExists(cloneline):
                util.printStderr(f"Using CFS cloneline {cloneline}")
            else:
                util.exitWithError(
                    f"CFS cloneline {cloneline} does not exist! Please create it with 'crystal cloneline {cloneline}'"
                )

        cfsname = util.mainCFSName(data, name)
        workspacepath = util.getCFSPath(cfsname)
        util.setPath(data, workspacepath)
        group = util.getGroup(data)
    else:
        workspacepath = util.sourcePath(data)

    if use_crystal:
        if delete_main_before_create and util.checkCFSExists(cfsname):
            util.printStderr(f"Deleting existing CFS workspace at {workspacepath}")
            ctx.forward(delete_mainCFS)

        if util.checkCFSExists(cfsname):
            util.printStderr(f"Using existing CFS workspace at {workspacepath}")
        else:
            util.printStderr(f"Creating new CFS workspace at {workspacepath}")
            util.createCFS(cfsname, group)
            util.createCrystalQsubenv(workspacepath)
    else:
        if workspacepath.exists():
            if delete_main_before_create:
                util.printStderr(f"Deleting existing workspace at {workspacepath}")
                ctx.forward(delete_main)
            else:
                util.printStderr(f"Using existing workspace at {workspacepath}")
        else:
            util.printStderr(f"Creating new workspace at {workspacepath}")
            workspacepath.mkdir(parents=True)

    # Delete any existing .workspace directory from the main volume
    util.deleteWorkspaceDir(workspacepath)

    # Create a .nvprojectname_default file at the top of the main workspace
    util.setDefaultProjectName(workspacepath, projectname)

    # Create new manifest
    mdata = util.newManifestWorkspaceData()
    mdata["name"] = name
    mdata["path"] = str(workspacepath)
    mdata["source"] = source
    os.chdir(workspacepath)
    util.createManifest(workspacepath, mdata, "created")

    print(workspacepath)


# ---------------------------------------------------------
# Setup main workspace
# ---------------------------------------------------------
@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
def setup_main(name: str, source: str, cfg: str) -> None:
    # Flexclone setup_main
    setup_main_workspace(name, source, cfg, False)


@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
def setup_mainCFS(name: str, source: str, cfg: str) -> None:
    # Crystal setup_main
    util.checkCrystalHost()
    setup_main_workspace(name, source, cfg, True)


def setup_main_workspace(name: str, source: str, cfg: str, use_crystal: bool) -> None:
    data = util.getCfgData(cfg, source)
    workspacepath = util.pathFromManifest(data)

    user = os.environ.get("USER")
    nvci_env_wd = util.nvciEnvWorkingDir(name, source)
    pickcl = util.getNvciEnv("ghw-nvci.pickcl", nvci_env_wd)

    mdata = util.getManifestWorkspaceData()
    mdata["name"] = name
    mdata["source"] = source
    mdata["path"] = str(workspacepath)
    mdata["conman_namespaces"] = util.getNamespaceContent(data)

    # Cleanup logs in main
    util.cleanupLogs(workspacepath)

    if util.isFlexclone(data):
        util.createMainClient(data)

    # Create new crucible clients in the workspace for the specified complex(es)
    view_templates = data.get("view_templates")
    for p4complex in view_templates:
        p4port = util.getP4Port(data, p4complex)
        p4depot = util.getP4Depot(p4complex)

        if use_crystal:
            cfsname = util.CFSNameFromPath(workspacepath)
            clientname = util.clientName(cfsname, p4depot)
        else:
            clientname = util.clonelineClientName(data, p4depot)

        util.printStderr(f"Creating {p4depot} client {clientname}")
        util.createP4Client(
            p4port,
            clientname,
            user,
            f"nvci workspace {p4depot} client",
            workspacepath,
            "ViewTemplates",
            view_templates.get(p4complex),
        )

        depotpath = util.depotPath(workspacepath, p4depot)
        if not depotpath.exists():
            depotpath.mkdir()

        util.createP4Config(clientname, p4port, depotpath, user)

        if use_crystal:
            if not util.checkCFSBound(cfsname):
                # bind client to CFS
                util.bindCFS(cfsname, p4port, "-" + p4depot)

        customer = data.get("golden_cl_customer")
        cl = 0
        if customer:
            mdata["tags"]["golden_cl_customer"] = customer

            if data.get("sync_main_to_golden"):
                cl = int(util.getGoldenCL(customer, p4depot))
                mdata["sync_cls"]["rules"] = int(util.getGoldenCL(customer, "rules"))
                mdata["tags"]["isGolden"] = True

            elif data.get("sync_main_to_pickcl") and pickcl:
                cl = int(pickcl)
                mdata["sync_cls"]["rules"] = int(util.getTOTRulesCL())
                mdata["tags"]["isPickCL"] = True

        if p4depot == "sw":
            # Lookup corresponding p4sw HSMB cl in the ctdb matching the p4hw cl
            ctdb_tag = data.get("ctdb_tag")
            if ctdb_tag:
                hwcl = mdata["sync_cls"]["p4hw"]
                cl = int(util.codepSWCl(hwcl, ctdb_tag))
                util.printStderr(f"Picked codep swcl {cl} for hwcl {hwcl}")

        if cl > 0:
            scl = f"CL {cl}"
        else:
            scl = "TOT"

        util.printStderr(
            f"Syncing {p4depot} client {clientname} to {scl} under {depotpath}"
        )
        util.syncP4Path(depotpath, cl)

        # Store sync CL of client
        revision = util.updateSyncCl(depotpath)
        mdata["sync_cls"][p4complex] = int(revision)
        util.printStderr(f"Storing sync_cl of {revision} for {depotpath}")

    # Set tot_dirs
    hwdir = "hw/" + util.hwTreeName(data)
    tot_dirs = data.get("tot_dirs", [hwdir])
    if tot_dirs:
        mdata["tot_dirs"] = list(tot_dirs)
        for tdir in list(tot_dirs):
            tpath = f"{workspacepath}/{tdir}"
            util.verifyNvciYmlExists(tdir)
            # Cleanup logs in cloned tot_dirs
            util.cleanupLogs(tpath)
            util.cleanupManifest(tpath)
    else:
        util.exitWithError("Could not determine tot_dirs for main workspace")

    util.createManifest(workspacepath, mdata, "setup")

    if data.get("snapshot_after_sync") and util.isCloneable(data):
        if use_crystal:
            snapshot_mainCFS.callback(cfg, name, source, "", "sync")  # type: ignore
        else:
            snapshot_main.callback(cfg, name, source, "", "sync")  # type: ignore

    print(workspacepath)


# ---------------------------------------------------------
# Snapshot main workspace
# ---------------------------------------------------------
@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.option("--prefix", help="Prefix for snapshot name")
@click.option("--suffix", help="Suffix for snapshot name")
def snapshot_main(cfg: str, name: str, source: str, prefix: str, suffix: str) -> Any:
    snapshot_main_workspace(cfg, name, source, prefix, suffix, False)


@cli.command()
@click.option("--name", help="CFS to snapshot")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.option("--prefix", help="Prefix for snapshot name")
@click.option("--suffix", help="Suffix for snapshot name")
def snapshot_mainCFS(cfg: str, name: str, source: str, prefix: str, suffix: str) -> Any:
    util.checkCrystalHost()
    snapshot_main_workspace(cfg, name, source, prefix, suffix, True)


def snapshot_main_workspace(
    cfg: str, name: str, source: str, prefix: str, suffix: str, use_crystal: bool
) -> Any:
    data = util.getCfgData(cfg, source)
    workspacepath = util.pathFromManifest(data)
    mdata = util.getManifestWorkspaceData()

    cloneline = util.getCloneline(data)
    snapshotname = util.snapshotName(data, prefix, name, suffix)

    if util.isScratch(data):
        util.exitWithError("Cannot snapshot a regular scratch space")

    # Create a .patch_clone file before snapping
    # This will be used to patch clones
    util.createPatchCloneFile(data)

    if use_crystal:
        cfsname = util.CFSNameFromPath(workspacepath)

        if util.snapshotCFSExists(cloneline, snapshotname):
            util.printStderr(f"Snapshot {snapshotname} already exists; skipping")
        else:
            tag = data.get("snapshot_tag", "")
            util.printStderr(f"Creating snapshot CFS {snapshotname} with tag {tag}")
            util.snapshotCFS(cfsname, snapshotname, tag)

            if cloneline:
                if util.checkCFSClonelineExists(cloneline):
                    util.printStderr(
                        f"Adding {snapshotname} to CFS cloneline {cloneline}"
                    )
                    util.addSnapshotToCFSCloneline(snapshotname, cloneline)
                else:
                    util.exitWithError(
                        f"CFS cloneline {cloneline} does not exist! Please create it with 'crystal cloneline'"
                    )
    else:
        if util.snapshotExists(cloneline, snapshotname):
            util.printStderr(f"Snapshot {snapshotname} already exists; skipping")
        else:
            util.printStderr(f"Creating snapshot {snapshotname}")
            util.snapshotMain(data, snapshotname)

    # Update manifest
    mdata["tags"]["snapshot_name"] = snapshotname
    util.createManifest(workspacepath, mdata, "snapshotted")


# ---------------------------------------------------------
# Delete main workspace
# ---------------------------------------------------------
@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.option(
    "--force",
    is_flag=True,
    help="Force delete of client even if files are open for edit",
)
def delete_main(name: str, source: str, cfg: str, force: str) -> None:
    delete_main_workspace(name, source, cfg, force, False)


@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.option(
    "--force",
    is_flag=True,
    help="Force delete of client even if files are open for edit",
)
def delete_mainCFS(name: str, source: str, cfg: str, force: str) -> None:
    util.checkCrystalHost()
    delete_main_workspace(name, source, cfg, force, True)


def delete_main_workspace(
    name: str, source: str, cfg: str, force: str, use_crystal: bool
) -> None:
    data = util.getCfgData(cfg, source)
    workspacepath = util.pathFromManifest(data)

    # Record time of deletion
    util.logDeleteTime(workspacepath)

    if use_crystal:
        # Delete CFS and bound p4 clients
        cfsname = util.mainCFSName(data, name)
        util.printStderr(f"Deleting CFS {cfsname}")
        util.deleteCFS(cfsname)
    else:
        view_templates = data.get("view_templates")
        for p4complex in view_templates:
            p4port = util.getP4Port(data, p4complex)
            p4depot = util.getP4Depot(p4complex)
            clientname = util.clonelineClientName(data, p4depot)
            depotpath = util.depotPath(workspacepath, p4depot)

            # Delete depot files
            if depotpath.exists():
                util.printStderr(f"Deleting {depotpath}")
                rmtree(depotpath)

            # Delete depot client
            util.printStderr(f"Deleting {p4depot} client: {clientname}")
            util.revertAndDeleteP4Client(p4port, depotpath, clientname)

        # Cleanup main cloneline dir
        util.deleteMainWorkspace(data, workspacepath)
        if util.isFlexclone(data):
            util.deleteMainClient(data, force)


# ---------------------------------------------------------
# Create clone workspace
# ---------------------------------------------------------
@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
def create_clone(cfg: str, name: str, source: str) -> None:
    create_clone_workspace(cfg, name, source, False)


@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
def create_cloneCFS(cfg: str, name: str, source: str) -> None:
    util.checkCrystalHost()
    create_clone_workspace(cfg, name, source, True)


def create_clone_workspace(cfg: str, name: str, source: str, use_crystal: bool) -> None:
    # Resolve the project name first
    projectname = util.resolveProjectName()
    util.printStderr(f"resolved projectname = {projectname}")

    data = util.getCfgData(cfg, source)
    cloneline = util.getCloneline(data)

    # Determine the latest snapshot that matches the specified tag
    if "snapshot_filter" in data:
        tag = data.get("snapshot_filter")
    elif "snapshot_tag" in data:
        tag = data.get("snapshot_tag")
    else:
        tag = ""

    if use_crystal:
        snapshotname = util.latestSnapshotCFS(cloneline, tag)
    else:
        if tag:
            snapshot_filter = "_" + tag
        else:
            snapshot_filter = ""
        snapshotname = util.latestSnapshot(cloneline, snapshot_filter)

    if not snapshotname:
        util.exitWithError(
            f"Unable to find a snapshot in cloneline {cloneline} with tag {tag}"
        )

    # Determine clone name
    if name:
        if name == "auto":
            base = snapshotname
        else:
            base = name
    else:
        base = snapshotname

    clonename = util.cloneName(base)

    if use_crystal:
        workspacepath = util.getCFSPath(clonename)
        util.setPath(data, workspacepath)
        snapshot_tag = data.get("snapshot_tag", "")
        group = data.get("security_group", "")
        util.printStderr(
            f"Creating CFS {clonename} from cloneline {cloneline} snapshot_tag {snapshot_tag}"
        )
        util.createCFSCloneFromCloneline(cloneline, clonename, group, snapshot_tag)
    else:
        # Determine if it's OK to create clone
        run_rule_engine = data.get("run_rule_engine", False)
        if run_rule_engine:
            team = data.get("team")
            user = os.environ.get("USER")
            # Run rule_engine to determine if its OK to create a new clone
            ok = util.okToCreateClone(team, user, cloneline, clonename)  # type: ignore
            if not ok:
                util.exitWithError("Unable to create a new workspace")
        else:
            # Check if the clone limit has been exceeded
            checkCloneCount(data)

        util.printStderr(
            f"Creating workspace clone {clonename} from snapshot {snapshotname}"
        )
        workspacepath = util.createClone(data, snapshotname, clonename)  # type: ignore

    # Delete the existing .workspace directory in the clone; it came from snapshotting the main volume
    util.deleteWorkspaceDir(workspacepath)

    # Backup manifest from snapshot
    util.moveManifest("manifest.snapshot.yml")

    # Guarantee that .sync_cl files exist for each p4complex
    view_templates = data.get("view_templates")
    for p4complex in view_templates:
        p4depot = util.getP4Depot(p4complex)
        depotpath = util.depotPath(workspacepath, p4depot)

        sync_cl_from_file = util.getSyncCl(depotpath)
        sync_cl_from_snapshot = util.extractP4Revision(snapshotname, p4depot)

        if sync_cl_from_file is not None:
            util.printStderr(
                f"Clone .sync_cl contians {p4depot} CL {sync_cl_from_file}"
            )
        elif sync_cl_from_snapshot is not None:
            # If .sync_cl file does not exist, extract the sync CL from the snapshot name and write to the .sync_cl file
            util.printStderr(
                f"Snapshot {snapshotname} is synced to {p4depot} CL {sync_cl_from_snapshot}"
            )
            util.writeSyncCl(depotpath, sync_cl_from_snapshot)
        else:
            util.exitWithError(
                f"Unable to determine {p4depot} CL from snapshot {snapshotname}"
            )

    # Get PROJECT_TEAM from resolved project name
    project_team = util.getProjectTeam(".")

    if project_team:
        util.printStderr(f"Resolved PROJECT_TEAM = {project_team}")
        # Create .nvprojectname file at the top of the workspace
        util.createProjectTeamFile(workspacepath, project_team)
    else:
        util.printStderr("WARNING. Could not determine PROJECT_TEAM")

    # Create new manifest
    mdata = util.newManifestWorkspaceData()
    mdata["name"] = name
    mdata["path"] = str(workspacepath)
    mdata["source"] = source
    mdata["tags"] = {
        "snapshot_name": snapshotname,
        "clone_name": clonename,
        "project_team": project_team,
    }
    util.createManifest(workspacepath, mdata, "created")

    print(workspacepath)


def checkCloneCount(data: Any) -> int:
    clonelinename = util.clonelineName(data)
    user = os.environ.get("USER")
    clone_count = util.getCloneCount(clonelinename, user)  # type: ignore

    max_clones = data.get("max_clones")
    if max_clones and max_clones > 0:
        if clone_count > max_clones:
            util.printStderr(
                f"User {user} is using {clone_count} clones in cloneline {clonelinename}, "
                + f"which is more than the {max_clones} allowed\n"
            )
            util.printStderr(
                "Please delete one or more of these workspaces using 'nvci delete -d <workspace>':"
            )
            util.printStderr(util.listFilteredWorkspaces(user, clonelinename) + "\n")  # type: ignore
            util.exitWithError(
                "Unable to create a new workspace because too many clones are in use."
            )
    else:
        util.printStderr(
            f"User {user} is using {clone_count} clones in cloneline {clonelinename}"
        )

    return clone_count


# ---------------------------------------------------------
@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.option("--sync/--nosync", default=False, help="Sync workspace to TOT")
@click.option(
    "--cl",
    multiple=True,
    type=click.UNPROCESSED,
    callback=util.validate_cl,
    help="depot+CL to sync workspace i.e. 'hw1234567'",
)
def setup_clone(cfg: str, name: str, source: str, sync: str, cl: Any) -> None:
    setup_clone_workspace(cfg, name, source, sync, cl, False)


@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.option("--sync/--nosync", default=False, help="Sync workspace to TOT")
@click.option(
    "--cl",
    multiple=True,
    type=click.UNPROCESSED,
    callback=util.validate_cl,
    help="depot+CL to sync workspace i.e. 'hw1234567'",
)
def setup_cloneCFS(cfg: str, name: str, source: str, sync: str, cl: Any) -> None:
    util.checkCrystalHost()
    setup_clone_workspace(cfg, name, source, sync, cl, True)


def setup_clone_workspace(
    cfg: str, name: str, source: str, sync: str, cl: Any, use_crystal: bool
) -> None:
    data = util.getCfgData(cfg, source)
    workspacepath = util.pathFromManifest(data)

    user = os.environ.get("USER")
    nvci_env_wd = util.nvciEnvWorkingDir(name, source)
    pickcl = util.getNvciEnv("ghw-nvci.pickcl", nvci_env_wd)

    # Cleanup logs in clone
    util.cleanupLogs(workspacepath)

    # Get data from manifest
    mdata = util.getManifestWorkspaceData()
    mdata["name"] = name
    mdata["source"] = source
    mdata["path"] = str(workspacepath)
    mdata["conman_namespaces"] = util.getNamespaceContent(data)

    # Get cl options
    sync_clone_to_tot = data.get("sync_clone_to_tot")
    sync_main_to_golden = data.get("sync_main_to_golden")
    sync_main_to_pick_cl = data.get("sync_main_to_pick_cl")

    view_templates = data.get("view_templates")
    clonename = util.cloneNameFromPath(workspacepath)

    # Create clients for the clone
    for p4complex in view_templates:
        p4port = util.getP4Port(data, p4complex)
        p4depot = util.getP4Depot(p4complex)
        clientname = util.clientName(clonename, p4depot)
        depotpath = util.depotPath(workspacepath, p4depot)

        util.printStderr(
            f"Creating {p4depot} client {clientname} on port {p4port} under {depotpath}"
        )
        util.createP4Client(
            p4port,
            clientname,
            user,
            f"nvci workspace {p4depot} client",
            workspacepath,
            "ViewTemplates",
            view_templates.get(p4complex),
        )
        util.createP4Config(clientname, p4port, depotpath)

        # sync clone client metadata to sync CL of snapshot
        sync_cl = util.getSyncCl(depotpath)
        if sync_cl is not None:
            util.printStderr(f"Syncing client {clientname} metadata to CL {sync_cl}")
            util.syncP4Metadata(depotpath, p4port, clientname, sync_cl)
        else:
            util.exitWithError(f"Unable to determine sync CL for {depotpath}")

        # --- Sync clone to specified CL or TOT ---------
        requested_cl = cl.get(p4depot)

        if requested_cl:
            util.printStderr(f"Syncing {p4port} to requested cl: {requested_cl}")
            util.syncP4Path(depotpath, requested_cl)
            mdata["tags"]["syncedToRequestedCL"] = True

        elif pickcl and int(pickcl) > 0:
            if p4depot == "hw":
                util.printStderr(f"Syncing {p4port} to pickcl: {pickcl}")
                util.syncP4Path(depotpath, pickcl)
                mdata["tags"]["isPickCL"] = True
            elif p4depot == "sw":
                # Lookup corresponding p4sw HSMB cl in the ctdb matching the pickcl
                ctdb_tag = data.get("ctdb_tag")
                if ctdb_tag:
                    codep_cl = int(util.codepSWCl(pickcl, ctdb_tag))  # type: ignore
                    util.printStderr(f"Syncing {p4port} to codep cl: {codep_cl}")
                    util.syncP4Path(depotpath, codep_cl)
                else:
                    util.printStderr("Warning: ctdb_tag not found for syncing SW tree")

        elif sync_clone_to_tot:
            util.printStderr(f"Syncing {p4port} to TOT")
            util.syncP4Path(depotpath, 0)
            mdata["tags"]["syncedToTOT"] = True

        elif sync_main_to_golden:
            # main was synced to golden, so is clone
            mdata["tags"]["isGolden"] = True

        elif sync_main_to_pick_cl:
            # main was synced to pickcl, so is clone
            mdata["tags"]["isPickCL"] = True

        # Store revision in manifest and .sync_cl
        revision = util.updateSyncCl(depotpath)
        mdata["sync_cls"][p4complex] = int(revision)
        util.printStderr(f"Storing sync_cl of {revision} for {depotpath}")
        # -------------------------------------------------------

    # If main was synced to golden, record customer and rules_cl
    if sync_main_to_golden:
        customer = data.get("golden_cl_customer")
        mdata["tags"]["golden_cl_customer"] = customer
        mdata["sync_cls"]["rules"] = int(util.getGoldenCL(customer, "rules"))

    # Determine HW TOT dir(s)
    hwdir = "hw/" + util.hwTreeName(data)
    tot_dirs = data.get("tot_dirs", [hwdir])
    util.printStderr(f"tot_dirs = {tot_dirs}")
    if tot_dirs:
        mdata["tot_dirs"] = list(tot_dirs)
        for tdir in list(tot_dirs):
            tpath = f"{workspacepath}/{tdir}"
            util.verifyNvciYmlExists(tdir)
            # Cleanup logs in cloned tot_dirs
            util.cleanupLogs(tpath)
            util.cleanupManifest(tpath)
            # Set PROJECT_TEAM in tree.make file
            project_team = util.getProjectTeam(tpath)
            if project_team:
                util.setProjectTeam(tpath, project_team)
    else:
        util.exitWithError(
            "Could not determine HW TOT dir for clone workspace. (Set tot_dirs in workspace config)"
        )

    # Patch abs paths
    util.printStderr("Patching clone")
    util.patchClone()

    # Create new manifest for clone
    util.createManifest(workspacepath, mdata, "setup")

    print(workspacepath)


# ---------------------------------------------------------
@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.option(
    "--force",
    is_flag=True,
    help="Force delete of client even if files are open for edit",
)
def delete_clone(name: str, source: str, cfg: str, force: str) -> None:
    delete_clone_workspace(name, source, cfg, force, False)


@cli.command()
@click.option("--name", help="Workspace name")
@click.option("--source", required=True, help="Workspace source type")
@click.option("--cfg", required=True, help="Path to workspace_manager config .yml file")
@click.option(
    "--force",
    is_flag=True,
    help="Force delete of client even if files are open for edit",
)
def delete_cloneCFS(name: str, source: str, cfg: str, force: str) -> None:
    util.checkCrystalHost()
    delete_clone_workspace(name, source, cfg, force, True)


def delete_clone_workspace(
    name: str, source: str, cfg: str, force: str, use_crystal: bool
) -> None:
    data = util.getCfgData(cfg, source)
    workspacepath = util.pathFromManifest(data)

    if use_crystal:
        # Delete CFS and bound p4 clients
        cfsname = util.CFSNameFromPath(workspacepath)
        util.deleteCFS(cfsname)
    else:
        clonename = util.cloneNameFromPath(workspacepath)
        cloneport = util.getFlexcloneP4Port(workspacepath)

        view_templates = data.get("view_templates")
        for p4complex in view_templates:
            p4port = util.getP4Port(data, p4complex)
            p4depot = util.getP4Depot(p4complex)
            depotpath = util.depotPath(workspacepath, p4depot)
            clientname = util.clientName(clonename, p4depot)

            # Check if client exists
            if util.clientExists(p4port, clientname):
                if force:
                    # Force revert p4 client
                    util.printStderr(f"FORCING revert of client {clientname}")
                    util.revertAndDeleteP4Client(p4port, depotpath, clientname)
            else:
                util.printStderr(f"Skipped delete of nonexistent client {clientname}")

        # Delete clone
        util.printStderr(f"Deleting clone {clonename}")
        util.deleteClone(clonename, cloneport)

    util.printStderr(f"Workspace {workspacepath} deleted.")


# ---------------------------------------------------------
def main() -> None:
    sys.exit(cli())
