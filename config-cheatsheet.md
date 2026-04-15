# Appendix A — Git Configuration Cheatsheet

## Configuration Levels

```bash
git config --system   # /etc/gitconfig        (all users)
git config --global   # ~/.gitconfig           (your user)
git config --local    # .git/config            (this repo only)
```

Local overrides global, which overrides system.

## Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Editor

```bash
git config --global core.editor "vim"
git config --global core.editor "code --wait"       # VS Code
git config --global core.editor "nano"
git config --global core.editor "subl -n -w"        # Sublime Text
```

## Default Branch

```bash
git config --global init.defaultBranch main
```

## Line Endings

```bash
# On macOS/Linux
git config --global core.autocrlf input

# On Windows
git config --global core.autocrlf true
```

## Merge & Diff Tools

```bash
git config --global merge.tool vimdiff
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'
```

## Pull Behavior

```bash
# Rebase by default (cleaner history)
git config --global pull.rebase true

# Only allow fast-forward pulls
git config --global pull.ff only
```

## Push Behavior

```bash
# Push only the current branch
git config --global push.default current

# Auto set upstream when pushing a new branch
git config --global push.autoSetupRemote true
```

## Colors

```bash
git config --global color.ui auto
```

## Credential Caching

```bash
# Cache credentials in memory for 1 hour
git config --global credential.helper 'cache --timeout=3600'

# On macOS, use Keychain
git config --global credential.helper osxkeychain

# On Windows, use Credential Manager
git config --global credential.helper manager
```

## Useful Misc Settings

```bash
# Show untracked files in subdirectories
git config --global status.showUntrackedFiles all

# Enable rerere (reuse recorded resolution)
git config --global rerere.enabled true

# Auto-correct typos (with 0.5s delay)
git config --global help.autocorrect 5

# Use histogram diff algorithm (better output)
git config --global diff.algorithm histogram

# Sign commits with GPG
git config --global commit.gpgsign true
git config --global user.signingkey YOUR_GPG_KEY_ID
```

## View All Settings

```bash
git config --list --show-origin
```

This shows every setting and which file it comes from.
