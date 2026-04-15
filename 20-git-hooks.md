# Chapter 20 — Git Hooks

Git hooks are scripts that run automatically at specific points in the Git workflow. They live in `.git/hooks/`.

## Available Hooks

```
Hook                  When It Runs
────────────────────────────────────────────────────
pre-commit            Before a commit is created
prepare-commit-msg    After default message, before editor opens
commit-msg            After you write the message (validate it)
post-commit           After a commit is created
pre-push              Before a push
pre-rebase            Before a rebase
post-merge            After a merge
post-checkout         After checkout / switch
```

## Your First Hook

### Example: pre-commit hook that runs linting

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running linter..."
npm run lint

if [ $? -ne 0 ]; then
    echo "❌ Lint failed. Fix errors before committing."
    exit 1
fi

echo "✅ Lint passed."
EOF

chmod +x .git/hooks/pre-commit
```

Now try committing:

```bash
git commit -m "Test hook"
```

```
Running linter...
✅ Lint passed.
[main a1b2c3d] Test hook
```

🧠 **What happened?** The hook ran before the commit. If it exits with a non-zero code, the commit is aborted.

### Example: commit-msg hook to enforce format

```bash
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
MSG=$(cat "$1")
PATTERN="^(feat|fix|docs|style|refactor|test|chore|perf|ci|build)(\(.+\))?: .{1,50}"

if ! echo "$MSG" | grep -qE "$PATTERN"; then
    echo "❌ Commit message does not follow Conventional Commits format."
    echo "   Expected: <type>(optional scope): <description>"
    echo "   Example:  feat(auth): add login endpoint"
    exit 1
fi
EOF

chmod +x .git/hooks/commit-msg
```

```bash
git commit -m "stuff"
```

```
❌ Commit message does not follow Conventional Commits format.
   Expected: <type>(optional scope): <description>
   Example:  feat(auth): add login endpoint
```

```bash
git commit -m "feat: add user model"
```

```
[main b2c3d4e] feat: add user model
```

### Example: pre-push hook to run tests

```bash
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
echo "Running tests before push..."
npm test

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Push aborted."
    exit 1
fi
EOF

chmod +x .git/hooks/pre-push
```

## The Problem: Hooks Aren't Shared

`.git/hooks/` is not tracked by Git, so hooks don't travel with the repository. Your teammates won't have them.

### Solution 1: Use a hooks directory in the repo

```bash
mkdir .githooks

# Move hooks there
mv .git/hooks/pre-commit .githooks/

# Tell Git to use this directory
git config core.hooksPath .githooks

# Commit the hooks
git add .githooks/
git commit -m "chore: add shared git hooks"
```

### Solution 2: Use a tool like Husky (Node.js projects)

```bash
npm install --save-dev husky
npx husky init
```

```bash
# Create a pre-commit hook
echo "npm run lint" > .husky/pre-commit
```

Now every developer who runs `npm install` gets the hooks automatically.

## Bypassing Hooks

### Example: Skip hooks for a single commit

```bash
git commit --no-verify -m "WIP: quick save"
```

### Example: Skip hooks for a push

```bash
git push --no-verify
```

⚠️ Use sparingly. If you're bypassing hooks often, the hooks might be too strict or too slow.

---

[← Chapter 19: Commit Messages](19-commit-messages.md) · [Next: Chapter 21 — Tips & Tricks →](21-tips-and-tricks.md)
