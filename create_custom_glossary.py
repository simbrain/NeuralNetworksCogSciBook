# Script to create a custom glossary for the chapters included in a container document. Finds all \glossary instances in these files. Searches for a match for each in the main glossary file (glossary.tex). All matches are added to the custom glossary.
#
# Unmatched \glossary items are noted
#
# Usage:python create_custom_glossary.py <ContainerDocument>.tex
#
# TODO: Add optional [glossary_key] argument of glossary items to be used as a key. Example: \glossary[activation]{Activations}  
# 
# TODO: Currently if two glossary items overlap in a word they get repeated.
# 

import sys
import re

CONTAINER_DOCUMENT = sys.argv[1]

# 
# Find chapters in container document
# 
included_chapters = []
with open(CONTAINER_DOCUMENT, 'r') as textfile:
    text = textfile.read()
    for line in text.split('\n'):
        # Ignore commented-out lines in .tex file
        regex = r"^\\input{(\w+)"
        match = re.search(regex,line)
        if (match is not None):
            if(len(match.groups())>0):
                included_chapters.append(match.group(1)+".tex")

# Find all the glossary items in the specified .tex files
glossary_items = []
for file in included_chapters:
    with open(file, 'r') as textfile:
        text = textfile.read()
        for line in text.split('\n'):
            # Ignore commented-out lines in .tex file
            if (line.startswith("%")):
                continue
            else:
                glossary_items += (re.findall(r'\\glossary{([\w\- ]+)}', line))

glossary_items = {x.lower() for x in glossary_items} # Use a set to avoid duplicates
glossary_items = list(glossary_items)
glossary_items.sort()


# Create the custom glossary file
custom_glossary = open("CustomGlossary.tex", "w")
string = """\\chapter*{Glossary}
\\begin{description}\n
"""
custom_glossary.write(string)

def contains_word(word, string):
    if(len(re.findall(word, string, re.IGNORECASE))):
        return True
    else:
        return False

# TODO: Fail case still not working
# 
# Scan the glossary file for matches and populate the custom glossary,
# or notify the user that a glossary item is needed
with open("Glossary.tex", 'r') as glossary_file:
    glossary_text = glossary_file.read()
    for glossary_item in glossary_items:
        # print(contains_word(glossary_item, glossary_text))
        if (contains_word(glossary_item, glossary_text)):
            for line in glossary_text.split('\n'):
                if("[" + glossary_item + "]" in line.lower()):
                    custom_glossary.write(line + '\n')
        else:
            print("Need a glossary entry for: ", glossary_item)
    custom_glossary.write("\\end{description}")
