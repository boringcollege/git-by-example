# Chapter 6 — Merging

Merging takes the work from one branch and integrates it into another.

## Fast-Forward Merge

When the target branch hasn't diverged, Git simply moves the pointer forward.

### Example: Fast-forward merge

```bash
git switch main
git merge feature/signup
```

```
Updating a1b2c3d..d5e6f7g
Fast-forward
 signup.js | 5 +++++
 1 file changed, 5 insertions(+)
 create mode 100644 signup.js
```

Before:

```
main:           A --- B
                         \
feature/signup:           C --- D
```

After:

```
main:           A --- B --- C --- D
```

🧠 **What happened?** No merge commit was created. Git simply moved `main` forward to where `feature/signup` was.

## Three-Way Merge

When both branches have new commits, Git creates a merge commit.

### Example: Merge with a merge commit

```bash
# Set up: both branches have diverged
git switch main
echo "main work" >> app.js && git add . && git commit -m "Work on main"

git switch feature/login
echo "login work" >> login.js && git add . && git commit -m "Work on login"

git switch main
git merge feature/login
```

```
Merge made by the 'ort' strategy.
 login.js | 1 +
 1 file changed, 1 insertion(+)
```

```bash
git log --oneline --graph
```

```
*   h8i9j0k Merge branch 'feature/login'
|\
| * f7g8h9i Work on login
* | e4f5a6b Work on main
|/
* a1b2c3d Initial commit
```

## Handling Merge Conflicts

Conflicts happen when both branches changed the same lines.

### Example: Create a conflict

```bash
# On main
echo "version = 2" > config.txt && git add . && git commit -m "Set version 2"

# On feature branch
git switch -c feature/config
echo "version = 3" > config.txt && git add . && git commit -m "Set version 3"

# Try to merge
git switch main
git merge feature/config
```

```
Auto-merging config.txt
CONFLICT (content): Merge conflict in config.txt
Automatic merge failed; fix conflicts and then commit the result.
```

### Example: See the conflict markers

```bash
cat config.txt
```

```
<<<<<<< HEAD
version = 2
=======
version = 3
>>>>>>> feature/config
```

### Example: Resolve the conflict

Edit the file to keep what you want:

```
version = 3
```

Then:

```bash
git add config.txt
git commit -m "Merge feature/config: use version 3"
```

🧠 **What happened?** Git couldn't automatically decide which version to keep, so it put both versions in the file with markers. You manually resolved it, then committed the result.

### Example: Abort a merge

If you're in the middle of a conflict and want to start over:

```bash
git merge --abort
```

Everything goes back to the state before you ran `git merge`.

## Merge Strategies

### Example: Force a merge commit (no fast-forward)

```bash
git merge --no-ff feature/signup
```

This creates a merge commit even when fast-forward is possible. Useful for preserving the fact that work happened on a branch.

### Example: Squash merge

```bash
git merge --squash feature/signup
git commit -m "Add signup feature"
```

🧠 **What happened?** All commits from the branch are combined into a single set of changes in the staging area. You then commit them as one commit. The branch's individual commits don't appear in `main`'s history.

---

[← Chapter 5: Branches](05-branches.md) · [Next: Chapter 7 — Rebasing →](07-rebasing.md)
