# Chapter 5 — Branches

A branch in Git is just a pointer to a commit. Creating a branch is instant and cheap — there's no reason not to branch early and often.

## Listing Branches

### Example: See local branches

```bash
git branch
```

```
  feature/login
* main
```

The `*` marks the branch you're currently on.

### Example: See all branches (including remote)

```bash
git branch -a
```

```
  feature/login
* main
  remotes/origin/main
  remotes/origin/feature/login
```

## Creating a Branch

### Example: Create a branch

```bash
git branch feature/signup
```

### Example: Create and switch in one command

```bash
git switch -c feature/signup
```

Or the older syntax:

```bash
git checkout -b feature/signup
```

🧠 **What happened?** Git created a new pointer called `feature/signup` pointing at the same commit you're currently on. `switch -c` also moves `HEAD` to that branch.

## Switching Branches

### Example: Switch to an existing branch

```bash
git switch main
```

```
Switched to branch 'main'
```

### Example: What happens to uncommitted changes?

```bash
# On feature/signup
echo "signup code" > signup.js
git switch main
```

```
error: Your local changes to the following files would be overwritten by checkout:
        signup.js
Please commit your changes or stash them before you switch branches.
```

🧠 **What happened?** Git protects you from losing work. You have three options: commit, stash (see [Chapter 9](09-stashing.md)), or discard.

## Renaming a Branch

### Example: Rename the current branch

```bash
git branch -m new-name
```

### Example: Rename any branch

```bash
git branch -m old-name new-name
```

## Deleting a Branch

### Example: Delete a merged branch

```bash
git branch -d feature/signup
```

```
Deleted branch feature/signup (was e4f5a6b).
```

### Example: Force-delete an unmerged branch

```bash
git branch -D feature/experiment
```

⚠️ `-D` deletes the branch even if its changes haven't been merged anywhere. The commits become orphaned.

## Understanding HEAD

`HEAD` is a pointer to "where you are right now." Normally, it points to a branch, which points to a commit.

```
HEAD → main → e4f5a6b
```

### Example: See where HEAD points

```bash
cat .git/HEAD
```

```
ref: refs/heads/main
```

### Example: Detached HEAD (looking at an old commit)

```bash
git checkout a1b2c3d
```

```
Note: switching to 'a1b2c3d'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.
```

🧠 **What happened?** HEAD now points directly to a commit instead of a branch. You can look around and experiment, but any new commits won't belong to any branch. Switch back with `git switch main`.

---

[← Chapter 4: Undoing Things](04-undoing-things.md) · [Next: Chapter 6 — Merging →](06-merging.md)
