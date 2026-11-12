---
name: writing-agents-md
description: Writes or updates the AGENTS.md file at the root of a repository, so that an AI without internet access finds its role, its rules and every skill and doc page. Use when the user asks to create, write, update, clean or review AGENTS.md or agent.md, or after a skill or doc page is added, removed or renamed, in English or French ("écris l'agent.md", "mets à jour AGENTS.md", "ajoute ce skill à l'index").
---

# Writing AGENTS.md

Result: a short `AGENTS.md` in English, at the root of the repository. The AI reads it before every task. It gives the role, the source rule, the index of all skills and doc pages, the rules and the limits.

## Rules

1. Write `AGENTS.md` in English, even when the user writes in French. Use French only for the user's own words in index lines.
2. Never invent facts. You have no internet access. If you do not know a command, a path, a version or a rule, ask the user. If the user is not there, write the marker TODO: ask user in its place.
3. Never put a web link in `AGENTS.md`. The AI that reads it has no internet either.
4. Write only what applies to every task and what the AI cannot guess. Put the details of one task in its skill or doc page, not here.
5. Every skill in `skills/` and every page in `docs/` has one line in the index. A file that is not in the index is never read.
6. Write each rule as one short imperative sentence. Each "Never" says what to do instead.
7. Name tools, versions, paths and commands exactly.
8. Keep 10 to 20 rules, the most important first. No two rules may contradict.
9. Keep `AGENTS.md` under 100 lines. Hard limit: 150 lines. Do not import other files into it.

## Known mistakes

- An overview of the project, its history or its folder tree → the AI wastes attention on it. Delete it.
- A skill missing from the index → the skill is never used. Add its line.
- An index line with the path only → the AI cannot match it to a task. Write the task in the user's words.
- Two rules that contradict → the AI follows one of them at random. Keep one, delete the other.
- "Never X" with no alternative → the AI stops or guesses. Add "Instead, Y."
- A vague rule ("write clean code", "be careful") → write the exact action or value.
- The most important rule appears only once, in the middle → repeat it on the last line.
- The user writes in French, so `AGENTS.md` is written in French → write it in English.

## Steps

Copy this checklist into your answer and tick each line:
```text
- [ ] 1. Collect the facts
- [ ] 2. List the files for the index
- [ ] 3. Write AGENTS.md
- [ ] 4. Run the checks
- [ ] 5. Give the file and the tests to the user
```

1. Collect the facts.
   - If `AGENTS.md` exists, read it first. Keep every rule that is still true.
   - Then ask, in one message, only the questions you have no answer for. Wait for the answers.
     - What is the AI's role: who does it help, and for what?
     - What must the AI always do, on every task?
     - What must the AI ask before doing?
     - What must the AI never do, and what must it do instead?
     - Which exact commands are used to build, test and run the project?
2. List the files for the index.
   - For each folder in `skills/`, read the `description` line of its `SKILL.md`.
   - For each page in `docs/`, read its title and its first line. If `docs/INDEX.md` exists, read it instead.
   - Write one line per file: `` - `{path}`: {task, in the user's words} ``.
3. Write `AGENTS.md` with the template below. Keep the section order. Replace every `{...}`. Delete the "Commands" section only if the project has no command.
4. Run the checks.
   - If you can run Python 3, run: `python3 skills/writing-agents-md/scripts/check_agents_md.py AGENTS.md`. Fix each FAIL. Read each WARN and fix it if it is right.
   - Then check each line of the checklist at the end of this file.
   - Repeat until no FAIL is left and every checklist line passes.
5. Give the file to the user.
   - List every TODO marker.
   - Give these 3 tests and ask the user to run them in a new conversation:
     - A question answered by one doc page → the AI names that page and answers from it.
     - A question with no answer in the files → the AI says the information is missing and names the file that should contain it.
     - A request for a "Never" action → the AI refuses and does the "Instead" action.
   - Do not say the file works. It is not tested yet.

## Updating AGENTS.md

- A skill or doc page is added → add its index line. Change nothing else.
- A file is removed or renamed → delete or fix its index line.
- The AI broke a rule → make that rule more exact, or move it higher. Add a new rule only if no rule covers the case.
- A rule is no longer true → delete it.
- After each change, run step 4.

## Template: AGENTS.md

````markdown
# AGENTS.md

You are {role: who you help, and for what}.
Answer only from the files in this repository. If the information is missing, say so and name the file that should contain it.

## Index

Before you answer, read the file that matches the task.
- `skills/{name}/SKILL.md`: {task, in the user's words}
- `docs/{topic}.md`: {task, in the user's words}

## Rules

### Writing files
- Write every skill, doc page and `AGENTS.md` in English. Use French only for the user's own words.
- To write or fix a skill, use `skills/writing-skills/SKILL.md`.
- After you add, remove or rename a skill or doc page, update the index of this file.

### {Topic}
- {Imperative rule, the most important first.}

## Limits

- Always: {action}.
- Ask first: {action}.
- Never: {action}. Instead, {action}.

## Commands

```bash
{exact command}   # {what it does}
```

Remember: answer only from the files in this repository, read the matching file in the index first, and {the most important project rule}.
````

## Checklist

- [ ] `AGENTS.md` is in English. French only in the user's words.
- [ ] The first lines give the role, then the rule "Answer only from the files in this repository ...".
- [ ] The first `##` section is "Index". Every skill in `skills/` and every page in `docs/` has one line.
- [ ] Each index line gives the exact path and the task in the user's words.
- [ ] 10 to 20 rules, short, imperative, the most important first.
- [ ] "Limits" has three levels: Always, Ask first, Never. Each "Never" has "Instead".
- [ ] No two rules contradict.
- [ ] No overview of the project, no history, no rule for one task only.
- [ ] No web link, no import of another file.
- [ ] Tools, versions, paths and commands are named exactly.
- [ ] Every fact comes from the user or from a file you read. Every guess has a TODO marker.
- [ ] The last line starts with "Remember:" and repeats the most important rules.
- [ ] `AGENTS.md` is under 100 lines (150 at most).
- [ ] No password, key or secret.

## Done when

- `check_agents_md.py` shows 0 FAIL, or every checklist line passes.
- The user has the list of TODO markers and the 3 tests.
