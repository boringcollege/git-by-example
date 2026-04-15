# Appendix B — .gitignore Patterns

## How .gitignore Works

Each line in `.gitignore` is a pattern. Git ignores matching files.

```
# This is a comment
*.log           # Ignore all .log files
!important.log  # But NOT this one
/build          # Ignore build/ in root only
build/          # Ignore any directory named build
**/temp         # Ignore temp anywhere in the tree
doc/**/*.pdf    # Ignore PDFs in doc/ subdirectories
```

## Pattern Syntax

```
Pattern            Matches
───────────────────────────────────────────
*.ext              Any file with that extension
dir/               A directory (and its contents)
/dir               Only in the repo root
**/pattern         At any depth
pattern/**         Everything inside pattern/
!pattern           Negate (un-ignore) a previous rule
?                  Any single character
[abc]              Any character in the set
[0-9]              Any digit
```

## Common .gitignore Templates

### Node.js

```gitignore
node_modules/
dist/
build/
.env
.env.local
*.log
npm-debug.log*
.DS_Store
coverage/
```

### Python

```gitignore
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/
.env
*.egg
.pytest_cache/
.mypy_cache/
```

### Java

```gitignore
*.class
*.jar
*.war
target/
.gradle/
build/
.idea/
*.iml
```

### Go

```gitignore
bin/
vendor/
*.exe
*.test
*.out
```

### Rust

```gitignore
target/
Cargo.lock  # only for libraries, keep for binaries
```

### General / IDE

```gitignore
# macOS
.DS_Store
.AppleDouble
.LSOverride

# Windows
Thumbs.db
desktop.ini

# Linux
*~
.nfs*

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~
.project
.classpath
.settings/

# Environment
.env
.env.local
.env.*.local
```

## Global .gitignore

Set a global ignore file for patterns that apply to all your repos:

```bash
git config --global core.excludesfile ~/.gitignore_global
```

```bash
# ~/.gitignore_global
.DS_Store
Thumbs.db
*.swp
.idea/
.vscode/
```

## Ignoring Already-Tracked Files

`.gitignore` only affects untracked files. To ignore a file that's already tracked:

```bash
git rm --cached filename
echo "filename" >> .gitignore
git commit -m "Stop tracking filename"
```

## Debugging .gitignore

### Example: Check why a file is ignored

```bash
git check-ignore -v path/to/file
```

```
.gitignore:3:*.log    debug.log
```

This tells you which rule in which file is causing the ignore.

## Resources

The [github/gitignore](https://github.com/github/gitignore) repository has comprehensive `.gitignore` templates for virtually every language and framework.
