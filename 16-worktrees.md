# Chapter 16 — Worktrees

Worktrees let you check out multiple branches at the same time, each in its own directory — without cloning the repo again.

## Why Worktrees?

You're working on a feature and someone asks you to review a PR or fix a bug on `main`. Without worktrees, you'd have to stash or commit your work, switch branches, do the review, switch back. With worktrees, you just open a second directory.

## Creating a Worktree

### Example: Check out a branch in a new directory

```bash
git worktree add ../hotfix main
```

```
Preparing worktree (checking out 'main')
HEAD is now at e4f5a6b Add greet function
```

```bash
ls ../hotfix/
```

```
README.md  index.js  .gitignore
```

🧠 **What happened?** Git created a new working directory at `../hotfix` linked to the same repository. Changes in either directory share the same `.git` database. The branch `main` is now checked out in `../hotfix`.

### Example: Create a worktree with a new branch

```bash
git worktree add ../bugfix -b bugfix/issue-42
```

## Listing Worktrees

### Example: See all worktrees

```bash
git worktree list
```

```
/home/you/project         e4f5a6b [feature/signup]
/home/you/hotfix          e4f5a6b [main]
/home/you/bugfix          e4f5a6b [bugfix/issue-42]
```

## Removing a Worktree

### Example: Remove a worktree

```bash
git worktree remove ../hotfix
```

Or manually delete the directory and then clean up:

```bash
rm -rf ../hotfix
git worktree prune
```

## Rules and Limitations

A branch can only be checked out in **one** worktree at a time. If you try:

```bash
git worktree add ../another main
```

```
fatal: 'main' is already checked out at '/home/you/hotfix'
```

This prevents conflicting edits to the same branch.

---

[← Chapter 15: Bisect](15-bisect.md) · [Next: Chapter 17 — Submodules →](17-submodules.md)
