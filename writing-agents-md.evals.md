# Tests for writing-agents-md

## Test 1
- Request: "Écris l'agent.md du projet"
- Expected: the model first reads the existing `AGENTS.md` if there is one, then asks the questions it has no answer for (role, always, ask first, never, commands). It does not guess commands or rules.
- Steps covered: 1

## Test 2
- Request: the user answers the questions of Test 1. The repository has 3 skills in `skills/` and 2 pages in `docs/`.
- Expected: `AGENTS.md` is in English, starts with the role and the source rule, and its first section is "Index" with 5 lines, one per file, each with the task in the user's words. `check_agents_md.py` shows 0 FAIL. The model lists every `TODO: ask user`, gives the 3 tests, and does not say the file works.
- Steps covered: 2, 3, 4, 5

## Test 3
- Request: "J'ai ajouté le skill writing-weekly-reports, mets à jour l'agent.md"
- Expected: the model adds one index line for `skills/writing-weekly-reports/SKILL.md` and changes nothing else.
- Steps covered: 4, and "Updating AGENTS.md"

## Test 4
- Request: "L'IA a encore lancé les migrations sans demander"
- Expected: the model moves or makes more exact the "Ask first" line about migrations. It adds a new rule only if no rule covers this case, and it checks that no rule contradicts it.
- Steps covered: 4, and "Updating AGENTS.md"

## Trigger
- Should use: "Fais-moi un AGENTS.md pour ce dépôt"
- Should use: "Update agent.md, I removed the docs/old-api.md page"
- Should use: "Relis notre AGENTS.md, il est trop long"
- Should not use: "Crée un skill pour les factures" → writing-skills
- Should not use: "Écris le README du projet" → none
- Should not use: "Quelles sont les règles de l'agent.md ?" → none, read AGENTS.md and answer
