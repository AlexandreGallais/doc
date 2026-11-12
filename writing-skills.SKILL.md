---
name: writing-skills
description: Writes a new skill (a folder with SKILL.md and evals.md) or fixes an existing one, from a real task the user has done. Use when the user asks to create, write, improve, fix or review a skill or a SKILL.md, in English or French ("crée un skill", "fais une skill", "améliore ce skill", "corrige ce SKILL.md").
---

# Writing skills

Result: a folder `skills/{name}/` with `SKILL.md` and `evals.md`, written in English, that another model can follow without help, plus one new line in the index of `AGENTS.md`.

## Rules

1. Write every file in English, even when the user writes in French. Use French only for the user's own words: in `description` and in test requests.
2. Never invent facts. You have no internet access. If you do not know a command, a path, a version, a value or a rule, ask the user. If the user is not there, write the marker TODO: ask user in its place.
3. Never put a web link in a skill. The model that reads the skill has no internet either. If the user gives you a document, copy the needed part into `references/{topic}.md`.
4. Write only what is specific to this task: the user's rules, paths, commands, formats and past mistakes. Do not explain general knowledge.
5. One skill = one task. If the task has two goals, write two skills.
6. Give one default way. Never give a list of options to choose from.
7. Write each step as one action: a verb plus the exact command, file or value.
8. Put the rules and the known mistakes before the steps.
9. Use the same word for the same thing in every file. No synonyms.
10. Keep `SKILL.md` under 300 lines. Hard limit: 500 lines. Put long reference text in `references/`: at most 3 files, each linked directly from `SKILL.md`.

## Known mistakes

- The description says what, but not when → the skill is never used. Always write "Use when ..." with the user's words.
- Long explanations → the model forgets the steps. Cut every sentence that is not a rule, a step, a fact or a mistake.
- Steps in a paragraph → steps get skipped. Use numbered steps.
- Vague words ("properly", "if needed", "etc.", "appropriate", "some") → write the exact condition or value.
- Warnings at the end of the file → move them to "Rules".
- A command, path or value you guessed → delete it and write the TODO marker.
- The user writes in French, so the skill is written in French → write it in English.
- A reference file that links to another file → link every file directly from `SKILL.md`.

## Steps

Copy this checklist into your answer and tick each line:
```text
- [ ] 1. Collect the facts
- [ ] 2. Write evals.md
- [ ] 3. Choose name and description
- [ ] 4. Write SKILL.md
- [ ] 5. Run the checks
- [ ] 6. Add the index line in AGENTS.md
- [ ] 7. Give the files to the user
```

1. Collect the facts.
   - If the user did the task with you earlier in this conversation, read it again. Note each correction the user made.
   - Then ask, in one message, only the questions you have no answer for. Wait for the answers.
     - What task must the skill do? Give one real request, in your own words.
     - What did you have to correct or repeat last time?
     - What is the expected result: which file, which format, which answer?
     - Which commands, files and tools are used? Give exact names and paths.
     - When must the skill NOT be used?
2. Write `evals.md` before `SKILL.md`, with the template "evals.md" below:
   - at least 3 tests, each with a real request and a result the user can check;
   - 6 trigger lines: 3 "Should use", 3 "Should not use" with requests that look close.
3. Choose `name` and `description`.
   - `name`: lowercase letters, digits and single hyphens; 1 to 64 characters; no hyphen at the start or the end; the same as the folder. Use a verb with -ing, for example `writing-reports`.
   - `description`: one line, third person, at most 1,024 characters. First what the skill does. Then "Use when ..." with the words the user types, in English and French.
4. Write `SKILL.md` with the template "SKILL.md" below. Keep the section order. Replace every `{...}`. Required sections: Rules, Steps, Done when. Delete an optional section only if you have no real fact for it.
5. Run the checks.
   - If you can run Python 3, run: `python3 skills/writing-skills/scripts/check_skill.py skills/{name}`. Fix each FAIL. Read each WARN and fix it if it is right.
   - Then check each line of the checklist at the end of this file.
   - Repeat until no FAIL is left and every checklist line passes.
6. Add one line to the "Index" section of `AGENTS.md`: `` - `skills/{name}/SKILL.md`: {task, in the user's words} ``. If `AGENTS.md` does not exist, use the skill `writing-agents-md`.
7. Give the files to the user.
   - List every TODO marker.
   - Ask: "Please run the tests in evals.md, once with the skill and once without it, and tell me what failed."
   - Do not say the skill works. It is not tested yet.

## Fixing an existing skill

1. Read the whole `SKILL.md` and `evals.md`.
2. Ask the user what went wrong, with one real example.
3. Change as little as possible: add one line to "Known mistakes", or make one step more exact. Do not rewrite the whole skill.
4. Add one test to `evals.md` that fails without your fix.
5. Run steps 5 and 7.

## Good and bad lines

```text
Bad description:  Helps with reports.
Good description: Writes the weekly status report from tasks.csv. Use when the user asks for the weekly report or status report ("rapport de la semaine", "point hebdo").

Bad step:  Format the output properly.
Good step: Write the output as a Markdown table with the columns Task, Owner, Status.

Bad rule:  Never use the old API.
Good rule: Never call /v1/orders. Instead, call /v2/orders.

Bad reference:  See the official documentation online.
Good reference: Read references/orders-api.md only if the request has a refund.
```

## Template: SKILL.md

````markdown
---
name: {name}
description: {What the skill does, third person.} Use when {the words the user types, in English and French}.
---

# {Title}

Result: {one line: what this skill produces}.

## Rules

1. {Rule the model would break without this skill.}
2. Never {action}. Instead, {action}.

## Known mistakes

- {Mistake} → {what to do instead}.

## Steps

Copy this checklist into your answer and tick each line:
```text
- [ ] 1. {short step}
- [ ] 2. {short step}
- [ ] 3. Check the result
```

1. {Verb + exact action, command, file or value.}
2. If {exact condition}, {action}. Otherwise, {action}.
3. Check: {exact test}. If it fails, fix it and check again.

## Output

Use this exact format:
```text
{output template}
```

## Done when

- {Fact the user can check.}

## References

- `references/{file}.md`: read only if {exact condition}.
````

Optional sections: Known mistakes, Output, References.

## Template: evals.md

````markdown
# Tests for {name}

## Test 1
- Request: "{real user request}"
- Expected: {result the user can check}
- Steps covered: {step numbers}

## Test 2
- Request: "{real user request}"
- Expected: {result the user can check}
- Steps covered: {step numbers}

## Test 3
- Request: "{real user request}"
- Expected: {result the user can check}
- Steps covered: {step numbers}

## Trigger
- Should use: "{request}"
- Should use: "{request}"
- Should use: "{request}"
- Should not use: "{close request}" → {other skill, or none}
- Should not use: "{close request}" → {other skill, or none}
- Should not use: "{close request}" → {other skill, or none}
````

## Checklist

- [ ] `SKILL.md` and `evals.md` are in English. French only in the user's words.
- [ ] The folder name is the same as `name`, and `name` follows the rules of step 3.
- [ ] `description` is one line, says what the skill does, then "Use when ..." with the user's words.
- [ ] The rules and the known mistakes come before the steps.
- [ ] Each step starts with a verb and names an exact command, file or value.
- [ ] No vague word: "properly", "if needed", "etc.", "appropriate", "some".
- [ ] Every fact comes from the user or from a file you read. Every guess has a TODO marker.
- [ ] One default way, no list of options.
- [ ] No web link. Each file in `references/` is linked from `SKILL.md` with "read only if".
- [ ] The steps end with a "Check" step, and the file has a "Done when" section.
- [ ] `evals.md` has at least 3 tests and 6 trigger lines. Each step number appears in a test.
- [ ] `SKILL.md` is under 300 lines (500 at most).
- [ ] `AGENTS.md` has an index line for this skill.
- [ ] No password, key or secret.

## Done when

- `check_skill.py` shows 0 FAIL, or every checklist line passes.
- The user has the list of TODO markers and the request to run the tests.
