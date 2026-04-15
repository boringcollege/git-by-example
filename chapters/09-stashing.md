# Chapter 9 — Stashing

Stashing saves your uncommitted changes temporarily so you can work on something else, then come back.

## Basic Stash

### Example: Stash your changes

```bash
# You're in the middle of something
echo "work in progress" >> app.js

git stash
```

```
Saved working directory and index state WIP on main: e4f5a6b Add greet function
```

```bash
git status
```

```
On branch main
nothing to commit, working tree clean
```

🧠 **What happened?** Git saved your changes to a stack and restored your working directory to a clean state. You can now switch branches safely.

### Example: Bring your changes back

```bash
git stash pop
```

```
On branch main
Changes not staged for commit:
        modified:   app.js

Dropped refs/stash@{0}
```

🧠 **What happened?** `pop` applies the most recent stash and removes it from the stack.

## Stash with a Message

### Example: Name your stash

```bash
git stash push -m "WIP: dark mode CSS"
```

```
Saved working directory and index state On main: WIP: dark mode CSS
```

## Listing Stashes

### Example: See all stashes

```bash
git stash list
```

```
stash@{0}: On main: WIP: dark mode CSS
stash@{1}: WIP on main: e4f5a6b Add greet function
```

## Applying Without Removing

### Example: Apply but keep in stack

```bash
git stash apply stash@{1}
```

🧠 **What happened?** Unlike `pop`, `apply` restores the changes but keeps the stash entry. Useful if you want to apply the same stash to multiple branches.

## Stashing Untracked Files

### Example: Include untracked files

```bash
echo "new file" > new.js
git stash push -u -m "Include new files"
```

By default, `git stash` only saves tracked files. `-u` includes untracked files too.

### Example: Include everything (even ignored files)

```bash
git stash push -a -m "Include absolutely everything"
```

## Dropping a Stash

### Example: Remove a specific stash

```bash
git stash drop stash@{1}
```

### Example: Remove all stashes

```bash
git stash clear
```

## Creating a Branch from a Stash

### Example: Stash → branch

```bash
git stash branch feature/dark-mode stash@{0}
```

🧠 **What happened?** Git created a new branch from the commit where you originally stashed, applied the stash, and dropped it. Useful when you realize your stashed work should live on its own branch.

---

[← Chapter 8: Working with Remotes](08-remotes.md) · [Next: Chapter 10 — Tagging →](10-tagging.md)
