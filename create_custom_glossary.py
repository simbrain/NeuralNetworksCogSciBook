# Script to create a custom glossary for a container document.
# 
# Usage: python create_custom_glossary.py <ContainerDocument>.tex
#
# Structure:
# - Find all \glossary instances in all chapters of the specified container document
# - Search for a match for each glossary item in the main glossary file (Glossary.tex).
# - Add matching entries to the custom glossary file (CustomGlossary.tex).
#
# Notes:
# - Unmatched \glossary items are noted in the terminal.
# - The script handles both singular and plural forms of glossary items.
# - Comments are ignored both in glossary and in chapters of the container doc 
# 
# TODO: Add colon after each entry but without the space \item adds.

import sys
import re
import os

MAIN_GLOSSARY_FILE = "Glossary.tex"

def read_file(file_path):
    try:
        with open(file_path, 'r') as textfile:
            return textfile.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        sys.exit(1)

def find_chapters(container_document):
    chapters = []
    content = read_file(container_document)
    for line in content.split('\n'):
        if line.startswith("%"):
            continue
        match = re.search(r"^\\input{([^}]+)}", line)
        if match:
            chapters.append(match.group(1) + ".tex")
    return chapters

def find_glossary_items(files):
    items = set()
    for file in files:
        content = read_file(file)
        for line in content.split('\n'):
            if line.startswith("%"):
                continue
            items.update(re.findall(r'\\glossary(?:\[[^\]]*\])?{([^}]+)}', line))
    return sorted(item.lower() for item in items)

def create_custom_glossary(glossary_items, glossary_text):
    added_entries = set()
    custom_glossary_entries = []
    
    for item in glossary_items:
        singular_item = item.rstrip('s')
        pattern = rf'\b{re.escape(singular_item)}s?\b'
        
        if re.search(pattern, glossary_text, re.IGNORECASE):
            for line in glossary_text.split('\n'):
                if re.search(pattern, line, re.IGNORECASE):
                    if line not in added_entries:
                        custom_glossary_entries.append(line)
                        added_entries.add(line)
        else:
            print(f"Need a glossary entry for: {item}")
    
    custom_glossary_entries.sort()
    
    with open("CustomGlossary.tex", "w") as custom_glossary:
        custom_glossary.write("\\chapter*{Glossary}\n\\begin{description}\n")
        for entry in custom_glossary_entries:
            custom_glossary.write(entry + '\n')
        custom_glossary.write("\\end{description}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_custom_glossary.py <ContainerDocument>.tex")
        sys.exit(1)
    
    container_document = sys.argv[1]
    chapters = find_chapters(container_document)
    glossary_items = find_glossary_items(chapters)
    glossary_text = read_file(MAIN_GLOSSARY_FILE)
    create_custom_glossary(glossary_items, glossary_text)

if __name__ == "__main__":
    main()
