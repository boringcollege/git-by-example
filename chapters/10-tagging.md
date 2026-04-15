# Chapter 10 — Tagging

Tags mark specific points in history — usually releases.

## Types of Tags

Git has two kinds of tags:

- **Lightweight**: just a pointer to a commit (like a branch that doesn't move).
- **Annotated**: a full Git object with a tagger name, date, message, and optional GPG signature.

Use annotated tags for releases. Use lightweight tags for personal bookmarks.

## Creating Tags

### Example: Annotated tag

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
```

### Example: Lightweight tag

```bash
git tag v1.0.0-beta
```

### Example: Tag an older commit

```bash
git tag -a v0.9.0 -m "Retroactive tag for beta" a1b2c3d
```

## Listing Tags

### Example: List all tags

```bash
git tag
```

```
v0.9.0
v1.0.0
v1.0.0-beta
```

### Example: Filter tags

```bash
git tag -l "v1.*"
```

```
v1.0.0
v1.0.0-beta
```

### Example: See tag details

```bash
git show v1.0.0
```

```
tag v1.0.0
Tagger: Dariush Abbasi <dariush@example.com>
Date:   Mon Mar 10 15:00:00 2025 +0330

Release version 1.0.0

commit e4f5a6b...
```

## Pushing Tags

Tags are **not** pushed by default.

### Example: Push a single tag

```bash
git push origin v1.0.0
```

### Example: Push all tags

```bash
git push origin --tags
```

## Deleting Tags

### Example: Delete a local tag

```bash
git tag -d v1.0.0-beta
```

### Example: Delete a remote tag

```bash
git push origin --delete v1.0.0-beta
```

## Checking Out a Tag

### Example: Look at a tagged version

```bash
git checkout v1.0.0
```

```
Note: switching to 'v1.0.0'.
You are in 'detached HEAD' state.
```

🧠 **What happened?** You can look at the code as it was at `v1.0.0`, but you're in detached HEAD state. To make changes from here, create a branch: `git switch -c hotfix/v1.0.1`.

---

[← Chapter 9: Stashing](09-stashing.md) · [Next: Chapter 11 — Cherry-Picking →](11-cherry-picking.md)
