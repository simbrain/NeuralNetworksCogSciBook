"""Create, validate, and format the book's glossary."""

import argparse
from pathlib import Path
import re
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
MAIN_GLOSSARY_FILE = REPOSITORY_ROOT / "Glossary.tex"
ITEM_PATTERN = re.compile(r"(?m)^\s*\\item\[([^]]+)\]")
GLOSSARY_PATTERN = re.compile(r"\\glossary(?:\[([^\]]+)\])?\{([^}]+)\}")


def read_file(file_path):
    try:
        return Path(file_path).read_text()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        sys.exit(1)


def sort_key(term):
    """Use a case-insensitive, punctuation-insensitive alphabetical order."""
    return re.sub(r"[^\w]+", "", term, flags=re.UNICODE).casefold()


def find_chapters(container_document):
    chapters = []
    for line in read_file(container_document).splitlines():
        if line.lstrip().startswith("%"):
            continue
        match = re.search(r"^\s*\\input\{([^}]+)\}", line)
        if match:
            chapters.append(Path(container_document).parent / f"{match.group(1)}.tex")
    return chapters


def find_glossary_items(files):
    items = set()
    for file in files:
        for line in read_file(file).splitlines():
            if line.lstrip().startswith("%"):
                continue
            for key, display_text in GLOSSARY_PATTERN.findall(line):
                items.add((key or display_text).strip())
    return items


def parse_entries(glossary_text):
    """Return complete glossary entry blocks, keyed by their displayed term."""
    matches = list(ITEM_PATTERN.finditer(glossary_text))
    entries = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else glossary_text.find(
            r"\end{description}", match.end()
        )
        if end == -1:
            raise ValueError("Glossary.tex has an item without a closing description environment")
        entries.append((match.group(1).strip(), glossary_text[match.start():end].strip()))
    return entries


def matching_entry(term, entries):
    """Match the legacy singular/plural convention used by ``\\glossary``."""
    normalized = term.casefold()
    singular = normalized[:-1] if normalized.endswith("s") else normalized
    matches = [
        entry
        for label, entry in entries
        if (label.casefold()[:-1] if label.casefold().endswith("s") else label.casefold())
        == singular
    ]
    return matches[0] if matches else None


def validate(entries, referenced_items, check_stranded):
    labels = [label for label, _ in entries]
    errors = []
    duplicate_labels = sorted({label for label in labels if sum(label.casefold() == other.casefold() for other in labels) > 1})
    for label in duplicate_labels:
        errors.append(f"Duplicate glossary entry: {label}")
    for previous, following in zip(labels, labels[1:]):
        if sort_key(previous) > sort_key(following):
            errors.append(f"Glossary out of order: {previous} should follow {following}")
    missing = sorted(
        (item for item in referenced_items if not matching_entry(item, entries)),
        key=sort_key,
    )
    for item in missing:
        errors.append(f"Need a glossary entry for: {item}")
    if check_stranded:
        stranded = sorted(
            (
                label
                for label in labels
                if matching_entry(label, [(item, "") for item in referenced_items]) is None
            ),
            key=sort_key,
        )
        for label in stranded:
            errors.append(f"Glossary entry is not referenced: {label}")
    return errors


def write_custom_glossary(entries, referenced_items):
    selected = []
    seen = set()
    for item in referenced_items:
        entry = matching_entry(item, entries)
        if entry and entry not in seen:
            selected.append(entry)
            seen.add(entry)
    selected.sort(key=lambda entry: sort_key(ITEM_PATTERN.match(entry).group(1)))
    output = "\\chapter*{Glossary}\n\\begin{description}\n\n"
    output += "\n\n".join(selected)
    output += "\n\\end{description}\n"
    (REPOSITORY_ROOT / "CustomGlossary.tex").write_text(output)


def format_master_glossary(glossary_text, entries):
    start = glossary_text.index(r"\begin{description}") + len(r"\begin{description}")
    end = glossary_text.index(r"\end{description}", start)
    ordered_entries = sorted(entries, key=lambda entry: sort_key(entry[0]))
    body = "\n\n" + "\n\n".join(entry for _, entry in ordered_entries) + "\n"
    return glossary_text[:start] + body + glossary_text[end:]


def main():
    parser = argparse.ArgumentParser(description="Create, validate, or format a glossary.")
    parser.add_argument("--check", action="store_true", help="validate without writing CustomGlossary.tex")
    parser.add_argument("--check-stranded", action="store_true", help="also fail on unreferenced master entries")
    parser.add_argument("--format", action="store_true", help="alphabetize Glossary.tex in place")
    parser.add_argument("container_document", nargs="?", help="container .tex document")
    args = parser.parse_args()

    glossary_text = read_file(MAIN_GLOSSARY_FILE)
    entries = parse_entries(glossary_text)
    if args.format:
        MAIN_GLOSSARY_FILE.write_text(format_master_glossary(glossary_text, entries))
        print("Formatted Glossary.tex.")
        return 0
    if not args.container_document:
        parser.error("container_document is required unless --format is used")

    container = REPOSITORY_ROOT / args.container_document
    referenced_items = find_glossary_items(find_chapters(container))
    errors = validate(entries, referenced_items, args.check_stranded)
    for error in errors:
        print(error)
    if errors:
        return 1
    if args.check:
        print("Glossary check passed.")
        return 0
    write_custom_glossary(entries, referenced_items)
    return 0


if __name__ == "__main__":
    sys.exit(main())
