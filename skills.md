---
name: writing-skills
description: Writes a new skill (a folder with a SKILL.md file) or fixes an existing one, from a task the user has already done. Use when the user asks to create, write, improve, fix or review a skill or a SKILL.md, in English or French ("crée un skill", "écris une skill", "améliore ce skill", "corrige ce SKILL.md").
---

# Writing skills

Result: a folder `skills/{name}/` with a short `SKILL.md` and an `evals.md`, that another model can follow alone.

## Rules

1. Never invent facts. You have no internet. If you do not know a command, a path, a value or a rule, ask the user. If the user is not there, write `TODO: ask user`.
2. Write only facts specific to this task: the user's rules, paths, commands, formats, and past mistakes. Do not explain general knowledge.
3. One skill = one task. If the task has two goals, write two skills.
4. Keep `SKILL.md` under 150 lines. Hard limit: 500 lines. Put long reference text in `references/`.
5. Use the same word for the same thing everywhere. No synonyms.
6. Give one default way. Never give a list of options to choose from.
7. Write each step as one exact action: verb + exact command, file or value.
8. Put rules and known mistakes before the steps.

## Steps

Copy this checklist into your answer and tick each line:
```text
- [ ] 1. Collect the facts
- [ ] 2. Write evals.md
- [ ] 3. Choose name and description
- [ ] 4. Write SKILL.md
- [ ] 5. Check with the checklist
- [ ] 6. Give the files to the user
```

1. Collect the facts. Ask the user these 5 questions in one message, then wait for the answers:
   - What task must the skill do? Give one real request.
   - What did you have to correct or repeat last time?
   - What is the expected result: file, format or answer?
   - Which commands, files or tools are used?
   - When must the skill NOT be used?
2. Write `evals.md` before `SKILL.md`, with the template "evals.md" below: 3 tests and 6 trigger lines (3 "should use", 3 "should not use").
3. Choose `name` and `description`:
   - `name`: lowercase letters, digits and hyphens; 1 to 64 characters; no hyphen at the start or the end; no `--`; same as the folder. Use a verb with -ing: `writing-reports`.
   - `description`: one line, third person, at most 1,024 characters. First what the skill does, then "Use when ..." with the words the user types, in English and French.
4. Write `SKILL.md` with the template "SKILL.md" below. Replace every `{...}`. Delete an optional section only if you have no real fact for it. Required: Rules, Steps, Done when.
5. Check each line of the checklist below. Fix each failed line. Check again until every line passes.
6. Give the files to the user. List every `TODO: ask user`. Then say: "Please run the 3 tests in evals.md and tell me what failed." Do not say the skill works: it is not tested yet.

## Fixing an existing skill

1. Read the whole `SKILL.md` and `evals.md`.
2. Ask the user what went wrong, with one real example.
3. Add one line to "Known mistakes" or change one step. Do not rewrite the whole skill.
4. Add one test to `evals.md` for this failure.
5. Run steps 5 and 6 above.

## Known mistakes

- Description says what, but not when → the skill is never used. Always write "Use when ..." with the user's words.
- Long explanations → the model forgets the steps. Cut every sentence that is not a rule, a step, a fact or a mistake.
- Steps in a paragraph → steps get skipped. Use numbered steps.
- Vague words ("properly", "if needed", "etc.", "some") → write the exact condition or value.
- Warnings at the end → move them to "Rules".
- Invented command, path or value → delete it, write `TODO: ask user`.
- A reference file that links to another file → keep links one level deep from `SKILL.md`.

## Template: SKILL.md

````markdown
---
name: {name}
description: {What the skill does.} Use when {words the user types, in English and French}.
---

# {Title}

{One line: the result.}

## Rules
- {Rule the model would break without this skill.}

## Steps
Copy this checklist into your answer and tick each line:
```text
- [ ] 1. {short step}
- [ ] 2. {short step}
- [ ] 3. Check the result
```
1. {Verb + exact action, command, file or value.}
2. If {exact condition}, {action}. Otherwise, {action}.
3. Check: {exact test}. If it fails, fix and check again.

## Known mistakes (optional)
- {Mistake} → {what to do instead}.

## Output (optional)
Use this exact format:
```text
{output template}
```

## Done when
- {Fact the user can check.}

## References (optional)
- `references/{file}.md`: read only if {exact condition}.
````

## Template: evals.md

````markdown
# Tests for {name}

## Test 1
- Request: "{real user request}"
- Expected: {result the user can check}
- Steps covered: {step numbers}

## Trigger
- Should use: "{request}"
- Should not use: "{nearby request}" → {other skill, or none}
````

## Checklist

- [ ] Folder name = `name`, and `name` follows the rules of step 3.
- [ ] `description` contains "Use when" and the user's own words.
- [ ] `SKILL.md` is under 150 lines (500 at most).
- [ ] Rules and known mistakes come before the steps.
- [ ] Each step starts with a verb and names an exact command, file or value.
- [ ] No vague word: "properly", "if needed", "etc.", "some", "appropriate".
- [ ] Every fact comes from the user or from a file you read.
- [ ] One default way, no list of options.
- [ ] Each file in `references/` is linked from `SKILL.md` with "read only if".
- [ ] A "Check" step and a "Done when" section exist.
- [ ] `evals.md` has 3 tests and 6 trigger lines; each step number appears in a test.
- [ ] No password, key or secret.
