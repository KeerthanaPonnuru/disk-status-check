#!/usr/bin/env python3
"""
A script to gather data about a disk to verify its presence in the OS.
Defaults to 'sda' if no disk is passed at runtime.
"""

import subprocess
import sys
import time


def check_return_code(return_code, error_message, status, *output):
    """
    Check the return code of a subprocess and update the global status.

    Args:
        return_code (int): The return code from the subprocess.
        error_message (str): The error message if the return code is not zero.
        *output (str): Additional output to display in case of an error.
    """
    if return_code != 0:
        print(f"ERROR:retval {return_code} : {error_message}", file=sys.stderr)
        if status == 0:
            status = return_code
        for item in output:
            print(f"output: {item}")
    return status


def main(disk="sda"):
    """
    Main function to check if the disk is properly represented in the OS.

    Args:
        disk (str): The disk to check, defaults to "sda".
    """
    status = 0
    nvdimm = "pmem"
    if nvdimm in disk:
        print(f"Disk {disk} appears to be an NVDIMM, skipping")
        sys.exit(status)

    # Check /proc/partitions
    result = subprocess.run(
        ["grep", "-w", "-q", disk, "/proc/partitions"],
        check=False
    )

    status = check_return_code(
        result.returncode,
        f"Disk {disk} not found in /proc/partitions",
        status
    )

    # Check /proc/diskstats
    result = subprocess.run(
        ["grep", "-w", "-q", "-m", "1", disk, "/proc/diskstats"],
        check=False
    )

    status = check_return_code(
        result.returncode,
        f"Disk {disk} not found in /proc/diskstats",
        status
    )

    # Verify the disk shows up in /sys/block/
    if not subprocess.run(
        ["ls", f"/sys/block/{disk}"],
        check=False
    ).returncode == 0:
        status = check_return_code(
            1,
            f"Disk {disk} not found in /sys/block",
            status
        )

    # Verify there are stats in /sys/block/{disk}/stat
    if not subprocess.run(
        ["test", "-s", f"/sys/block/{disk}/stat"],
        check=False
    ).returncode == 0:
        status = check_return_code(
            1,
            f"stat is either empty or nonexistent in /sys/block/{disk}/stat",
            status
        )

    # Get some baseline stats for use later
    proc_stat_begin = subprocess.check_output(
        ["grep", "-w", "-m", "1", disk, "/proc/diskstats"]
    ).decode().strip()
    sys_stat_begin = subprocess.check_output(
        ["cat", f"/sys/block/{disk}/stat"]
    ).decode().strip()

    # Generate some disk activity using hdparm -t
    subprocess.run(
        ["hdparm", "-t", f"/dev/{disk}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

    # Sleep 5 to let the stats files catch up
    time.sleep(5)

    # Make sure the stats have changed
    proc_stat_end = subprocess.check_output(
        ["grep", "-w", "-m", "1", disk, "/proc/diskstats"]
    ).decode().strip()
    sys_stat_end = subprocess.check_output(
        ["cat", f"/sys/block/{disk}/stat"]
    ).decode().strip()

    # Check for changes in /proc/diskstats
    if proc_stat_begin == proc_stat_end:
        status = check_return_code(
            1,
            "Stats in /proc/diskstats did not change",
            proc_stat_begin, proc_stat_end,
            status
        )
    else:
        status = check_return_code(
            0,
            "Stats in /proc/diskstats changed",
            status
        )

    # Check for changes in /sys/block/{disk}/stat
    if sys_stat_begin == sys_stat_end:
        status = check_return_code(
            1,
            f"Stats in /sys/block/{disk}/stat did not change",
            sys_stat_begin, sys_stat_end,
            status
        )
    else:
        status = check_return_code(
            0,
            f"Stats in /sys/block/{disk}/stat changed",
            status
        )

    if status == 0:
        print(f"PASS: Finished testing stats for {disk}")

    sys.exit(status)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
