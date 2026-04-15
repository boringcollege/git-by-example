# Chapter 14 — Reflog: Your Safety Net

The reflog records every time HEAD moves. It's your undo history for Git itself.

## Viewing the Reflog

### Example: See recent HEAD movements

```bash
git reflog
```

```
e4f5a6b (HEAD -> main) HEAD@{0}: commit: Add greet function
a1b2c3d HEAD@{1}: commit (initial): Initial commit
f7g8h9i HEAD@{2}: checkout: moving from feature/login to main
b2c3d4e HEAD@{3}: commit: Add login page
a1b2c3d HEAD@{4}: checkout: moving from main to feature/login
```

🧠 **What happened?** Every checkout, commit, rebase, reset, merge, and cherry-pick is logged here with a timestamp.

### Example: See reflog with dates

```bash
git reflog --date=relative
```

```
e4f5a6b HEAD@{5 minutes ago}: commit: Add greet function
a1b2c3d HEAD@{10 minutes ago}: commit (initial): Initial commit
```

## Recovering from Mistakes

### Example: Undo an accidental hard reset

```bash
# Oops, I reset too far
git reset --hard HEAD~3

# Find the commit I lost
git reflog
```

```
a1b2c3d (HEAD -> main) HEAD@{0}: reset: moving to HEAD~3
e4f5a6b HEAD@{1}: commit: Add greet function
d4e5f6g HEAD@{2}: commit: Add routes
c3d4e5f HEAD@{3}: commit: Add controller
```

```bash
# Recover!
git reset --hard e4f5a6b
```

🧠 **What happened?** The reflog still remembered where HEAD was before the reset. You can always go back.

### Example: Recover a deleted branch

```bash
git branch -D feature/experiment
# Oh no, I needed that!

git reflog | grep experiment
```

```
b2c3d4e HEAD@{7}: checkout: moving from feature/experiment to main
```

```bash
git branch feature/experiment b2c3d4e
```

The branch is back.

### Example: Recover after a bad rebase

```bash
# Find where the branch was before the rebase
git reflog
```

```
f6g7h8i HEAD@{0}: rebase (finish): returning to refs/heads/feature/signup
f6g7h8i HEAD@{1}: rebase (pick): Add signup form
e4f5a6b HEAD@{2}: rebase (start): checkout main
b2c3d4e HEAD@{3}: commit: Add signup form    ← this is the pre-rebase state
```

```bash
git reset --hard b2c3d4e
```

## Reflog Expiration

Reflog entries expire after **90 days** by default (30 days for unreachable commits). You can configure this:

```bash
git config --global gc.reflogExpire 180
```

## Branch Reflog

Each branch has its own reflog too.

### Example: See reflog for a specific branch

```bash
git reflog show feature/login
```

---

[← Chapter 13: Git Internals](13-git-internals.md) · [Next: Chapter 15 — Bisect →](15-bisect.md)
