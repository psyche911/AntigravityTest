# Claude Code Project Configuration

## gstack

Use the `/browse` skill from gstack for all web browsing. Never use `mcp__claude-in-chrome__*` tools.

Available gstack skills:
- `/plan-ceo-review` — CEO-level plan review
- `/plan-eng-review` — Engineering-level plan review
- `/review` — PR review
- `/ship` — Ship workflow
- `/browse` — Headless browser for web browsing, QA, and site testing
- `/qa` — QA testing workflow
- `/setup-browser-cookies` — Set up browser cookies for authenticated sessions
- `/retro` — Retrospective workflow

If gstack skills aren't working, run the following to build the binary and register skills:

```bash
cd .claude/skills/gstack && ./setup
```
