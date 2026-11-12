# Tests for writing-skills

## Test 1
- Request: "Crée un skill pour faire le rapport de la semaine à partir de tasks.csv"
- Expected: before writing any file, the model asks the questions it has no answer for (result format, columns of tasks.csv, past corrections, when not to use). It does not guess the columns.
- Steps covered: 1

## Test 2
- Request: the user answers the questions of Test 1.
- Expected: the folder `skills/writing-weekly-reports/` has `evals.md` and `SKILL.md`, both in English. `description` has "Use when" and the user's French words. `check_skill.py` shows 0 FAIL. `AGENTS.md` has the new index line. The model lists every `TODO: ask user` and does not say the skill works.
- Steps covered: 2, 3, 4, 5, 6, 7

## Test 3
- Request: "Le skill exporting-invoices a oublié de vérifier que le total est égal à la somme des lignes"
- Expected: the model adds one line to "Known mistakes" or makes one step more exact, and adds one test to `evals.md`. It does not rewrite the rest of the skill.
- Steps covered: 5, 7, and "Fixing an existing skill"

## Test 4
- Request: "Fais un skill pour notre API, la doc est en ligne sur le site de l'éditeur"
- Expected: the model writes no web link in the skill. It asks the user to paste the needed part of the documentation, then copies it into `references/`.
- Steps covered: 1, 4, 5

## Trigger
- Should use: "Crée-moi une skill pour générer les factures"
- Should use: "Improve this SKILL.md, the model skips step 3"
- Should use: "Corrige le skill writing-weekly-reports"
- Should not use: "Écris l'AGENTS.md du projet" → writing-agents-md
- Should not use: "Fais le rapport de la semaine" → the skill that writes the report, or none
- Should not use: "C'est quoi un skill ?" → none, answer directly
