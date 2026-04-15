# Chapter 19 — Writing Good Commit Messages

Good commit messages make your project's history useful. Bad ones make it noise.

## The Format

```
<type>: <short summary> (50 chars or less)

<optional body — wrap at 72 chars>
Explain WHAT changed and WHY, not HOW.

<optional footer>
Refs: #123
Co-authored-by: Jane Doe <jane@example.com>
```

## The Seven Rules

1. Separate subject from body with a blank line.
2. Limit the subject line to 50 characters.
3. Capitalize the subject line.
4. Do not end the subject line with a period.
5. Use the imperative mood ("Add feature" not "Added feature").
6. Wrap the body at 72 characters.
7. Use the body to explain *what* and *why*, not *how*.

### Example: Good commit messages

```
Add rate limiting to login endpoint

Without rate limiting, the login endpoint was vulnerable to brute-force
attacks. This adds a sliding window rate limiter that allows 5 attempts
per minute per IP address.

Refs: #247
```

```
Fix crash when user has no profile photo

The avatar component assumed a non-null photo URL. Users who never
uploaded a photo triggered a TypeError. This adds a fallback to a
default avatar.
```

```
Upgrade React from 18.2 to 19.0

Breaking changes addressed:
- Replaced legacy context API usage in ThemeProvider
- Updated all class components to function components
- Removed deprecated lifecycle methods

See: https://react.dev/blog/2024/12/05/react-19
```

### Example: Bad commit messages

```
fix bug                          ← What bug? Where?
update                           ← Update what?
WIP                              ← Don't commit WIP to shared branches
changes                          ← Meaningless
fix review comments              ← Which comments? What changed?
asdfasdf                         ← Come on
```

## Conventional Commits

A widely adopted convention that adds a type prefix:

```
feat: add user registration
fix: prevent crash on empty input
docs: update API reference
style: format code with prettier
refactor: extract validation logic
test: add tests for login flow
chore: update dependencies
perf: cache database queries
ci: add GitHub Actions workflow
build: switch from webpack to vite
```

### Example: With scope

```
feat(auth): add two-factor authentication
fix(api): handle timeout errors gracefully
docs(readme): add installation instructions
```

### Example: Breaking change

```
feat(api)!: change response format to JSON:API

BREAKING CHANGE: All API responses now follow the JSON:API spec.
The old format is no longer supported. See migration guide at
docs/migration-v3.md
```

## The Imperative Mood Test

Your subject line should complete this sentence:

> "If applied, this commit will **___your subject line here___**."

- ✅ "If applied, this commit will **add rate limiting to login endpoint**."
- ✅ "If applied, this commit will **fix crash when user has no profile photo**."
- ❌ "If applied, this commit will **fixed a bug**."
- ❌ "If applied, this commit will **some changes**."

## Commit Atomicity

Each commit should be one logical change. If you can describe a commit as "X **and** Y," it should probably be two commits.

```bash
# Bad: one commit doing two things
git commit -m "Fix login bug and add dark mode"

# Good: two focused commits
git commit -m "Fix login redirect after session timeout"
git commit -m "Add dark mode toggle to settings page"
```

Use `git add -p` (see [Chapter 2](02-the-basics.md)) to stage parts of a file when you've made multiple unrelated changes.

---

[← Chapter 18: Branching Strategies](18-branching-strategies.md) · [Next: Chapter 20 — Git Hooks →](20-git-hooks.md)
