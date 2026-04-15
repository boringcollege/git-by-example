# Chapter 18 — Branching Strategies

A branching strategy is a convention your team agrees on for how branches are created, named, and merged.

## Git Flow

The classic model. Good for software with scheduled releases.

```
main ─────────●─────────────────────●──────── (production releases)
               \                   /
release/1.0 ────●───●─────────────● ── (stabilization)
                     \           /
develop ──●──●──●──●──●──●──●──●──●──●── (integration)
           \      /    \      /
feature/a   ●──●──●     ●──●──●  feature/b
```

Branches:
- `main` — always production-ready, tagged with version numbers.
- `develop` — integration branch for the next release.
- `feature/*` — branch off `develop`, merge back to `develop`.
- `release/*` — branch off `develop` for stabilization, merge to `main` and `develop`.
- `hotfix/*` — branch off `main` for urgent fixes, merge to `main` and `develop`.

### Example: Git Flow workflow

```bash
# Start a feature
git switch develop
git switch -c feature/user-profile

# Work on the feature
git commit -m "Add profile page"
git commit -m "Add avatar upload"

# Merge back to develop
git switch develop
git merge --no-ff feature/user-profile
git branch -d feature/user-profile
```

## GitHub Flow

Simpler. Good for teams that deploy continuously.

```
main ──●──●──●──●──●──●──●──●── (always deployable)
        \      /    \      /
feature  ●──●──●     ●──●──●
         (PR + review)
```

Rules:
1. `main` is always deployable.
2. Branch off `main` for every change.
3. Open a pull request.
4. After review and CI passes, merge to `main`.
5. Deploy immediately.

### Example: GitHub Flow workflow

```bash
# Start work
git switch -c feature/dark-mode
git commit -m "Add dark mode toggle"
git push -u origin feature/dark-mode

# Open a PR on GitHub, get reviews, then merge via the UI
# After merge:
git switch main
git pull
git branch -d feature/dark-mode
```

## Trunk-Based Development

Even simpler. Everyone commits to `main` (the trunk) with short-lived branches.

```
main ──●──●──●──●──●──●──●──●──●──●──●── (continuous)
        \  /       \  /
        ●──●       ●  (short-lived, <1 day)
```

Rules:
1. Branches live for hours, not days.
2. Everyone integrates to `main` at least once a day.
3. Feature flags hide incomplete work.
4. CI/CD is mandatory.

### Example: Trunk-based workflow

```bash
git switch -c fix/button-color
git commit -m "Fix button color on mobile"
git push -u origin fix/button-color
# PR reviewed and merged same day
```

## Which Strategy Should You Use?

```
Team Size        Release Cadence       Strategy
──────────────────────────────────────────────────
1-3 people       Continuous            Trunk-based or GitHub Flow
3-10 people      Weekly/biweekly       GitHub Flow
10+ people       Scheduled releases    Git Flow
Any size         Regulated/audited     Git Flow (for traceability)
```

There's no universally correct answer. Pick the simplest strategy that works for your team and change it when it stops working.

## Branch Naming Conventions

Whatever strategy you choose, use consistent names:

```
feature/user-authentication
bugfix/login-redirect
hotfix/security-patch
release/2.1.0
chore/update-dependencies
docs/api-reference
```

---

[← Chapter 17: Submodules](17-submodules.md) · [Next: Chapter 19 — Writing Good Commit Messages →](19-commit-messages.md)
