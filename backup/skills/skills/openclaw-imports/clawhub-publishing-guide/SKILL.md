---
name: clawhub-publishing-guide
description: ClawHub skill publishing guide - avoid common pitfalls when publishing skills to ClawHub. Covers YAML format requirements, git LFS issues, version management, and step-by-step publish workflow.
metadata:
  openclaw:
    emoji: "📦"
    version: "1.1.0"
    last_updated: "2026-04-10"
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

**Cause**: Incorrect credential helper configuration. The `gh auth git-credential` is the correct one (not `credential-gh`).

**Solution**:
```bash
git config credential.helper "gh auth git-credential"
```

**Note**: Even if this errors, git push may still work if you have SSH keys or other auth configured. The push in this case succeeded using SSH authentication despite the error message.

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

## auto_enhancer.py Known Bug

**Issue**: auto_enhancer.py does NOT update SKILL.md's version field when bumping versions. It only updates:
- `_meta.json` (version and publishedAt)
- `CHANGELOG.md` (new entry)

This causes version drift: local `_meta.json` shows v4.0.1 but `SKILL.md` still shows v4.0.0.

**Impact**: Version inconsistency between files, confusing state.

**Fix needed**: When auto_enhancer bumps version, it should also update the version in SKILL.md frontmatter.

**Workaround**: After auto_enhancer runs, manually sync SKILL.md or use `clawhub update <slug> --force` to pull ClawHub's latest.

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

### Error: `Version already exists`

**Cause**: Two scenarios:
1. You tried to republish the same version (simple — just bump)
2. ClawHub already has a **newer** version than you're trying to publish (e.g., ClawHub has v4.0.2 but your local is v4.0.1)

**Solution for scenario 2** (ClawHub ahead of local):
```bash
# Check what's on ClawHub
clawhub inspect <slug>

# Sync to ClawHub's latest version
clawhub update <slug> --force
```

**Why this happens**: auto_enhancer.py only updates `_meta.json` and `CHANGELOG.md`, not `SKILL.md`. This causes version drift where local is behind but doesn't realize it.

### Error: `Path must be a folder`

**Cause**: `clawhub publish` expects a folder path, not a skill name.

**Solution**:
```bash
# Correct
clawhub publish /path/to/skill-folder

# For ontology-clawra specifically
cd ~/.hermes/skills/openclaw-imports/ontology-clawra
clawhub publish .
```

### Error: `--version must be valid semver` (even with valid version)

**Cause**: The folder you're publishing from doesn't contain a valid skill structure.

**Solution**: Ensure you're in the skill folder with SKILL.md, _meta.json, etc.

| Error | Solution |
|-------|----------|
| `--version must be valid semver` | Fix YAML metadata format; ensure you're in the correct folder |
| `git-lfs died of signal 9` | Remove .gitattributes file |
| `Version already exists` (local behind) | Use `clawhub update <slug> --force` to sync |
| `Version already exists` (local same) | Bump to new version manually |
| ClawHub timeout | Retry with longer timeout |
| `git: 'credential-gh' is not a git command` | Use `gh auth git-credential` |
| `Path must be a folder` | Use `.` or full path to skill folder, not slug name |
