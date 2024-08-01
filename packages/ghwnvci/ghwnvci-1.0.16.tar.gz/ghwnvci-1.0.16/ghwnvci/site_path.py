#!/usr/bin/env python3

from pathlib import Path
from typing import Any, Dict, List, Union

import click

from ghwnvci import conman
from ghwnvci import workspace_utils as util


# ---------------------------------------------------------
@click.command()
@click.option("--root", "--workspace-root", help="path to workspace")
@click.option("--wd", "--working-dir", help="dir where temp files can be put")
@click.option("--input_file", "--input", required=True, help="input file")
@click.option("--output_file", "--output", help="output file")
def site_path(root: str, wd: str, input_file: str, output_file: str) -> None:
    path = None
    transformer_content = None
    conmandir = Path(f"{wd}/conman")

    # Determine current site
    site = util.getSite()

    # Read input file
    workspace_source = util.readYamlFile(input_file)

    # get path matching site from transfomer file
    ghwconfig = workspace_source.get("ghw-nvci")
    if ghwconfig:
        transformer_content = ghwconfig.get("transformer_content", "")
        site_paths = ghwconfig.get("site_paths", {})

    if transformer_content:
        util.printStderr(f"Getting path from {transformer_content}")
        site_path_file = getContent(conmandir, transformer_content)
        path = getSitePathFromFile(site, site_path_file)
    elif site_paths:
        util.printStderr("Getting path from site_paths")
        path = getSitePath(site, site_paths)
    else:
        util.exitWithError("site_paths not defined in workspace configuration")

    if path is not None:
        util.printStderr(f"Found path for site {site}: {path}\n")
        # Replace path
        recursive_replace(workspace_source, "path", path)
        # Write output file
        util.writeYamlFile(output_file, workspace_source)
    else:
        util.exitWithError(f"No path found for site {site} found")


# ----------------------------------------------------------------
def getSitePathFromFile(site: str, site_path_file: Any) -> Any:
    pconfig = util.readYamlFile(site_path_file)
    if pconfig:
        site_paths = pconfig.get("site_paths", [])
        return getSitePath(site, site_paths)
    return None


def getSitePath(site: str, site_paths: dict) -> Any:
    for item in site_paths:
        if item["site"] == site:
            paths = item.get("paths", [])
            if paths:
                # Use first path
                path = paths[0]
                return path
    return None


# ----------------------------------------------------------------
def getContent(conmandir: Path, conmanpath: str) -> Path:
    # Get namespace content from Content Manager
    (path, version) = conman.path_version(conmanpath)
    namespace = path.split("/")[0]
    if not version:
        version = "latest"
    conman.download_desired_version(namespace, conmandir, True, version)
    return Path(f"{conmandir}/{path}")


# ----------------------------------------------------------------
def recursive_replace(
    node: Union[List[Any], Dict[Any, Any]], node_name: str, val: Any
) -> None:
    # If the node is a dictionary
    if isinstance(node, dict):
        if node_name in node:
            # Found a matching node_name to replace with val
            node[node_name] = val
        else:
            # Otherwise, continue searching recursively in each value
            for value in node.values():
                recursive_replace(value, node_name, val)

    # If the node is a list
    elif isinstance(node, list):
        for item in node:
            # Continue searching recursively in each item
            recursive_replace(item, node_name, val)


# ----------------------------------------------------------------
def main() -> None:
    site_path()
