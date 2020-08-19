# Git lazy pull
Script for pulling updates from git repositories.

Given a target directory the program searches for **.git** subdirectory in it and walks subdirectories recursively up to specified depth.
The script then goes to each of found directories with repositories, does **git pull** and reports the result for each.

You'll need to **chmod +x git-lazy-pull.py** to run directly from terminal.

See **git-lazy-pull.py --help** for command-line options.

Examples:

**git-lazy-pull.py ~/mystuff** checks if there is a git repo in **~/mystuff** and does **git pull** in that directory.
**git-lazy-pull.py ~/projects -d 1** will search for git repositories in **~/projects** and all of its subdirectories.





