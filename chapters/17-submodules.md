# Chapter 17 — Submodules

Submodules let you include one Git repository inside another, pinned to a specific commit.

## When to Use Submodules

Common use cases: shared libraries, vendor dependencies, monorepo-like setups where components have independent release cycles.

## Adding a Submodule

### Example: Add a submodule

```bash
git submodule add https://github.com/example/shared-lib.git libs/shared
```

```
Cloning into '/home/you/project/libs/shared'...
done.
```

```bash
git status
```

```
Changes to be committed:
        new file:   .gitmodules
        new file:   libs/shared
```

### Example: See the .gitmodules file

```bash
cat .gitmodules
```

```ini
[submodule "libs/shared"]
    path = libs/shared
    url = https://github.com/example/shared-lib.git
```

```bash
git commit -m "Add shared-lib submodule"
```

🧠 **What happened?** Git recorded the submodule's URL and the exact commit it points to. The parent repo doesn't store the submodule's files — it stores a pointer.

## Cloning a Repo with Submodules

### Example: Clone and initialize submodules

```bash
git clone --recurse-submodules https://github.com/boringcollege/project.git
```

Or if you already cloned:

```bash
git submodule init
git submodule update
```

Or in one command:

```bash
git submodule update --init --recursive
```

## Updating a Submodule

### Example: Pull latest changes in a submodule

```bash
cd libs/shared
git fetch
git checkout v2.0.0
cd ../..
git add libs/shared
git commit -m "Update shared-lib to v2.0.0"
```

### Example: Update all submodules to their latest remote commit

```bash
git submodule update --remote
```

🧠 **What happened?** Each submodule is an independent repo. You update it like any repo, then commit the new pointer in the parent.

## Checking Submodule Status

### Example: See which commit each submodule is on

```bash
git submodule status
```

```
 a1b2c3d4e5f6 libs/shared (v2.0.0)
```

## Removing a Submodule

There's no single command. Here are the steps:

```bash
# 1. Remove from .gitmodules
git config -f .gitmodules --remove-section submodule.libs/shared

# 2. Remove from .git/config
git config --remove-section submodule.libs/shared

# 3. Remove the tracked directory
git rm --cached libs/shared

# 4. Remove the submodule directory
rm -rf libs/shared

# 5. Remove the submodule's .git data
rm -rf .git/modules/libs/shared

# 6. Commit
git commit -m "Remove shared-lib submodule"
```

## Common Pitfalls

**Detached HEAD**: Submodules are always checked out in detached HEAD state. If you want to make changes, create a branch first:

```bash
cd libs/shared
git switch -c my-changes
```

**Forgetting to push submodule changes**: If you commit a new submodule pointer in the parent but forget to push the submodule's commits, collaborators will get errors. Always push the submodule first, then the parent.

```bash
cd libs/shared
git push
cd ../..
git push
```

---

[← Chapter 16: Worktrees](16-worktrees.md) · [Next: Chapter 18 — Branching Strategies →](18-branching-strategies.md)
