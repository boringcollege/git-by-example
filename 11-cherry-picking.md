# Chapter 11 — Cherry-Picking

Cherry-pick copies a single commit from one branch to another.

## When to Cherry-Pick

Cherry-picking is useful when you need one specific commit from another branch without merging the whole branch. Common scenarios: applying a hotfix from `main` to a release branch, or grabbing a single bug fix from a feature branch.

## Basic Cherry-Pick

### Example: Apply a single commit

```bash
git switch main
git cherry-pick f7g8h9i
```

```
[main k1l2m3n] Fix login redirect bug
 Date: Mon Mar 10 16:00:00 2025 +0330
 1 file changed, 2 insertions(+), 1 deletion(-)
```

🧠 **What happened?** Git created a *new* commit on `main` with the same changes as `f7g8h9i`, but with a different hash. The original commit on the other branch is untouched.

## Cherry-Pick Multiple Commits

### Example: Pick a range

```bash
git cherry-pick a1b2c3d..e4f5a6b
```

⚠️ The range is **exclusive** of the first commit. This picks everything *after* `a1b2c3d` up to and including `e4f5a6b`.

### Example: Pick several specific commits

```bash
git cherry-pick a1b2c3d e4f5a6b f7g8h9i
```

## Handling Conflicts

### Example: Conflict during cherry-pick

```bash
git cherry-pick f7g8h9i
```

```
CONFLICT (content): Merge conflict in app.js
error: could not apply f7g8h9i... Fix login redirect bug
```

```bash
# Fix the conflict in app.js
git add app.js
git cherry-pick --continue
```

### Example: Abort the cherry-pick

```bash
git cherry-pick --abort
```

## Cherry-Pick Without Committing

### Example: Apply changes but don't commit

```bash
git cherry-pick --no-commit f7g8h9i
git status
```

```
Changes to be committed:
        modified:   app.js
```

🧠 **What happened?** The changes are staged but not committed. You can modify them further or combine them with other changes before committing.

---

[← Chapter 10: Tagging](10-tagging.md) · [Next: Chapter 12 — Interactive Rebase →](12-interactive-rebase.md)
