# Chapter 21 — Tips & Tricks

A collection of useful Git techniques that don't fit neatly into other chapters.

## Aliases

### Example: Set up useful aliases

```bash
git config --global alias.st "status -sb"
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.ci "commit"
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "restore --staged"
git config --global alias.amend "commit --amend --no-edit"
```

Now you can type:

```bash
git st        # instead of git status -sb
git lg        # beautiful graph log
git unstage file.js
```

## Ignoring Files Locally

### Example: Ignore a file without changing .gitignore

```bash
echo "my-local-notes.txt" >> .git/info/exclude
```

🧠 `.git/info/exclude` works like `.gitignore` but isn't tracked, so it's private to your machine.

### Example: Temporarily ignore a tracked file

```bash
git update-index --assume-unchanged config/local.yml
```

Undo it:

```bash
git update-index --no-assume-unchanged config/local.yml
```

## Finding Things

### Example: Find which commit deleted a file

```bash
git log --diff-filter=D --summary -- path/to/deleted-file.js
```

### Example: Find all commits by a specific author

```bash
git log --author="Dariush" --oneline
```

### Example: Find all commits touching a specific function

```bash
git log -p -S "calculateTotal" -- "*.js"
```

### Example: Find all TODO comments added recently

```bash
git diff HEAD~10..HEAD -S "TODO"
```

## Cleaning Up

### Example: Remove all merged branches

```bash
git branch --merged main | grep -v "main" | xargs git branch -d
```

### Example: Garbage collect

```bash
git gc --prune=now
```

This cleans up unnecessary files and optimizes the repository.

## Working with Large Files

### Example: See the largest files in history

```bash
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '/^blob/ {print $3, $4}' \
  | sort -rn \
  | head -10
```

### Example: Set up Git LFS for large files

```bash
git lfs install
git lfs track "*.psd"
git lfs track "*.mp4"
git add .gitattributes
git commit -m "Track large files with Git LFS"
```

## Useful One-Liners

### Example: Count commits per author

```bash
git shortlog -sn --all
```

### Example: See which files change most often

```bash
git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -10
```

### Example: See total lines added/removed by author

```bash
git log --author="Dariush" --pretty=tformat: --numstat \
  | awk '{ add += $1; del += $2 } END { printf "Added: %s Removed: %s\n", add, del }'
```

### Example: Create an archive of the current HEAD

```bash
git archive --format=tar.gz --prefix=project-v1.0/ HEAD > project-v1.0.tar.gz
```

### Example: Show a file as it was 5 commits ago

```bash
git show HEAD~5:path/to/file.js
```

## Sparse Checkout

When a repo is huge and you only need a few directories:

### Example: Clone only specific directories

```bash
git clone --filter=blob:none --sparse https://github.com/big/repo.git
cd repo
git sparse-checkout set src/frontend docs
```

🧠 **What happened?** Git cloned the repo's metadata but only downloaded files in `src/frontend` and `docs`. Everything else is downloaded on demand.

## Git Maintenance

For large repositories, enable background maintenance:

```bash
git maintenance start
```

This runs hourly tasks like prefetching, garbage collection, and commit-graph updates.

---

[← Chapter 20: Git Hooks](20-git-hooks.md) · [Back to Table of Contents →](../README.md)
