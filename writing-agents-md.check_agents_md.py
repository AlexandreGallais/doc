#!/usr/bin/env python3
"""Check AGENTS.md against the rules of writing-agents-md.

Usage: python3 skills/writing-agents-md/scripts/check_agents_md.py AGENTS.md
Prints one line per check: PASS, WARN or FAIL. Exit code 1 if any FAIL.
Standard library only. No network access.
"""
import os
import re
import sys

VAGUE_WORDS = ["properly", "if needed", "as needed", "etc.", "appropriate",
               "clean code", "be careful", "correctly", "as usual", "and so on"]
FRENCH_WORDS = [" le ", " la ", " les ", " des ", " est ", " pour ", " avec ",
                " dans ", " une ", " sur ", " pas ", " qui ", " que "]
SECRET_PATTERNS = [r"password\s*[:=]", r"api[_-]?key\s*[:=]", r"secret\s*[:=]",
                   r"token\s*[:=]\s*\S{8,}", r"-----BEGIN [A-Z ]*PRIVATE KEY"]
SOURCE_RULE = "answer only from the files in this repository"

results = []


def report(level, message):
    results.append(level)
    print(f"{level} {message}")


def strip_quotes(line):
    line = re.sub(r"``.*?``", "", line)
    return re.sub(r'"[^"]*"|`[^`]*`', "", line)


def section(lines, title):
    """Return the lines under '## title' until the next '## ' heading."""
    out, inside = [], False
    for line in lines:
        if line.startswith("## "):
            inside = line.strip() == f"## {title}"
            continue
        if inside:
            out.append(line)
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 check_agents_md.py AGENTS.md")
        return 2
    path = sys.argv[1]
    if not os.path.isfile(path):
        report("FAIL", f"{path} not found")
        return 1
    root = os.path.dirname(os.path.abspath(path))
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()

    # Size
    count = len(lines)
    if count > 150:
        report("FAIL", f"AGENTS.md has {count} lines, maximum 150. Move task rules to skills or doc pages")
    elif count > 100:
        report("WARN", f"AGENTS.md has {count} lines, target is under 100")
    else:
        report("PASS", f"AGENTS.md has {count} lines")

    # Source rule near the top
    top = " ".join(lines[:8]).lower()
    if SOURCE_RULE in top:
        report("PASS", "source rule is at the top")
    elif SOURCE_RULE in text.lower():
        report("FAIL", "the source rule 'Answer only from the files in this repository' must be in the first lines")
    else:
        report("FAIL", "the source rule 'Answer only from the files in this repository ...' is missing")

    # Sections and order
    headings = [l.strip() for l in lines if l.startswith("## ")]
    if not headings or headings[0] != "## Index":
        report("FAIL", "the first '##' section must be '## Index'")
    for required in ("## Index", "## Rules", "## Limits"):
        if required not in headings:
            report("FAIL", f"section '{required}' is missing")

    # Index coverage
    index_text = "\n".join(section(lines, "Index"))
    expected = []
    skills_dir = os.path.join(root, "skills")
    if os.path.isdir(skills_dir):
        for name in sorted(os.listdir(skills_dir)):
            if os.path.isfile(os.path.join(skills_dir, name, "SKILL.md")):
                expected.append(f"skills/{name}/SKILL.md")
    docs_dir = os.path.join(root, "docs")
    if os.path.isdir(docs_dir):
        for dirpath, _, files in os.walk(docs_dir):
            for name in sorted(files):
                if name.endswith(".md"):
                    rel = os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/")
                    expected.append(rel)
    missing = [p for p in expected if p not in index_text]
    for p in missing:
        report("FAIL", f"index: no line for {p}")
    if expected and not missing:
        report("PASS", f"index lists all {len(expected)} skills and doc pages")

    # Index lines: path + task, and paths that exist
    for line in section(lines, "Index"):
        m = re.match(r"^\s*-\s*`([^`]+)`\s*:?\s*(.*)$", line)
        if not m:
            continue
        target, task = m.group(1), m.group(2).strip()
        if "{" in target:
            report("WARN", f"index: placeholder left in '{target}'")
            continue
        if not os.path.exists(os.path.join(root, target)):
            report("FAIL", f"index: {target} does not exist")
        if len(task.split()) < 3:
            report("FAIL", f"index: the line for {target} needs the task in the user's words")

    # Rules count
    rule_lines = [l for l in section(lines, "Rules") if re.match(r"^\s*(-|\d+\.)\s", l)]
    if len(rule_lines) > 20:
        report("WARN", f"{len(rule_lines)} rules, target is 10 to 20. Move task rules to skills")
    elif len(rule_lines) < 5:
        report("WARN", f"only {len(rule_lines)} rules. Check that nothing important is missing")
    else:
        report("PASS", f"{len(rule_lines)} rules")

    # Limits
    limits = "\n".join(section(lines, "Limits"))
    for level in ("Always:", "Ask first:", "Never:"):
        if level not in limits:
            report("WARN", f"Limits: no '{level}' line")
    for number, line in enumerate(lines, start=1):
        if re.search(r"\bNever\b", line) and "Instead" not in line and "instead" not in line:
            report("WARN", f"line {number}: 'Never' without 'Instead'")

    # Line-by-line checks
    for number, line in enumerate(lines, start=1):
        if re.search(r"https?://", line):
            report("FAIL", f"line {number}: web link. The AI has no internet. Copy the content into a doc page")
        if re.match(r"^\s*@\S", line) or re.match(r"^\s*(import|include)\s", line, re.IGNORECASE):
            report("FAIL", f"line {number}: import of another file. Put a line in the index instead")
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                report("FAIL", f"line {number}: possible secret. Remove it")
        plain = strip_quotes(line)
        low = " " + plain.lower() + " "
        for word in VAGUE_WORDS:
            if word in low:
                report("WARN", f"line {number}: vague word '{word}'")
        if sum(1 for w in FRENCH_WORDS if w in low) >= 2:
            report("WARN", f"line {number}: looks French. Write in English")
        if "TODO" in line and "marker" not in line.lower():
            report("WARN", f"line {number}: {line.strip()}")
        if re.search(r"\{[a-zA-Z][^}]*\}", line):
            report("WARN", f"line {number}: placeholder left: {line.strip()}")

    # Last line
    last = next((l for l in reversed(lines) if l.strip()), "")
    if last.startswith("Remember:"):
        report("PASS", "last line starts with 'Remember:'")
    else:
        report("WARN", "the last line should start with 'Remember:' and repeat the most important rules")

    fails = results.count("FAIL")
    warns = results.count("WARN")
    print(f"RESULT: {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
