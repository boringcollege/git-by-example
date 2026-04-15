# Chapter 3 — Viewing History

## The Log

### Example: Basic log

```bash
git log
```

```
commit e4f5a6b (HEAD -> main)
Author: Dariush Abbasi <dariush@example.com>
Date:   Mon Mar 10 14:32:00 2025 +0330

    Add greet function

commit a1b2c3d
Author: Dariush Abbasi <dariush@example.com>
Date:   Mon Mar 10 14:30:00 2025 +0330

    Initial commit: add README, index.js, and .gitignore
```

### Example: One-line log

```bash
git log --oneline
```

```
e4f5a6b (HEAD -> main) Add greet function
a1b2c3d Initial commit: add README, index.js, and .gitignore
```

### Example: Log with a graph

```bash
git log --oneline --graph --all
```

```
* f7g8h9i (feature/login) Add login page
| * e4f5a6b (HEAD -> main) Add greet function
|/
* a1b2c3d Initial commit
```

🧠 **What happened?** `--graph` draws the branch structure as ASCII art. `--all` shows all branches, not just the one you're on.

### Example: Log for a specific file

```bash
git log --oneline -- README.md
```

```
a1b2c3d Initial commit: add README, index.js, and .gitignore
```

### Example: Search commits by message

```bash
git log --oneline --grep="fix"
```

### Example: Search commits by code change

```bash
git log --oneline -S "greet"
```

🧠 **What happened?** `-S` (the "pickaxe") finds commits where the number of occurrences of "greet" changed — i.e., where that string was added or removed.

## Show a Specific Commit

### Example: Show full commit details

```bash
git show e4f5a6b
```

```
commit e4f5a6b
Author: Dariush Abbasi <dariush@example.com>
Date:   Mon Mar 10 14:32:00 2025 +0330

    Add greet function

diff --git a/index.js b/index.js
index 1a2b3c4..5d6e7f8 100644
--- a/index.js
+++ b/index.js
@@ -1 +1,2 @@
 console.log('hello');
+function greet() { return 'hi'; }
```

### Example: Show only the files that changed

```bash
git show --stat e4f5a6b
```

```
 index.js | 1 +
 1 file changed, 1 insertion(+)
```

## Blame: Who Changed What

### Example: See who wrote each line

```bash
git blame index.js
```

```
a1b2c3d (Dariush Abbasi 2025-03-10 14:30:00 +0330 1) console.log('hello');
e4f5a6b (Dariush Abbasi 2025-03-10 14:32:00 +0330 2) function greet() { return 'hi'; }
```

🧠 **What happened?** `git blame` annotates each line with the commit, author, and date of the last change. Despite the dramatic name, it's a tool for understanding history, not assigning fault.

## Shortlog: Contributor Summary

### Example: See commits grouped by author

```bash
git shortlog -sn
```

```
    15  Dariush Abbasi
     3  Jane Doe
     1  Bob Smith
```

## Comparing Points in Time

### Example: Diff between two commits

```bash
git diff a1b2c3d..e4f5a6b
```

### Example: Diff between two branches

```bash
git diff main..feature/login
```

### Example: What changed in the last 3 commits?

```bash
git diff HEAD~3..HEAD
```

### Example: Just show file names that changed

```bash
git diff --name-only HEAD~3..HEAD
```

```
index.js
README.md
```

---

[← Chapter 2: The Basics](02-the-basics.md) · [Next: Chapter 4 — Undoing Things →](04-undoing-things.md)
