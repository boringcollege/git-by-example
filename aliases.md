# Appendix C — Aliases Worth Having

Copy and paste the following into your terminal to set up all aliases at once.

## Essential Aliases

```bash
# Short forms
git config --global alias.st "status -sb"
git config --global alias.co "checkout"
git config --global alias.sw "switch"
git config --global alias.br "branch"
git config --global alias.ci "commit"
git config --global alias.cp "cherry-pick"
```

## Log Aliases

```bash
# Beautiful one-line graph log
git config --global alias.lg "log --oneline --graph --all --decorate"

# Detailed graph log
git config --global alias.ll "log --graph --all --decorate --format='%C(yellow)%h%C(reset) %C(cyan)%an%C(reset) %s %C(green)(%cr)%C(reset)%C(auto)%d'"

# Show the last commit
git config --global alias.last "log -1 HEAD --stat"

# Commits from today
git config --global alias.today "log --since=midnight --oneline --author='$(git config user.name)'"

# Commits from this week
git config --global alias.week "log --since='1 week ago' --oneline --author='$(git config user.name)'"
```

## Undo Aliases

```bash
# Unstage a file
git config --global alias.unstage "restore --staged"

# Amend the last commit without editing the message
git config --global alias.amend "commit --amend --no-edit"

# Undo the last commit, keep changes staged
git config --global alias.undo "reset --soft HEAD~1"

# Discard all uncommitted changes (dangerous!)
git config --global alias.nuke "!git reset --hard HEAD && git clean -fd"
```

## Branch Aliases

```bash
# Delete all merged branches
git config --global alias.cleanup "!git branch --merged main | grep -v 'main' | xargs -r git branch -d"

# Show branches sorted by last commit date
git config --global alias.recent "branch --sort=-committerdate --format='%(committerdate:relative)%09%(refname:short)'"

# Show current branch name
git config --global alias.current "branch --show-current"
```

## Diff Aliases

```bash
# Word-level diff (useful for prose)
git config --global alias.wdiff "diff --word-diff"

# Show only filenames that changed
git config --global alias.changed "diff --name-only"

# Diff of staged changes
git config --global alias.staged "diff --staged"
```

## Workflow Aliases

```bash
# Save work in progress
git config --global alias.wip "!git add -A && git commit -m 'WIP: work in progress [skip ci]'"

# Quick save and push
git config --global alias.save "!git add -A && git commit -m 'chore: savepoint' && git push"

# Pull with rebase
git config --global alias.up "pull --rebase --autostash"

# Force push safely
git config --global alias.pushf "push --force-with-lease"
```

## Info Aliases

```bash
# Who contributed?
git config --global alias.who "shortlog -sn --all"

# List all aliases
git config --global alias.aliases "config --get-regexp ^alias\\."

# Show repo root directory
git config --global alias.root "rev-parse --show-toplevel"
```

## Usage Examples

After setting up these aliases:

```bash
$ git st
## main...origin/main
 M README.md

$ git lg
* e4f5a6b (HEAD -> main) Add greet function
* a1b2c3d Initial commit

$ git recent
5 minutes ago    main
2 hours ago      feature/login
3 days ago       feature/old-experiment

$ git today
e4f5a6b Add greet function
d4e5f6g Fix tests
c3d4e5f Update README

$ git undo
# Last commit undone, changes are staged and ready to re-commit
```

## Shell Aliases (bonus)

Add these to your `~/.bashrc` or `~/.zshrc` for even shorter commands:

```bash
alias g="git"
alias gs="git status -sb"
alias gc="git commit"
alias gp="git push"
alias gl="git pull"
alias gd="git diff"
alias gco="git checkout"
alias gsw="git switch"
alias gb="git branch"
alias ga="git add"
alias glg="git log --oneline --graph --all --decorate"
```

Now `gs` shows status, `glg` shows the graph, and `ga .` stages everything.
