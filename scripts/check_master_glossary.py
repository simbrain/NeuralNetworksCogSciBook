"""Validate the canonical glossary used by the master book."""

import sys

from create_custom_glossary import (
    MAIN_GLOSSARY_FILE,
    REPOSITORY_ROOT,
    find_chapters,
    find_glossary_items,
    parse_entries,
    read_file,
    validate,
)


def main():
    entries = parse_entries(read_file(MAIN_GLOSSARY_FILE))
    master_document = REPOSITORY_ROOT / "NeuralNetworksCogsci.tex"
    referenced_items = find_glossary_items(find_chapters(master_document))
    errors = validate(entries, referenced_items, check_stranded=False)
    for error in errors:
        print(error)
    if errors:
        return 1
    print("Master glossary check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
