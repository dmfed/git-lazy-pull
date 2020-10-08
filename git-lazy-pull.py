#!/usr/bin/env python3
#  Copyright 2020 Dmitry Fedotov <dafedotov@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os, datetime, sys, argparse
import subprocess as sub

LOGFILENAME = ".git_lazy_pull"
HOME = os.path.expanduser("~")

def find_git_repos(path: str, depth=0) -> list:
    '''
    Checks specified path and returns list of subdirectories up to <depth>, which have
    .git subdir in them.
    '''
    if depth == 0:
        return [path] if check_dir_has_git(path) else []
    dirs_with_git = []
    if check_dir_has_git(path):
        dirs_with_git.append(path)
    dirs = [path + os.path.sep + d for d in os.listdir(path) if os.path.isdir(path + os.path.sep + d)]
    for d in dirs:
        dirs_with_git.extend(find_git_repos(d, depth-1))
    return dirs_with_git


def check_dir_has_git(dirname: str) -> bool:
    '''
    Lists files and directories in the given directory
    and returns True if the given directory has ".git" subdir in it.
    '''
    dirs = os.listdir(dirname)
    for d in dirs:
        if os.path.isdir(dirname + os.path.sep + d) and d == ".git":
            return True
    return False


def run_git_pull(dirname: str, verbose=True) -> int:
    '''
    Changes current dir to <dirname> and runs git pull.
    Returns exit code of the command.
    '''
    os.chdir(dirname)
    proc = sub.run(["git", "pull"], capture_output=True)
    if verbose:
        print(f"Changed dir to {dirname}, and issued \"git pull\"...")
        print(proc.stdout.decode())
        print(proc.stderr.decode())
        print(f"\"git pull\" returned {proc.returncode}.", end=" ")
        if proc.returncode == 0:
            print("Repo updated.")
        else:
            print("Looks like something went wrong...")
    return proc.returncode


def run_update(path: str, depth: int, verbose=True) -> list:
    '''
    Does the actual update: runs search in specified directory
    then launches run_git_pull() function for every directory which has .git
    '''
    dirs_with_git = find_git_repos(path, depth)
    if verbose:
        print(f"Found {len(dirs_with_git)} repositories in {path}")
    status = []
    for dir in dirs_with_git:
        result = run_git_pull(dir, verbose=verbose)
        if result == 0:
            result = "updated"
        else:
            result = "failed"
        status.append((dir, result))
    return status

def check_dir_is_valid_path(path: str) -> bool:
    '''
    Checks if path exists and is actually a directory.
    '''
    return (os.path.exists(path) and os.path.isdir(path))

def write_log(status: list, verbose=True) -> bool:
    '''
    Replaces log file $HOME/.git_lazy_pull with most recent result
    of running script.

    This functions relies on constants defined in the beginning of script:
    LOGFILENAME = ".git_lazy_pull"
    HOME = os.path.expanduser("~")
    '''
    filename = HOME + os.path.sep + LOGFILENAME
    try:
        with open(filename, "w") as f:
            f.write(f"Last update on {datetime.datetime.now()}\n")
            for tup in status:
                f.write(f"{tup[0]} status: {tup[1]}\n")
        if verbose:
            print(f"Wrote result to {filename}. All ok.")
        return True
    except:
        if verbose:
            print(f"Failed to write result to {filename}")
        return False




def parse_args():
    '''
    Parses command-line arguments and outputs basic help info.
    '''
    parser = argparse.ArgumentParser(
    description='Looks for git repositories in specified directory (and subdirs up to --depth n) and runs "git pull" in each of them')
    parser.add_argument('path',  metavar='path',
                        help='Where to look for git repositories',
                        type=str)
    parser.add_argument('-d', '--depth',  metavar='number',
                        type=int, default=0,
                        help='If set to 0 only looks in the specified path, if 1 - includes specified path + subdirectories, 2 - includes subdirs of subdirs, etc.')
    parser.add_argument('-l', '--log',
                        default=False, action='store_true',
                        help='If set (by defaul it is not) writes output to $HOME/.git_updater')
    parser.add_argument('-v', '--verbose',
                        default=False, action='store_true',
                        help='If set (by default it is not) the program echoes output from "git pull" command')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    currdir = os.getcwd()
    workpath = os.path.abspath(args.path)
    if not check_dir_is_valid_path(workpath):
        print("Invalid path specified (path does not exist or is a file). Exiting...")
        sys.exit(1)
    if args.depth < 0:
        print("Depth can not be less than 0. Exiting...")
        sys.exit(1)
    print("Starting update...")
    status = run_update(workpath, args.depth, verbose=args.verbose)
    if len(status) == 0:
        print("No git repositories found in specifies path. Check whether --depth argument is correct. Exiting...")
        sys.exit(0)
    print(f"Last update on {datetime.datetime.now()}. Processed {len(status)} repositories.")
    for tup in status:
        print(f"{tup[0]} status: {tup[1]}")
    os.chdir(currdir)
    if args.log:
        result = write_log(status, args.verbose)
        if result:
            print("Log updated.")
        else:
            print("Log NOT updated.")
            sys.exit(1)
    print("Update completed. Exiting...")


if __name__ == "__main__":
    main()
