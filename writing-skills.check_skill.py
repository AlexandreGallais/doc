#!/usr/bin/env python3
"""Check a skill folder (SKILL.md + evals.md) against the rules of writing-skills.

Usage: python3 skills/writing-skills/scripts/check_skill.py skills/{name}
Prints one line per check: PASS, WARN or FAIL. Exit code 1 if any FAIL.
Standard library only. No network access.
"""
import os
import re
import sys

VAGUE_WORDS = ["properly", "if needed", "as needed", "etc.", "appropriate",
               "some ", "correctly", "as usual", "and so on"]
FRENCH_WORDS = [" le ", " la ", " les ", " des ", " est ", " pour ", " avec ",
                " dans ", " une ", " sur ", " pas ", " qui ", " que "]
SECRET_PATTERNS = [r"password\s*[:=]", r"api[_-]?key\s*[:=]", r"secret\s*[:=]",
                   r"token\s*[:=]\s*\S{8,}", r"-----BEGIN [A-Z ]*PRIVATE KEY"]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

results = []


def report(level, message):
    results.append(level)
    print(f"{level} {message}")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    fields = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return fields, i + 1
        m = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return None, 0


def strip_quotes(line):
    line = re.sub(r"``.*?``", "", line)
    return re.sub(r'"[^"]*"|`[^`]*`', "", line)


def fenced_lines(lines):
    """Return the set of line numbers (1-based) inside fenced code blocks."""
    inside, marker, out = False, "", set()
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not inside and stripped.startswith("```"):
            inside, marker = True, re.match(r"`+", stripped).group(0)
            out.add(number)
        elif inside:
            out.add(number)
            if stripped == marker:
                inside = False
    return out


def text_files(folder):
    for root, _, files in os.walk(folder):
        for name in files:
            if name.endswith((".md", ".txt", ".py", ".sh", ".js", ".mjs", ".json", ".yaml", ".yml")):
                yield os.path.join(root, name)


def find_agents_md(folder):
    current = os.path.abspath(folder)
    for _ in range(4):
        current = os.path.dirname(current)
        candidate = os.path.join(current, "AGENTS.md")
        if os.path.isfile(candidate):
            return candidate
    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 check_skill.py skills/{name}")
        return 2
    folder = sys.argv[1].rstrip("/\\")
    folder_name = os.path.basename(os.path.abspath(folder))
    skill_path = os.path.join(folder, "SKILL.md")
    if not os.path.isfile(skill_path):
        report("FAIL", f"{skill_path} not found")
        return 1
    text = read(skill_path)
    lines = text.splitlines()
    fences = fenced_lines(lines)
    outside = "\n".join(l for n, l in enumerate(lines, start=1) if n not in fences)

    # Frontmatter
    fields, body_start = parse_frontmatter(text)
    if fields is None:
        report("FAIL", "SKILL.md must start with a frontmatter block between two '---' lines")
        fields = {}
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name:
        report("FAIL", "frontmatter: 'name' is missing")
    elif not NAME_RE.match(name) or len(name) > 64:
        report("FAIL", f"name '{name}': use 1 to 64 lowercase letters, digits and single hyphens")
    elif name != folder_name:
        report("FAIL", f"name '{name}' is not the same as the folder '{folder_name}'")
    else:
        report("PASS", f"name '{name}'")
    if not description:
        report("FAIL", "frontmatter: 'description' is missing")
    elif description in (">", "|", ">-", "|-"):
        report("FAIL", "description: write it on one line, after 'description:'")
    else:
        if len(description) > 1024:
            report("FAIL", f"description: {len(description)} characters, maximum 1024")
        if "use when" not in description.lower():
            report("FAIL", "description: add 'Use when ...' with the words the user types")
        else:
            report("PASS", f"description ({len(description)} characters, has 'Use when')")

    # Size
    count = len(lines)
    if count > 500:
        report("FAIL", f"SKILL.md has {count} lines, maximum 500. Move reference text to references/")
    elif count > 300:
        report("WARN", f"SKILL.md has {count} lines, target is under 300")
    else:
        report("PASS", f"SKILL.md has {count} lines")

    # Sections
    headings = [l.strip() for n, l in enumerate(lines, start=1) if l.startswith("## ") and n not in fences]
    for required in ("## Rules", "## Steps", "## Done when"):
        if required not in headings:
            report("FAIL", f"section '{required}' is missing")
    if "## Steps" in headings and "## Rules" in headings:
        if headings.index("## Rules") > headings.index("## Steps"):
            report("FAIL", "'## Rules' must come before '## Steps'")
    if "## Known mistakes" in headings and "## Steps" in headings:
        if headings.index("## Known mistakes") > headings.index("## Steps"):
            report("WARN", "'## Known mistakes' should come before '## Steps'")
    if not re.search(r"^\d+\.\s", outside, re.MULTILINE):
        report("FAIL", "no numbered step found (lines like '1. ...')")
    if not re.search(r"^\d+\.\s+.*\bcheck", outside, re.MULTILINE | re.IGNORECASE):
        report("WARN", "no numbered step that checks the result")

    # Line-by-line checks in SKILL.md body
    for number, line in enumerate(lines, start=1):
        if number <= body_start or number in fences:
            continue
        plain = strip_quotes(line)
        low = " " + plain.lower() + " "
        for word in VAGUE_WORDS:
            if word in low:
                report("WARN", f"SKILL.md line {number}: vague word '{word.strip()}'")
        french = sum(1 for w in FRENCH_WORDS if w in low)
        if french >= 2:
            report("WARN", f"SKILL.md line {number}: looks French. Write in English")
        if "TODO" in line and "marker" not in line.lower():
            report("WARN", f"SKILL.md line {number}: {line.strip()}")
        if re.search(r"\{[a-zA-Z][^}]*\}", plain):
            report("WARN", f"SKILL.md line {number}: placeholder left: {line.strip()}")

    # Links, secrets, references in all text files
    for path in text_files(folder):
        rel = os.path.relpath(path, folder)
        if rel.startswith("scripts" + os.sep) and path.endswith(".py") and os.path.basename(path) == "check_skill.py":
            continue
        content = read(path)
        for number, line in enumerate(content.splitlines(), start=1):
            if re.search(r"https?://", line):
                report("FAIL", f"{rel} line {number}: web link. The model has no internet. Copy the content into references/")
            for pattern in SECRET_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    report("FAIL", f"{rel} line {number}: possible secret. Remove it")

    ref_dir = os.path.join(folder, "references")
    if os.path.isdir(ref_dir):
        ref_files = sorted(os.listdir(ref_dir))
        if len(ref_files) > 3:
            report("WARN", f"references/ has {len(ref_files)} files, target is at most 3")
        for ref in ref_files:
            if f"references/{ref}" not in outside:
                report("FAIL", f"references/{ref} is not linked from SKILL.md")
    for linked in re.findall(r"references/[A-Za-z0-9_.-]+", outside):
        if not os.path.isfile(os.path.join(folder, linked)) and "{" not in linked:
            report("FAIL", f"SKILL.md links to {linked}, but the file does not exist")

    # evals.md
    evals_path = os.path.join(folder, "evals.md")
    if not os.path.isfile(evals_path):
        report("FAIL", "evals.md is missing. Write the tests first")
    else:
        evals = read(evals_path)
        tests = len(re.findall(r"^## Test", evals, re.MULTILINE))
        should = len(re.findall(r"^- Should use:", evals, re.MULTILINE))
        should_not = len(re.findall(r"^- Should not use:", evals, re.MULTILINE))
        if tests < 3:
            report("FAIL", f"evals.md has {tests} tests, minimum 3")
        else:
            report("PASS", f"evals.md has {tests} tests")
        if should < 3 or should_not < 3:
            report("FAIL", f"evals.md trigger lines: {should} 'Should use', {should_not} 'Should not use'; minimum 3 each")
        else:
            report("PASS", "evals.md trigger lines")
        if "{" in evals:
            report("WARN", "evals.md still has a '{...}' placeholder")

    # Index line in AGENTS.md
    agents = find_agents_md(folder)
    if agents is None:
        report("WARN", "AGENTS.md not found. Use the skill writing-agents-md")
    elif f"skills/{folder_name}/SKILL.md" in read(agents):
        report("PASS", "AGENTS.md has an index line for this skill")
    else:
        report("FAIL", f"AGENTS.md has no index line for skills/{folder_name}/SKILL.md")

    fails = results.count("FAIL")
    warns = results.count("WARN")
    print(f"RESULT: {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
