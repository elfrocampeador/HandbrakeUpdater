import sys
import os
import subprocess
import multiprocessing
from github import Github

os.chdir("/data0/private/handbrake_updater/")

github_handle = Github()
repo = github_handle.get_repo("HandBrake/HandBrake")
latest_release = repo.get_latest_release().tag_name

local_version_file = open("latest_version.txt", "r")
local_version = local_version_file.read()
local_version_file.close()

print("Local HandBrake Version is: {}".format(local_version))
print("Latest HandBrake Release is: {}".format(latest_release))


if latest_release != local_version:
    working_dir = '/home/corey/HandBrake/'
    print("  There's a new version of HandBrake available!  Downloading and building it!\n")
    status = subprocess.call(["git", "fetch"], cwd=working_dir)
    if status != 0: # Abort
        print("Couldn't fetch, aborting!")
        sys.exit(1)

    print("Checking out new code...")
    status = subprocess.call(["git", "checkout", "tags/{}".format(latest_release)], cwd=working_dir)
    if status != 0: # Abort
        print("Couldn't check out new code, aborting!")
        sys.exit(1)

    print("Building with {} CPUs...".format(multiprocessing.cpu_count()))
    status = subprocess.call(['./configure', '--force', '--launch-jobs={}'.format(multiprocessing.cpu_count()), '--launch', '--disable-gtk'], cwd=working_dir)    
    if status != 0: # Abort
        print("Couldn't build, aborting!")
        sys.exit(1)
        
    print("Installing...")
    status = subprocess.call(['sudo', 'make', '--directory=build', 'install'], cwd=working_dir)    
    if status != 0: # Abort
        print("Couldn't build, aborting!")
        sys.exit(1)
        
    print("DONE")

    local_version_file = open("latest_version.txt", "w")
    local_version_file.write("{}".format(latest_release))