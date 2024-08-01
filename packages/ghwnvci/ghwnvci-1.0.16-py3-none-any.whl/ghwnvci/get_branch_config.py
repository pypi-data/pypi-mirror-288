#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# @file   get_branch_config.py
# @brief  Transformer used to find the appropriate nvci config for a branch
# @author jloyola
# @date   04/17/2024
# ----------------------------------------------------------------------------
# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
# ----------------------------------------------------------------------------

import argparse
import logging
import os
import subprocess
from pathlib import Path
from typing import Any

import yaml


def _get_logger() -> Any:
    """Wrapper to get logger handle"""
    return logging.getLogger(__name__)


def _setup_logger(debug: bool) -> None:
    """Executes the steps to configure a logger"""
    logger = _get_logger()
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def run_command(cmd: str, cwd: Any = os.getcwd()) -> Any:
    """
    Wrapper for subprocess.check_call
    """
    logger = _get_logger()
    try:
        logger.debug(f"Now running: {str(cmd)}")
        result = subprocess.run(
            cmd, check=True, cwd=cwd, text=True, capture_output=True
        )
        logger.debug(f"Result: {str(result)}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"{str(e.returncode)} error code after running: {e.cmd}")
        raise e
    except Exception as ex:
        raise ex


def get_tot() -> Any:
    """
    Returns the absolute path to TOT
    """
    result = run_command("/home/nv/bin/depth")
    return Path(result.stdout).absolute()


def get_branch_config(branch_override: Any) -> str:
    """
    Returns the path to the branch-specific nvci.yml file
    """
    tot_path = get_tot()

    branch_name = tot_path.stem
    if branch_override:
        branch_name = branch_override

    nvci_config = Path(tot_path, f"etc/nvci/trees/{branch_name}/_nvci.yml")
    return str(nvci_config)


def xform_config(args: Any) -> None:
    """
    Consume the input config, merge it with the branch-specific config, and write it.
    """
    with open(args.input, "r") as f:
        input_yaml = yaml.safe_load(f)

    branch_override = input_yaml.get("branch_override")
    branch_config = get_branch_config(branch_override)

    # Inject branch-specific config using 'add-config' keyword.
    # If we dump the contents of 'branch_config' directly, additional transformers will not run.
    # We must have nvci read the file to process it.
    # See https://nvbugs/4607954/8
    if "add-config" in input_yaml["config"]:
        input_yaml["config"]["add-config"].extend(branch_config)
    else:
        input_yaml["config"]["add-config"] = [branch_config]

    with open(args.output, "w") as f:
        yaml.dump(input_yaml, f)


def get_args() -> Any:
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.get_branchion = "Transformer used to find the appropriate nvci config for a branch"  # type: ignore

    parser.add_argument(
        "--workspace-root",
        help="The root of the workspace in which nvci is being run",
        required=False,
        nargs="+",
    )
    parser.add_argument(
        "--working-dir",
        help="The space in which the transformer can store any intermediate files",
    )
    parser.add_argument("--input", help="The input YAML file from which to read")
    parser.add_argument("--output", help="The output YAML file to which to write")
    parser.add_argument(
        "--verbose",
        "-v",
        help="Enable debug prints",
        required=False,
        action="store_true",
    )
    args = parser.parse_args()
    return args


def main() -> None:
    """
    Main program
    """
    args = get_args()
    _setup_logger(args.verbose)
    xform_config(args)


if __name__ == "__main__":
    main()
