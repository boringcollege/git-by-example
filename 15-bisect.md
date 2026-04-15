# Chapter 15 — Bisect: Finding Bugs

`git bisect` uses binary search to find the exact commit that introduced a bug.

## How It Works

You tell Git one "good" commit (where the bug didn't exist) and one "bad" commit (where the bug exists). Git checks out the midpoint and asks: good or bad? It keeps halving until it finds the exact commit.

With 1,000 commits between good and bad, bisect finds the culprit in about 10 steps.

## Manual Bisect

### Example: Find the commit that broke the tests

```bash
# Start bisecting
git bisect start

# Current commit is broken
git bisect bad

# This older commit was fine
git bisect good v1.0.0
```

```
Bisecting: 15 revisions left to test after this (roughly 4 steps)
[c3d4e5f] Add caching layer
```

Git checks out a commit in the middle. Test it:

```bash
# Run your tests
npm test

# If tests pass:
git bisect good

# If tests fail:
git bisect bad
```

Repeat until Git narrows it down:

```
b2c3d4e is the first bad commit
commit b2c3d4e
Author: Someone <someone@example.com>
Date:   Mon Mar 10 2025

    Refactor database queries
```

### Example: End the bisect session

```bash
git bisect reset
```

This returns you to the branch you were on before bisecting.

## Automated Bisect

If you have a script or test that can determine good/bad automatically, let Git run it for you.

### Example: Bisect with a test script

```bash
git bisect start HEAD v1.0.0
git bisect run npm test
```

```
running 'npm test'...
...
b2c3d4e is the first bad commit
```

### Example: Bisect with a custom script

```bash
git bisect start HEAD v1.0.0
git bisect run ./test-bug.sh
```

The script must exit with code `0` for good and `1` (or `125` to skip) for bad.

### Example: test-bug.sh

```bash
#!/bin/bash
# Check if the specific bug exists
grep -q "broken_function" app.js && exit 1 || exit 0
```

## Skipping a Commit

Sometimes a commit can't be tested (doesn't compile, for example):

```bash
git bisect skip
```

Git will try a nearby commit instead.

## Viewing Bisect Log

### Example: See the bisect history

```bash
git bisect log
```

```
git bisect start
# bad: [e4f5a6b] HEAD
git bisect bad e4f5a6b
# good: [a1b2c3d] v1.0.0
git bisect good a1b2c3d
# good: [c3d4e5f] Add caching layer
git bisect good c3d4e5f
# bad: [d4e5f6g] Update dependencies
git bisect bad d4e5f6g
```

---

[← Chapter 14: Reflog](14-reflog.md) · [Next: Chapter 16 — Worktrees →](16-worktrees.md)
