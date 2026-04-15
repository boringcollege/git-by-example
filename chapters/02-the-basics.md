# Chapter 2 — The Basics: Add, Commit, Status

## The Three Areas

Git has three areas you need to understand:

```
Working Directory  →  Staging Area (Index)  →  Repository (.git)
    (your files)        (git add)               (git commit)
```

- **Working Directory**: the files you see and edit.
- **Staging Area**: a draft of your next commit. You choose what goes in.
- **Repository**: the permanent history.

## Checking Status

### Example: Status of a fresh repo

```bash
git status
```

```
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

### Example: Create a file and check status

```bash
echo "# My Project" > README.md
git status
```

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md

nothing added to commit but untracked files present (use "git add" to track)
```

🧠 **What happened?** Git sees a new file it hasn't been told to track. It's "untracked."

## Adding Files to the Staging Area

### Example: Stage a single file

```bash
git add README.md
git status
```

```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
```

### Example: Stage everything

```bash
echo "console.log('hello');" > index.js
echo "node_modules/" > .gitignore
git add .
git status
```

```
Changes to be committed:
        new file:   .gitignore
        new file:   README.md
        new file:   index.js
```

🧠 **What happened?** `git add .` stages all new and modified files in the current directory and below.

### Example: Stage only part of a file

```bash
git add -p index.js
```

Git will show you each change (hunk) and ask:

```
Stage this hunk [y,n,q,a,d,s,e,?]?
```

Type `y` to stage that hunk, `n` to skip it. This lets you create precise, focused commits even when you've made many changes to one file.

## Making a Commit

### Example: Commit with a message

```bash
git commit -m "Initial commit: add README, index.js, and .gitignore"
```

```
[main (root-commit) a1b2c3d] Initial commit: add README, index.js, and .gitignore
 3 files changed, 3 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 index.js
```

### Example: Commit with a longer message

```bash
git commit
```

This opens your editor. Write:

```
Add user authentication module

- Add login/logout endpoints
- Add session middleware
- Add password hashing with bcrypt
```

🧠 **What happened?** Git took a snapshot of everything in the staging area and stored it permanently. The commit gets a unique SHA hash (`a1b2c3d`).

## The Edit-Stage-Commit Cycle

Here's the workflow you'll use hundreds of times a day:

```bash
# 1. Edit files
echo "function greet() { return 'hi'; }" >> index.js

# 2. See what changed
git status
git diff

# 3. Stage the changes
git add index.js

# 4. Commit
git commit -m "Add greet function"
```

## Viewing Differences

### Example: See unstaged changes

```bash
echo "// TODO: add tests" >> index.js
git diff
```

```diff
diff --git a/index.js b/index.js
index 1a2b3c4..5d6e7f8 100644
--- a/index.js
+++ b/index.js
@@ -1,2 +1,3 @@
 console.log('hello');
 function greet() { return 'hi'; }
+// TODO: add tests
```

### Example: See staged changes (what will be in the next commit)

```bash
git add index.js
git diff --staged
```

```diff
+// TODO: add tests
```

### Example: See both staged and unstaged

```bash
git diff HEAD
```

## Removing and Renaming Files

### Example: Remove a file

```bash
git rm old-file.js
git commit -m "Remove old-file.js"
```

### Example: Rename a file

```bash
git mv index.js app.js
git status
```

```
Changes to be committed:
        renamed:    index.js -> app.js
```

🧠 **What happened?** `git mv` is a shortcut for `mv` + `git rm` + `git add`. Git detects renames by comparing file content.

---

[← Chapter 1: Getting Started](01-getting-started.md) · [Next: Chapter 3 — Viewing History →](03-viewing-history.md)
