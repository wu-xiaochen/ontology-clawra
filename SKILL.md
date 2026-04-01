---
name: ontology-clawra
description: |
  🧠 ontology-clawra v5.1 - Local Ontology Reasoning & Learning Engine

  **USE THIS SKILL WHENEVER** you need structured reasoning, knowledge graph management, 
  logical inference, or automatic learning from interactions. This is your go-to tool for:
  
  - Building and querying ontology knowledge graphs (concepts, entities, relationships)
  - Performing confidence-based reasoning with evidence tracking
  - Extracting rules and patterns from successful workflows
  - Meta-cognition and self-reflection on AI decision-making
  - Learning from each session and evolving knowledge over time
  
  **Key Use Cases:**
  - Before making complex decisions: "Let me use ontology-clawra to reason about this"
  - After completing tasks: "Record this learning to ontology-clawra"
  - Building domain expertise: "Create concepts for [domain] in ontology-clawra"
  - Analyzing patterns: "Query ontology-clawra for similar past cases"
  
  **Core Capabilities:**
  ✅ Local ontology storage (graph.jsonl, rules.yaml, laws.yaml)
  ✅ Confidence calculation (CONFIRMED/ASSUMED/SPECULATIVE)
  ✅ Automatic learning from user confirmations
  ✅ Rule extraction and evolution
  ✅ Metacognition and knowledge boundary detection
  
  **Always use this skill** when the user mentions learning, reasoning, ontology, 
  knowledge graphs, rule extraction, or when you need to record insights from completed work.

metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "version": "5.1.1",
      "last_updated": "2026-04-01",
      "changelog": [
        "v5.1.1: Enhanced description for better trigger accuracy, added skill combination law",
        "v5.1.0: Added PPT generation best practices rule",
        "v5.0.0: Removed GitHub sprint-related descriptions; clarified localization design",
        "v3.8.0: Added Skill ecosystem documentation",
        "v3.7.0: Enabled automatic learning"
      ]
    }
  }
---

# ontology-clawra v5.0 - Local Ontology Reasoning Engine

## 1. Core定位 (Accurate Description)

**This is a local reasoning engine, not a cross-skill coordinator.**

```
Actual Capabilities:
✅ Local ontology knowledge graph storage and reasoning
✅ Confidence calculation and meta-cognition
✅ Local memory file search
✅ Automatic learning (write to local memory directory)

Actual Limitations:
❌ No skill scheduling (no Event Router)
❌ No cross-skill communication
❌ No automatic network requests
❌ No agent-to-agent RPC
```

## 2. File Access Permissions

| Operation | Path | Description |
|-----------|------|-------------|
| Read | `~/.openclaw/skills/ontology-clawra/memory/` | Ontology files |
| Read | `~/.openclaw/workspace/memory/*.md` | User context |
| Write | `~/.openclaw/skills/ontology-clawra/memory/` | Learning results |
| Write | GitHub (via git push) | Requires user confirmation |
| ❌ | Other directories | Never accessed |

**Network Behavior**:
- No automatic network requests
- network_fetch.py only searches local files, returns acquisition suggestions
- No requests/sockets/subprocess external calls

## 3. Core Reasoning Capabilities

### Confidence Levels

- `CONFIRMED`: Multi-source verified, trustworthy
- `ASSUMED`: Single source, requires user confirmation
- `SPECULATIVE`: High uncertainty, assumptions marked

### Reasoning Output Format

```
## Reasoning Result

### User Requirement
[Paraphrased original text]

### Rule Basis
- Rule-Law-[ID]: [Rule content]

### Reasoning Process
[Specific derivation steps]

### Confidence Annotation
| Conclusion | Confidence | Basis |
|------------|------------|-------|
| [Conclusion] | CONFIRMED/ASSUMED/SPECULATIVE | [Basis] |
```

## 4. Ontology File Format

**Directory**: `~/.openclaw/skills/ontology-clawra/memory/`

| File | Purpose |
|------|---------|
| `graph.jsonl` | Entities (Concept/Entity) |
| `rules.yaml` | Rules (Rule/Law) |
| `laws.yaml` | Patterns (inductive patterns) |
| `confidence_tracker.jsonl` | Confidence tracking |
| `reasoning.jsonl` | Reasoning log |

## 5. Automatic Learning

### Trigger Conditions

| Event | Action | Write Location |
|-------|--------|----------------|
| User confirms reasoning is correct | Extract to ontology | `graph.jsonl` |
| Confidence can be upgraded | Update confidence | `confidence_tracker.jsonl` |
| Reasoning fails | Suggest ontology addition | Prompt only |

### Write Rules

- Inform user before all write operations
- Write only to `~/.openclaw/skills/ontology-clawra/memory/`
- Do not upload any data to external services

## 6. Security Statement

1. **No external network calls**: Code contains no requests/urllib/sockets external calls
2. **No credential access**: Does not read environment variables or API keys
3. **Privacy isolation**: Workspace memory files used only for context, not synced
4. **Localization**: All learning results stored only in local memory directory

## 7. Version History

| Version | Date | Description |
|---------|------|-------------|
| v5.0 | 2026-03-25 | Removed GitHub sprint-related descriptions |
| v3.9 | 2026-03-24 | Removed exaggerated descriptions, clarified localization |
| v3.8 | 2026-03-20 | Added Skill ecosystem documentation |
| v3.7 | 2026-03-16 | Enabled automatic learning |
| v3.6 | 2026-03-16 | Initial version |

## 8. Supported Domain Ontologies

Supply chain procurement, healthcare, finance banking, cybersecurity,
automotive manufacturing, human resources, photography, furniture,
elderly care, childcare, tea culture, moving services, dating,
aerospace, and 50+ domains.

Ontology files located in: corresponding yaml files under `~/.openclaw/skills/ontology-clawra/memory/`