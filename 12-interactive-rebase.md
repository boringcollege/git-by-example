# Chapter 12 — Interactive Rebase

Interactive rebase lets you rewrite history: reorder, squash, edit, or drop commits before sharing them.

## Starting an Interactive Rebase

### Example: Rebase the last 4 commits

```bash
git rebase -i HEAD~4
```

Your editor opens with:

```
pick a1b2c3d Add user model
pick b2c3d4e Add user controller
pick c3d4e5f Fix typo in user model
pick d4e5f6g Add user routes
```

## The Commands

```
pick   = use commit as-is
reword = use commit, but edit the message
edit   = use commit, but stop to amend it
squash = meld into previous commit (keep message)
fixup  = meld into previous commit (discard message)
drop   = remove commit entirely
```

## Squash: Combine Commits

### Example: Squash a typo fix into the original commit

Change the file to:

```
pick a1b2c3d Add user model
fixup c3d4e5f Fix typo in user model
pick b2c3d4e Add user controller
pick d4e5f6g Add user routes
```

🧠 **What happened?** We moved the typo fix right after the original commit and changed `pick` to `fixup`. Git will combine them into one commit and discard the "Fix typo" message.

```bash
git log --oneline
```

```
g7h8i9j Add user routes
f6g7h8i Add user controller
e5f6g7h Add user model
```

Three clean commits instead of four.

## Reword: Fix a Commit Message

### Example: Change a message

```
reword a1b2c3d Add user model
pick b2c3d4e Add user controller
```

Save and close. Git will open a new editor for the commit message of `a1b2c3d`.

## Edit: Modify a Past Commit

### Example: Add a forgotten file to an old commit

```
edit a1b2c3d Add user model
pick b2c3d4e Add user controller
```

Save and close. Git stops at that commit:

```bash
# Add the forgotten file
git add user_model_test.js
git commit --amend --no-edit
git rebase --continue
```

## Reorder Commits

### Example: Change the order

Simply rearrange the lines:

```
pick d4e5f6g Add user routes
pick a1b2c3d Add user model
pick b2c3d4e Add user controller
```

⚠️ Reordering can cause conflicts if commits depend on each other.

## Drop: Remove a Commit

### Example: Delete a commit from history

```
pick a1b2c3d Add user model
drop b2c3d4e Add experimental debug logging
pick c3d4e5f Add user controller
```

Or simply delete the line entirely — same effect.

## Autosquash

If you name fixup commits with `fixup!` or `squash!` prefix, Git can organize them automatically.

### Example: Autosquash workflow

```bash
# Original commit
git commit -m "Add user model"

# Later, a fix for that commit
git commit -m "fixup! Add user model"

# Rebase with autosquash
git rebase -i --autosquash HEAD~3
```

Git automatically puts the fixup commit right after its target and marks it as `fixup`.

---

[← Chapter 11: Cherry-Picking](11-cherry-picking.md) · [Next: Chapter 13 — Git Internals →](13-git-internals.md)
