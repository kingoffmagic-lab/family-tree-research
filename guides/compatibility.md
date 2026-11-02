# Use with an agent

Install or copy the **entire `family-tree-research` directory**, not only SKILL.md or a nested helper. References, scripts and the pinned research engine must stay together. Never put real cases inside the installed skill.

| Host | Local installation | Invoke |
|---|---|---|
| Claude Code | `~/.claude/skills/family-tree-research/` or project `.claude/skills/family-tree-research/` | `/family-tree-research` |
| Codex | `~/.agents/skills/family-tree-research/` or project `.agents/skills/family-tree-research/` | `$family-tree-research` |
| Other Agent Skills host | Its configured skill directory | Select `family-tree-research` |
| Any file-capable agent | Any readable folder | Ask it to read the absolute path to SKILL.md and follow its local references |

For a downloaded ZIP, extract the folder before use. Do not flatten it. A separate upstream skill or MCP server is unnecessary. The optional agents/openai.yaml supplies UI metadata, not a runtime dependency. AGENTS.md and CLAUDE.md are thin entry-point pointers; hosts that ignore them can read SKILL.md directly.

Minimum full workflow: file access, a shell with Python 3.9+, and web tools for online research. Image/PDF reading is needed for scans. Without a capability, follow the entry point's fallback and state what was not performed. Account and source restrictions still apply.

The package is checked after relocation, under a skill-directory layout, from an unrelated working directory and from a ZIP extraction. These are packaging/CLI tests, not live certification of every agent's reasoning or permissions.

Sources: [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Agent Skills specification](https://agentskills.io/specification).
