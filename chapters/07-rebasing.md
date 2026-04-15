# Chapter 7 — Rebasing

Rebasing replays your commits on top of another branch, creating a linear history.

## Merge vs. Rebase

```
MERGE creates this:              REBASE creates this:

*   Merge branch 'feature'       * C' (feature, rebased)
|\                                * B' (feature, rebased)
| * C (feature)                   * E (main)
| * B (feature)                   * D (main)
* | E (main)                      * A
* | D (main)
|/
* A
```

Both integrate the same changes. Rebase gives you a cleaner, linear history.

## Basic Rebase

### Example: Rebase a feature branch onto main

```bash
git switch feature/signup
git rebase main
```

```
Successfully rebased and updated refs/heads/feature/signup.
```

```bash
git log --oneline
```

```
b2c3d4e (HEAD -> feature/signup) Add signup form
a9b8c7d (main) Latest main commit
```

🧠 **What happened?** Git took the commits from `feature/signup` that aren't in `main`, then replayed them one by one on top of `main`. Each replayed commit gets a new hash because its parent changed.

### Example: Then fast-forward main

```bash
git switch main
git merge feature/signup
```

```
Fast-forward
```

Now `main` has a clean, linear history with no merge commit.

## Handling Rebase Conflicts

Conflicts work similarly to merge conflicts, but you resolve them commit-by-commit.

### Example: Conflict during rebase

```bash
git switch feature/config
git rebase main
```

```
CONFLICT (content): Merge conflict in config.txt
error: could not apply b2c3d4e... Update config
hint: Resolve all conflicts manually, then run "git rebase --continue".
hint: To abort, run "git rebase --abort".
```

```bash
# 1. Fix the conflict in config.txt
# 2. Stage the fix
git add config.txt
# 3. Continue the rebase
git rebase --continue
```

### Example: Abort a rebase

```bash
git rebase --abort
```

Everything goes back to how it was before the rebase started.

### Example: Skip a conflicting commit

```bash
git rebase --skip
```

⚠️ This drops the conflicting commit entirely.

## The Golden Rule of Rebasing

> **Never rebase commits that have been pushed and shared with others.**

Rebasing rewrites commit hashes. If someone else has based work on the original commits, rebasing will cause chaos.

```
Safe to rebase:
  Your local commits that haven't been pushed yet.

NOT safe to rebase:
  Anything on a shared branch that others have pulled.
```

## Rebase onto a Specific Commit

### Example: Rebase onto a specific point

```bash
git rebase --onto main feature/old-base feature/new-feature
```

🧠 **What happened?** This takes the commits between `feature/old-base` and `feature/new-feature`, and replays them on top of `main`. Useful when you branched from the wrong point.

---

[← Chapter 6: Merging](06-merging.md) · [Next: Chapter 8 — Working with Remotes →](08-remotes.md)
