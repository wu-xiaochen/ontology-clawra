---
name: git-https-push-with-token
description: Git push to HTTPS remote using token authentication — avoids SSH setup, works in CI/automated environments.
triggers:
  - git push fails with "authentication failed"
  - HTTPS token embedded in URL but push still asks for credentials
  - git credential.helper interfering with URL-embedded auth
---

# Git HTTPS Push with Token Authentication

## The Problem

Git push to an HTTPS remote fails even when the token is embedded in the URL:
```
remote: authentication failed
fatal: Authentication failed for 'https://github.com/user/repo.git'
```

## Key Insight (Gotcha)

**Setting `credential.helper` overrides URL-embedded credentials.**

Git's credential helper runs *before* the URL-embedded token is used. If `credential.helper` is configured, git uses that instead of the token in the URL.

## Correct Approach

```bash
# 1. Set remote URL with token embedded (no trailing spaces or special chars)
git remote set-url origin "https://github.com/USER/REPO.git"
# Actually embed token:
git remote set-url origin "https://GITHUB_TOKEN@github.com/USER/REPO.git"

# 2. CRITICAL: Remove/override any credential helper that would override URL token
git config --unset credential.helper    # Remove global/default helper

# 3. Now push will use the URL-embedded token
git push origin main
```

## Alternative: Store credentials persistently

```bash
# Store credentials in a file (note: writes token in plain text)
git config credential.helper "store --file ~/.git-credentials"
echo "https://GITHUB_TOKEN@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

git push origin main
```

## Checklist When Push Asks for Password

- [ ] Token has correct permissions (repo scope for private repos)
- [ ] Token not expired or revoked
- [ ] URL is correct (not truncated, no extra chars)
- [ ] `credential.helper` is unset or points to a store that has the right credentials
- [ ] `git remote -v` shows the expected URL with token

## Debug

```bash
# See what git thinks the remote URL is
git remote -v

# See what credential helper is configured (global + local)
git config --list --show-origin | grep credential

# Test if credential helper is interfering
GIT_TRACE=1 git push origin main 2>&1 | grep -i credential
```
