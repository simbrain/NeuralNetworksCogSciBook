"""Prepare a LaTeX container document for local builds and releases.

Updates the generated author line, then verifies every glossary reference has
an entry in Glossary.tex.  It can also generate CustomGlossary.tex and change
the container document to include it.
"""

import argparse
from pathlib import Path
import re
import subprocess
import sys


SCRIPTS_DIRECTORY = Path(__file__).resolve().parent
REPOSITORY_ROOT = SCRIPTS_DIRECTORY.parent


def run(script, *arguments):
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIRECTORY / script), *arguments],
        cwd=REPOSITORY_ROOT,
        check=True,
    )


def use_custom_glossary(document):
    """Select the generated glossary in a custom container document."""
    contents = document.read_text()
    updated_contents, replacements = re.subn(
        r"(?m)^(\s*)\\input\{Glossary\}",
        r"\1\\input{CustomGlossary}",
        contents,
    )
    if replacements:
        document.write_text(updated_contents)
        return
    if re.search(r"(?m)^\s*\\input\{CustomGlossary\}", contents):
        return
    updated_contents, replacements = re.subn(
        r"(?m)^(\s*)%\s*\\input\{CustomGlossary\}",
        r"\1\\input{CustomGlossary}",
        contents,
    )
    if replacements:
        document.write_text(updated_contents)
        return
    raise ValueError(
        f"{document.name} does not include Glossary.tex or CustomGlossary.tex"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Update authorship and validate glossary entries for a container document."
    )
    parser.add_argument("container_document", help="path to the container .tex document")
    parser.add_argument(
        "--write-custom-glossary",
        action="store_true",
        help="write CustomGlossary.tex after validation succeeds",
    )
    parser.add_argument(
        "--use-custom-glossary",
        action="store_true",
        help="replace \\input{Glossary} with \\input{CustomGlossary}",
    )
    parser.add_argument(
        "--check-stranded-glossary-entries",
        action="store_true",
        help="also fail if a master glossary entry is not referenced",
    )
    args = parser.parse_args()

    document = Path(args.container_document)
    if not document.is_absolute():
        document = REPOSITORY_ROOT / document
    document = document.resolve()

    if document.suffix != ".tex" or not document.is_file():
        parser.error(f"container document not found: {args.container_document}")
    try:
        document_argument = str(document.relative_to(REPOSITORY_ROOT))
    except ValueError:
        parser.error("container document must be inside this repository")

    run("create_authorship_order.py", document_argument)
    check_arguments = ["--check"]
    if args.check_stranded_glossary_entries:
        check_arguments.append("--check-stranded")
    run("create_custom_glossary.py", *check_arguments, document_argument)
    if args.write_custom_glossary or args.use_custom_glossary:
        run("create_custom_glossary.py", document_argument)
    if args.use_custom_glossary:
        try:
            use_custom_glossary(document)
        except ValueError as error:
            parser.error(str(error))

    print(f"Prepared {document_argument}.")


if __name__ == "__main__":
    main()
