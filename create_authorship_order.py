#
# Scan a container document for chapter authors, and determines
# author ordering on the basis of authors listed with the 
# \chapterauthor command
# 
# Usage: python create_authorship_order.py <ContainerDocument>.tex
# 
# Assumes chapter author lists are associated with an \authorweights command
# If none is found then assume equal authorship amongst chapter co-authors
#
import sys
import re
import os
from collections import defaultdict
import operator

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

#
# Loop through chapters. Find unique book authors. Add them to a dictionary.
# Find author weightings and add them to current summed weightings in that
# author's dictionary entry. This creates an ordering on authors.
# 
# TODO: Check that ties are broken alphabetically
#
book_authors = defaultdict(int) # Author to summed weightings
for chapter in included_chapters:
    with open(chapter, 'r') as textfile:
        text = textfile.read()
        # TODO: Will this work on commented out \chapterauthor?
        # TODO: Allow for curly braces in the regex (e.g. {\''e} fails) 
        reg_author = re.compile(r"\\chapterauthor\{([^}]+)\}(\{[^}]+\})*")
        for match in re.findall(reg_author, text):
            names = match[0].split(",")
            # No weightings provided
            if(match[1] == ""):
                if(len(names) == 1):
                    book_authors[names[0].strip()] += 1
                else:
                    for name in names:
                        book_authors[name.strip()] += 1/float(len(names))

            # Weightings provided
            else:
                weights = match[1].strip("{}").split(",")
                for i,name in enumerate(names):
                    book_authors[name.strip()] += float(weights[i])

#
# Sort author list by sum of their weighted contribution
#
# factor=1.0/sum(book_authors.values())
# for author in book_authors:
#   book_authors[author] = book_authors[author]*factor
sorted_authors = sorted(book_authors.items(), key=operator.itemgetter(1), reverse=True)
print("Ordering:", str(sorted_authors).strip("[]"))
sorted_authors = [i[0] for i in sorted_authors]
author_string = ', '.join(sorted_authors)

#
# Function to split the author string into chunks of a given size
#
def split_author_string(author_string, max_length=80):
    words = author_string.split(", ")
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 2 > max_length:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += ", " + word
            else:
                current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return r"\\ ".join(lines)

#
# Write ordered authorship list to container document
#
with open(CONTAINER_DOCUMENT, 'r') as input_file, open('_temp.tex', 'w') as output_file:
    for line in input_file:
        if line.startswith("\\author"):
            # Replace author_string with the split version
            formatted_author_string = split_author_string(author_string)
            output_file.write(r"\author{" + formatted_author_string + "}\n")
        else:
            output_file.write(line)


os.rename('_temp.tex', CONTAINER_DOCUMENT)