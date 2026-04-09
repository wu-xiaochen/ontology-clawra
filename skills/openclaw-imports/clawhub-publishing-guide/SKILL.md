---
name: clawhub-publishing-guide
description: ClawHub skill publishing guide - avoid common pitfalls when publishing skills to ClawHub. Covers YAML format requirements, git LFS issues, version management, and step-by-step publish workflow.
metadata:
  openclaw:
    emoji: "📦"
    version: "1.0.0"
    last_updated: "2026-04-09"
---

# ClawHub Publishing Guide

Publishing skills to ClawHub requires specific format compliance. This guide documents common pitfalls and the correct workflow.

## Common Errors & Solutions

### Error: `--version must be valid semver`

**Cause**: YAML metadata format is incorrect. ClawHub's YAML parser doesn't accept JSON-style objects.

**Wrong (JSON-style)**:
```yaml
metadata:
  {
    "openclaw": {
      "version": "1.0.0"
    }
  }
```

**Correct (YAML-style)**:
```yaml
metadata:
  openclaw:
    version: "1.0.0"
```

### Error: `git-lfs died of signal 9`

**Cause**: A `.gitattributes` file with LFS directives is interfering with git operations.

**Solution**:
```bash
rm -f .gitattributes
git add .
git commit -m "message"
git push origin main
```

### Error: `git: 'credential-gh' is not a git command`

**Cause**: Incorrect credential helper configuration.

**Solution**:
```bash
git config credential.helper "gh auth git-credential"
```

## Version Management

### Required: Sync _meta.json and SKILL.md

Both files must have the same version number:

**SKILL.md** (metadata section):
```yaml
metadata:
  openclaw:
    version: "1.0.0"  # Must match _meta.json
```

**_meta.json**:
```json
{
  "ownerId": "your-owner-id",
  "slug": "skill-name",
  "version": "1.0.0",  # Must match SKILL.md
  "publishedAt": 1234567890000
}
```

### Version Bump Script

```python
import json
from datetime import datetime

def bump_version(version_file, skill_md_file):
    # Read current version
    with open(version_file) as f:
        meta = json.load(f)
    current = meta["version"]
    
    # Bump patch version
    parts = current.split(".")
    new_version = f"{parts[0]}.{parts[1]}.{int(parts[2]) + 1}"
    
    # Update _meta.json
    meta["version"] = new_version
    meta["publishedAt"] = int(datetime.now().timestamp() * 1000)
    with open(version_file, "w") as f:
        json.dump(meta, f, indent=2)
    
    # Update SKILL.md
    with open(skill_md_file) as f:
        content = f.read()
    content = content.replace(f'version: "{current}"', f'version: "{new_version}"')
    content = content.replace(f'"version": "{current}"', f'"version": "{new_version}"')
    with open(skill_md_file, "w") as f:
        f.write(content)
    
    return new_version
```

## Step-by-Step Publish Workflow

```bash
# 1. Ensure clean git state (remove problematic .gitattributes)
rm -f .gitattributes

# 2. Sync versions between _meta.json and SKILL.md
# (Use the script above or do manually)

# 3. Commit changes
git add .
git commit -m "feat: skill-name v1.0.0"

# 4. Push to GitHub (if using gh auth)
git config credential.helper "gh auth git-credential"
git push origin main

# 5. Publish to ClawHub
clawhub publish /path/to/skill --version 1.0.0 --changelog "Release notes"
```

## YAML Frontmatter Format

SKILL.md must have valid YAML frontmatter:

```yaml
---
name: skill-name
description: Brief description of what the skill does
metadata:
  openclaw:
    emoji: "🔧"
    version: "1.0.0"
    last_updated: "2026-04-09"
---

# Skill Title

Skill content here...
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `--version must be valid semver` | Fix YAML metadata format |
| `git-lfs died of signal 9` | Remove .gitattributes file |
| `Version already exists` | Bump to new version |
| ClawHub timeout | Retry with longer timeout |
| `git: 'credential-gh' is not a git command` | Use `gh auth git-credential` |
