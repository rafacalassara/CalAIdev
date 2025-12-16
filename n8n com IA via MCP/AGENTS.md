# AGENTS.md — n8n Workflow Builder Guardrails (based on czlonkowski/n8n-skills)

> **Note**: This file provides condensed guardrails. The full agent is defined in `.github/agents/n8n-workflow-builder.agent.md` which dynamically loads skills from `n8n-skills/skills/`.

## Global Rules (Always Apply)

### MCP-First Approach
- **NEVER guess nodeType** - always use `search_nodes` first
- Use `get_node_essentials` (91.7% success, 5KB) over `get_node_info` (80% success, 100KB+)
- Default loop: search → essentials → configure → validate → fix → validate again

### nodeType Format Rules
| Context | Format | Example |
|---------|--------|---------|
| Search/Validate tools | `nodes-base.*` | `nodes-base.slack` |
| Workflow JSON | `n8n-nodes-base.*` | `n8n-nodes-base.slack` |

### Critical Gotchas (Cause 80% of Failures)
1. Webhook data is under `$json.body` not `$json`
2. Code nodes return `[{json: {...}}]` format
3. No `{{}}` expressions inside Code nodes
4. Python has NO external libraries
5. Validation is iterative (expect 2-3 cycles)

---

## Dynamic Skill Routing

The agent activates skills based on detected triggers:

### 🔴 Always Active: MCP Tools Expert
**File**: `n8n-skills/skills/n8n-mcp-tools-expert/SKILL.md`

Quick rules:
- Smart parameters: `branch="true"/"false"` for IF, `case=0/1` for Switch
- Use `n8n_update_partial_workflow` for edits (99% success rate)
- Validation profiles: `minimal`, `runtime` (default), `ai-friendly`, `strict`

### 🟠 High Priority: Workflow Patterns
**Triggers**: `build workflow`, `new workflow`, `automate`, `webhook`, `api`, `schedule`
**File**: `n8n-skills/skills/n8n-workflow-patterns/SKILL.md`

Quick rules:
- 5 patterns: Webhook Processing, HTTP API, Database Ops, AI Agent, Scheduled Tasks
- Webhook (35%) → Always include response node
- Always explain why the chosen pattern fits

### 🟡 Medium Priority: Node Configuration
**Triggers**: `configure`, `setup node`, `properties`, `operation`, `required fields`
**File**: `n8n-skills/skills/n8n-node-configuration/SKILL.md`

Quick rules:
- Configuration is operation-aware: set resource → operation → specific fields
- Use `get_property_dependencies` for field visibility rules
- Progressive discovery: essentials → dependencies → full info

### 🟡 Medium Priority: Validation Expert
**Triggers**: `error`, `validation`, `fails`, `not working`, `warning`, `fix`
**File**: `n8n-skills/skills/n8n-validation-expert/SKILL.md`

Quick rules:
- ~40% of warnings are acceptable false positives
- Error types: `missing_required` (45%), `invalid_value` (28%), `type_mismatch` (12%)
- Auto-sanitization may rewrite operator structures

### 🟢 On-Demand: Expression Syntax
**Triggers**: `{{`, `expression`, `$json`, `$node`, `$now`, `undefined`
**File**: `n8n-skills/skills/n8n-expression-syntax/SKILL.md`

Quick rules:
- All expressions: `{{ expression }}`
- **CRITICAL**: Webhook data → `{{ $json.body.field }}` NOT `{{ $json.field }}`
- Only use in node parameters, NOT in Code nodes

### 🟢 On-Demand: Code JavaScript
**Triggers**: `code node`, `javascript`, `js`, `$input`, `$helpers`, `transform`
**File**: `n8n-skills/skills/n8n-code-javascript/SKILL.md`

Quick rules:
- Data: `$input.all()`, `$input.first()`, `$input.item`
- HTTP: `await $helpers.httpRequest({...})`
- Return: `[{json: {key: value}}]`
- Mode: "Run Once for All Items" (95% of cases)

### 🔵 Rare: Code Python
**Triggers**: `python`, `_input`, `standard library`
**File**: `n8n-skills/skills/n8n-code-python/SKILL.md`

Quick rules:
- **Prefer JavaScript for 95% of cases**
- NO external libs (no requests, pandas, numpy)
- Available: json, datetime, re, base64, hashlib, urllib.parse, math, random
- Webhook: `_json["body"]["field"]`

---

## Skill Composition Examples

**"Build webhook → Slack workflow"**
```
1. Workflow Patterns   → Webhook Processing pattern
2. MCP Tools Expert    → Search webhook, slack nodes
3. Node Configuration  → Configure operations
4. Expression Syntax   → Map $json.body fields
5. Validation Expert   → Validate complete workflow
```

**"Fix validation error"**
```
1. Validation Expert   → Analyze error type
2. Node Configuration  → Check dependencies
3. [If code] Code JS   → Check return format
```

---

## Supporting Files (Load on Demand)

| Situation | File |
|-----------|------|
| Search issues | `n8n-skills/skills/n8n-mcp-tools-expert/SEARCH_GUIDE.md` |
| Validation errors | `n8n-skills/skills/n8n-validation-expert/ERROR_CATALOG.md` |
| False positives | `n8n-skills/skills/n8n-validation-expert/FALSE_POSITIVES.md` |
| Code errors | `n8n-skills/skills/n8n-code-javascript/ERROR_PATTERNS.md` |
| Data access | `n8n-skills/skills/n8n-code-javascript/DATA_ACCESS.md` |
| Expression examples | `n8n-skills/skills/n8n-expression-syntax/EXAMPLES.md` |
