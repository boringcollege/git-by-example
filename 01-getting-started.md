# Chapter 1 — Getting Started

## Installing Git

### macOS

```bash
# Option 1: Xcode Command Line Tools (easiest)
xcode-select --install

# Option 2: Homebrew
brew install git
```

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install git
```

### Linux (Fedora)

```bash
sudo dnf install git
```

### Windows

Download the installer from [git-scm.com](https://git-scm.com/download/win), or use:

```powershell
winget install Git.Git
```

### Verify Installation

```bash
git --version
```

```
git version 2.44.0
```

## Configuring Git

Before your first commit, tell Git who you are.

### Example: Set your identity

```bash
git config --global user.name "Dariush Abbasi"
git config --global user.email "dariush@example.com"
```

🧠 **What happened?** Git wrote these values to `~/.gitconfig`. Every commit you make will be stamped with this name and email.

### Example: See your config

```bash
git config --list
```

```
user.name=Dariush Abbasi
user.email=dariush@example.com
```

### Example: Set your default editor

```bash
git config --global core.editor "vim"
```

Other popular choices: `"code --wait"` (VS Code), `"nano"`, `"subl -n -w"` (Sublime Text).

### Example: Set default branch name

```bash
git config --global init.defaultBranch main
```

🧠 **What happened?** New repositories you create with `git init` will use `main` instead of `master` as the default branch name.

## Creating Your First Repository

### Example: Initialize a new repo

```bash
mkdir my-project
cd my-project
git init
```

```
Initialized empty Git repository in /home/you/my-project/.git/
```

### Example: See what Git created

```bash
ls -la .git/
```

```
drwxr-xr-x  HEAD
drwxr-xr-x  config
drwxr-xr-x  hooks/
drwxr-xr-x  objects/
drwxr-xr-x  refs/
```

🧠 **What happened?** Git created a hidden `.git/` directory. This single folder *is* your repository — all history, branches, and configuration live inside it. Your working directory is just a checkout of one version.

## Cloning an Existing Repository

### Example: Clone a repo from GitHub

```bash
git clone https://github.com/boringcollege/git-by-example.git
cd git-by-example
```

```
Cloning into 'git-by-example'...
remote: Enumerating objects: 42, done.
remote: Total 42 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (42/42), done.
```

🧠 **What happened?** Git downloaded the entire repository — all files, all branches, all history — to your machine. You now have a full, independent copy.

---

[Next: Chapter 2 — The Basics →](02-the-basics.md)
