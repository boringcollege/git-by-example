# Chapter 13 — Git Internals: Objects & Refs

Understanding Git's internals makes everything else click. Git is, at its core, a content-addressable filesystem with a version control system built on top.

## The Four Object Types

Everything in Git is stored as one of four types of objects:

```
blob    → file contents (no filename, just data)
tree    → directory listing (filenames + pointers to blobs/trees)
commit  → snapshot (pointer to tree + author + message + parent)
tag     → annotated tag (pointer to commit + tagger + message)
```

## Exploring Objects

### Example: See the type of an object

```bash
git cat-file -t HEAD
```

```
commit
```

### Example: See the content of a commit

```bash
git cat-file -p HEAD
```

```
tree 4b825dc642cb6eb9a060e54bf899d15d2cb1b5d6
parent a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
author Dariush Abbasi <dariush@example.com> 1710072720 +0330
committer Dariush Abbasi <dariush@example.com> 1710072720 +0330

Add greet function
```

### Example: See a tree object

```bash
git cat-file -p HEAD^{tree}
```

```
100644 blob a906cb2a4a904a152e80877d4088654daad0c859    .gitignore
100644 blob 1f7a7a472abf3dd9643fd615f6da379c4acb3e3a    README.md
100644 blob 5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e    index.js
```

### Example: See a blob (file contents)

```bash
git cat-file -p 5d6e7f8
```

```
console.log('hello');
function greet() { return 'hi'; }
```

🧠 **What happened?** A blob stores raw file content. It has no filename — the tree object maps filenames to blobs.

## How SHA Hashes Work

Every object is identified by a SHA-1 hash of its content.

### Example: Hash a file manually

```bash
echo -n "hello" | git hash-object --stdin
```

```
ce013625030ba8dba906f756967f9e9ca394464a
```

### Example: Store an object

```bash
echo "hello world" | git hash-object -w --stdin
```

```
95d09f2b10159347eece71399a7e2e907ea3df4f
```

🧠 **What happened?** `-w` actually writes the object to `.git/objects/`. The hash is derived from the content, so identical content always produces the same hash.

## Where Objects Live

```bash
find .git/objects -type f | head -5
```

```
.git/objects/95/d09f2b10159347eece71399a7e2e907ea3df4f
.git/objects/ce/013625030ba8dba906f756967f9e9ca394464a
.git/objects/a9/06cb2a4a904a152e80877d4088654daad0c859
```

Objects are stored in directories named by the first two characters of their hash.

## Refs: Named Pointers

Branches and tags are just files containing a commit hash.

### Example: See what a branch points to

```bash
cat .git/refs/heads/main
```

```
e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3
```

### Example: See what HEAD points to

```bash
cat .git/HEAD
```

```
ref: refs/heads/main
```

🧠 **What happened?** A branch is literally a 41-byte file (40 hex chars + newline). HEAD is a symbolic ref that usually points to a branch. That's why branching in Git is so fast — there's nothing to copy.

## The Commit Graph

Commits form a directed acyclic graph (DAG). Each commit points to its parent(s):

```
a1b2c3d  ←  e4f5a6b  ←  f7g8h9i  ←  h8i9j0k
  │                                      │
  └──────────────── g6h7i8j ─────────────┘
                  (second parent of merge commit)
```

Understanding this graph is the key to understanding `merge`, `rebase`, `reset`, and `cherry-pick`.

---

[← Chapter 12: Interactive Rebase](12-interactive-rebase.md) · [Next: Chapter 14 — Reflog →](14-reflog.md)
