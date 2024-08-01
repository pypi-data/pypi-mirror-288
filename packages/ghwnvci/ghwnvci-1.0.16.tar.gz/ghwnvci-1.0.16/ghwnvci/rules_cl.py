#!/usr/bin/env python3
import re
import subprocess
import sys


def main() -> None:
    # Determine CL of current client
    cl = ""
    revision = runCmdOutput("p4 _revision --fullSync")
    match = re.search(r"revision: (\d+)", revision)
    if match:
        cl = match.group(1)
    else:
        printStderr("ERROR: Coluld not determine CL of client")
        exit(1)

    # Lookup CL in golden_cl DB
    golden_output = runCmdFallback(
        f"/home/nv/utils/GoldenCl/v2_latest/bin/golden_cl status --cl {cl}"
    )

    if golden_output:
        # Golden CL found
        lines = golden_output.split("\n")
        filtered_lines = [
            line.strip() for line in lines if cl in line and ".2001" in line
        ]

        if filtered_lines:
            columns = filtered_lines[0].split("|")

            if len(columns) > 3:
                data = columns[3].strip()
                data = data.replace("2001", "p4hw")
                if data:
                    printStderr(f"Using golden rules CL {data}")
                    print(data)
            else:
                printStderr(f"Rules CL not found for golden CL {cl}")
                exit(1)
        else:
            printStderr(f"No output for golden CL {cl}")
            exit(1)
    else:
        # Golden CL not found; default to TOT rules CL
        printStderr("Using TOT rules CL")
        print("tot.p4hw")


def printStderr(msg: str) -> None:
    print(msg, file=sys.stderr)


def runCmdOutput(cmd: str) -> str:
    output = subprocess.check_output(cmd, shell=True)
    out = output.decode().strip()
    return out


def runCmdFallback(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode:
        return ""
    else:
        return result.stdout.strip()
