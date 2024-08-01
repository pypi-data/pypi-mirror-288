#!/home/utils/Python-3.9.1/bin/python3

import subprocess
import sys
from shutil import rmtree
from typing import Any

import requests
from request_token import getToken  # type: ignore

# Workaround for request_token issue
# store before clearing
# logname = os.environ["LOGNAME"]
# os.environ["LOGNAME"] = ""

CONMAN_API = "https://content-manager.nvidia.com"

access_token = getToken()

cnm = "cnm"
tarfile = "conman.tar"


# ------------------------------------------------------
def get_conman(path: str) -> Any:
    request = f"{CONMAN_API}/" + path
    # print(request)
    # print(access_token)
    try:
        resp = requests.get(
            request,
            verify=False,
            headers={
                "Authorization": f"{access_token}",
                "Content-Type": "application/json",
            },
        )
        resp.raise_for_status()

    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    except requests.ConnectionError as e:
        raise SystemExit(e)

    if resp:
        if resp.status_code == 200:
            return resp
        else:
            print("Unexpected response: {resp}")
            exit(1)
    else:
        print(f"ERROR: {resp}")
        exit(1)


def get_namespaces() -> Any:
    resp = get_conman("namespace")
    return resp.json()


def get_namespace_content(namespace: Any) -> Any:
    resp = get_conman(f"content/{namespace}")
    return resp.json()


def get_content(namespace: Any, version: Any) -> Any:
    resp = get_conman(f"content/{namespace}/{version}")
    return resp.json()


def list_content(namespace: Any) -> None:
    c = get_namespace_content(namespace)
    items = c["items"]
    for n in items:
        namespace = n["namespace"]
        version = n["name"]
        content_blob = n["content_blob_name"]
        published = n["published"]
        print("%-30s %-10s %-5s %s" % (namespace, version, content_blob, published))


def latest_published(namespace: Any) -> Any:
    c = get_namespace_content(namespace)
    items = reversed(c["items"])
    for item in items:
        # nspace = item["namespace"]
        version = item["name"]
        published = item["published"]
        # print(f"{nspace} {version} {published}")
        if published:
            return version
    return False


def list_namespaces() -> Any:
    c = get_namespaces()

    namespaces = c["items"]
    for n in namespaces:
        name = n["name"]
        desc = n["description"]
        print("%-30s %s" % (name, desc))


def download_content(namespace: Any, conmandir: Any, unpubOK: Any, version: Any) -> Any:
    # (re)create conman namespace dir
    cdir = conmandir / namespace
    rmtree(cdir, ignore_errors=True)
    cdir.mkdir(parents=True, exist_ok=True)

    # download tarfile
    printStderr(f"Downloading content for namespace {namespace} version {version}")
    cmd = (
        f"{cnm} download version {version} --namespace {namespace} --extract-dir {cdir}"
    )
    if unpubOK:
        cmd += " --unpublished"
    runCmd(cmd)


def publish_content(namespace: Any, conmandir: Any, incr: Any = "none") -> None:
    cdir = conmandir / namespace
    curr_version = read_version(namespace, conmandir)
    if not curr_version:
        curr_version = latest_published(namespace)
    version = increment_version(curr_version, incr)

    printStderr(f"Publishing content for namespace {namespace} version {version}")
    write_version(namespace, conmandir, version)
    runCmd(f"cd {cdir} && tar cvf {tarfile} --exclude={tarfile} .")
    runCmd(
        f"cd {cdir} && {cnm} upload version {version} --namespace {namespace} --content-blob-path {tarfile}"
    )
    runCmd(f"cd {cdir} && {cnm} publish version {version} --namespace {namespace}")


def download_desired_version(
    namespace: Any, conmandir: Any, unpubOK: Any, desired_version: Any
) -> Any:
    curr_version = read_version(namespace, conmandir)

    if not desired_version or desired_version == "latest":
        desired_version = latest_published(namespace)

    if curr_version != desired_version:
        download_content(namespace, conmandir, unpubOK, desired_version)
    else:
        printStderr(
            f"Keeping existing content for namespace {namespace} version {curr_version}"
        )

    return desired_version


def versionfile_name(namespace: Any, conmandir: Any) -> Any:
    cdir = conmandir / namespace
    versionfile = cdir / "VERSION"
    return versionfile


def read_version(namespace: Any, conmandir: Any) -> Any:
    versionfile = versionfile_name(namespace, conmandir)
    if versionfile.exists():
        version = runCmd(f"cat {versionfile}")
        return version
    else:
        return ""


def write_version(namespace: Any, conmandir: Any, version: Any) -> None:
    versionfile = versionfile_name(namespace, conmandir)
    runCmd(f"echo {version} > {versionfile}")


def increment_version(version: Any, incr: Any = "patch") -> Any:
    if "." in version:
        [major, minor, patch] = version.split(".")
    else:
        return version

    if incr == "major":
        major = int(major) + 1
        minor = 0
        patch = 0
    elif incr == "minor":
        minor = int(minor) + 1
        patch = 0
    elif incr == "patch":
        patch = int(patch) + 1
    return f"{major}.{minor}.{patch}"


def path_version(pathversion: str) -> Any:
    path = ""
    version = ""

    if "@" in pathversion:
        (path, version) = pathversion.split("@")
    else:
        path = pathversion
    return (path, version)


def runCmd(cmd: str) -> str:
    output = subprocess.check_output(cmd, shell=True)
    out = output.decode().strip()
    printStderr(out)
    return out


def printStderr(string: str) -> None:
    print(string, file=sys.stderr)
