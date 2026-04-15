# Chapter 8 — Working with Remotes

A remote is a copy of your repository hosted somewhere else — usually GitHub, GitLab, or Bitbucket.

## Listing Remotes

### Example: See configured remotes

```bash
git remote -v
```

```
origin  https://github.com/boringcollege/git-by-example.git (fetch)
origin  https://github.com/boringcollege/git-by-example.git (push)
```

🧠 **What happened?** `origin` is the default name for the remote you cloned from. You can have multiple remotes.

## Adding and Removing Remotes

### Example: Add a remote

```bash
git remote add upstream https://github.com/original-author/project.git
```

### Example: Remove a remote

```bash
git remote remove upstream
```

### Example: Rename a remote

```bash
git remote rename origin github
```

## Fetching

Fetch downloads new data from the remote but does **not** change your working files.

### Example: Fetch from origin

```bash
git fetch origin
```

```
remote: Enumerating objects: 5, done.
remote: Total 3 (delta 1), reused 3 (delta 1)
Unpacking objects: 100% (3/3), done.
From https://github.com/boringcollege/git-by-example
   a1b2c3d..d4e5f6g  main       -> origin/main
```

### Example: See what's new

```bash
git log main..origin/main --oneline
```

```
d4e5f6g Fix typo in README
c3d4e5f Add contributing guidelines
```

🧠 **What happened?** `git fetch` updated your remote-tracking branches (`origin/main`) without touching your local `main`. You can inspect the changes before deciding to integrate them.

## Pulling

Pull = fetch + merge (or fetch + rebase).

### Example: Pull with merge (default)

```bash
git pull origin main
```

### Example: Pull with rebase (cleaner history)

```bash
git pull --rebase origin main
```

### Example: Set rebase as default for pull

```bash
git config --global pull.rebase true
```

## Pushing

### Example: Push to the remote

```bash
git push origin main
```

### Example: Push a new branch

```bash
git switch -c feature/dark-mode
# ... make commits ...
git push -u origin feature/dark-mode
```

```
Branch 'feature/dark-mode' set up to track remote branch 'feature/dark-mode' from 'origin'.
```

🧠 **What happened?** `-u` (or `--set-upstream`) links your local branch to the remote branch. After this, you can just run `git push` without specifying the remote and branch.

### Example: Push rejected (remote has new commits)

```bash
git push origin main
```

```
! [rejected]        main -> main (fetch first)
error: failed to push some refs
hint: Updates were rejected because the remote contains work that you do not have locally.
```

Fix: pull first, then push.

```bash
git pull --rebase origin main
git push origin main
```

### Example: Force push (after rebase)

```bash
git push --force-with-lease origin feature/my-branch
```

🧠 **What happened?** `--force-with-lease` is a safer force push. It refuses to overwrite the remote if someone else has pushed commits you haven't seen. Use it instead of `--force`.

## Tracking Branches

### Example: See which local branches track which remote branches

```bash
git branch -vv
```

```
  feature/login  f7g8h9i [origin/feature/login] Add login page
* main           e4f5a6b [origin/main] Add greet function
```

### Example: Set up tracking for an existing branch

```bash
git branch --set-upstream-to=origin/main main
```

---

[← Chapter 7: Rebasing](07-rebasing.md) · [Next: Chapter 9 — Stashing →](09-stashing.md)
