# Chapter 4 — Undoing Things

Git gives you many ways to undo mistakes. The right tool depends on *where* the mistake is.

## Undo Cheatsheet

```
Mistake is in...             Use...
─────────────────────────────────────────
Working directory            git checkout -- <file>  or  git restore <file>
Staging area                 git reset HEAD <file>   or  git restore --staged <file>
Last commit (not pushed)     git commit --amend
Older commit (not pushed)    git rebase -i
Any commit (already pushed)  git revert
```

## Discard Changes in Working Directory

### Example: Throw away uncommitted edits

```bash
echo "BROKEN CODE" > index.js
git status
```

```
Changes not staged for commit:
        modified:   index.js
```

```bash
git restore index.js
cat index.js
```

```
console.log('hello');
function greet() { return 'hi'; }
```

🧠 **What happened?** `git restore` replaced the working directory version with the version from the staging area (which matches the last commit). Your changes are gone — this is not reversible.

## Unstage a File

### Example: Remove a file from the staging area

```bash
echo "secret=abc123" > .env
git add .env        # Oops, didn't mean to stage this
git restore --staged .env
git status
```

```
Untracked files:
        .env
```

🧠 **What happened?** The file is still on disk, but it's no longer staged for commit. Your changes are safe.

## Amend the Last Commit

### Example: Fix a typo in the last commit message

```bash
git commit --amend -m "Add greet function to index.js"
```

### Example: Add a forgotten file to the last commit

```bash
echo "test" > test.js
git add test.js
git commit --amend --no-edit
```

🧠 **What happened?** `--amend` replaces the last commit with a new one. The old commit is discarded. **Never amend commits you've already pushed** — it rewrites history.

## Revert a Commit

### Example: Undo a commit that's already been pushed

```bash
git log --oneline
```

```
c3d4e5f Add broken feature
e4f5a6b Add greet function
a1b2c3d Initial commit
```

```bash
git revert c3d4e5f
```

```
[main f6g7h8i] Revert "Add broken feature"
 1 file changed, 1 deletion(-)
```

```bash
git log --oneline
```

```
f6g7h8i Revert "Add broken feature"
c3d4e5f Add broken feature
e4f5a6b Add greet function
a1b2c3d Initial commit
```

🧠 **What happened?** `git revert` creates a *new* commit that undoes the changes from the target commit. History is preserved. This is the safe way to undo public commits.

## Reset: Moving the Branch Pointer

Reset is powerful and comes in three flavors:

```
                     Moves HEAD?  Resets Index?  Resets Working Dir?
git reset --soft         ✅           ❌               ❌
git reset --mixed        ✅           ✅               ❌
git reset --hard         ✅           ✅               ✅
```

### Example: Soft reset — undo commit, keep changes staged

```bash
git reset --soft HEAD~1
git status
```

```
Changes to be committed:
        modified:   index.js
```

🧠 **What happened?** The commit is gone, but your changes are still staged. Useful when you want to re-do a commit.

### Example: Mixed reset (default) — undo commit, unstage changes

```bash
git reset HEAD~1
git status
```

```
Changes not staged for commit:
        modified:   index.js
```

### Example: Hard reset — undo everything

```bash
git reset --hard HEAD~1
```

⚠️ **Warning**: `--hard` permanently discards uncommitted changes. Use with extreme care.

### Example: Reset to a specific commit

```bash
git reset --hard a1b2c3d
```

🧠 **What happened?** Your branch now points to `a1b2c3d`. All commits after it are orphaned (but recoverable via `git reflog` for ~30 days).

## Clean: Remove Untracked Files

### Example: See what would be deleted

```bash
git clean -n
```

```
Would remove temp.txt
Would remove debug.log
```

### Example: Actually delete them

```bash
git clean -f
```

### Example: Remove untracked directories too

```bash
git clean -fd
```

---

[← Chapter 3: Viewing History](03-viewing-history.md) · [Next: Chapter 5 — Branches →](05-branches.md)
