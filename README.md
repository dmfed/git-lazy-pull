# Git lazy pull
Script for pulling updates from git repositories.

Given a target directory the program walks its subdirectories recursively up to specified depth and searches for **.git** subdirs in each of directories it visits. 
The script then does **git pull** in each of found directories (NOTE: including the specified target directory) and reports the result for each (_ok_ if **git pull** ran smoothly or _failed_ if exit code after running **git** was different from 0).

You'll need to **chmod +x git-lazy-pull.py** to run directly from terminal.

See **git-lazy-pull.py --help** for command-line options.

Examples:

**git-lazy-pull.py ~/mystuff** checks if there is a git repo in **~/mystuff** and does **git pull** in that directory.

**git-lazy-pull.py ~/projects -d 1 -v** will search for git repository in **~/projects** and all of its subdirectories and then try to pull updates in each providing verbose output.

If you want the script to write result to a file use **git-lazy-pull.py -l**. By default the log is written to **$HOME/.git_lazy_pull**



