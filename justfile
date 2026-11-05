python := env_var_or_default("PYTHON", "python3")

# Show the two usual build paths.
default:
    @echo
    @echo "Master book:"
    @echo "  just build-master"
    @echo
    @echo "Container document (for example Book_124):"
    @echo "  just build Book_124"
    @echo "  (.tex is optional)"
    @echo

# Prepare and compile a container document using the existing authorship and
# custom-glossary scripts, so its PDF has current metadata and glossary.
build document:
    {{python}} scripts/prepare_container_document.py {{document}} --use-custom-glossary
    @{{just_executable()}} compile {{document}}

# Backwards-compatible name for the container build recipe.
prep document:
    @{{just_executable()}} build {{document}}

# Prepare and compile the master without replacing its canonical glossary.
build-master document="NeuralNetworksCogsci.tex":
    {{python}} scripts/prepare_container_document.py {{document}}
    @{{just_executable()}} compile {{document}}

# Compile only (no author or glossary update), with SyncTeX for editor/PDF sync.
# Tagged documents exhaust pdfTeX's default memory when serializing the parent
# tree, so the limits are raised here; plain pdflatex (e.g. TeXShop's default
# LaTeX command) dies at \end{document} and can leave a truncated .aux file.
# The TeXShop engine in scripts/BookBuild.engine calls this recipe.
compile document:
    extra_mem_top=50000000 extra_mem_bot=50000000 pool_size=20000000 max_strings=1000000 hash_extra=1000000 save_size=200000 latexmk -pdf -synctex=1 -interaction=nonstopmode -halt-on-error -e '$max_repeat=9' {{document}} || { echo; echo "Build failed. If the error looks unrelated to your edits (e.g. a Runaway argument at the start of the document, or latexmk reporting an error from a previous invocation), an interrupted build may have left stale auxiliary files. Run: just clean {{document}}  and then rebuild."; exit 1; }

# Update the master document's author line and validate its full glossary.
prep-master document="NeuralNetworksCogsci.tex":
    {{python}} scripts/prepare_container_document.py {{document}}

# Remove a document's generated auxiliary files (keeps the PDF). Use this when a
# build fails because an interrupted run left a truncated .aux or similar file.
clean document:
    latexmk -c {{document}}
    rm -f "{{without_extension(document)}}.bbl" "{{without_extension(document)}}.synctex(busy)"

# Check glossary coverage without changing a container document.
check-glossary document="NeuralNetworksCogsci.tex":
    {{python}} scripts/create_custom_glossary.py --check {{document}}

# Validate the canonical glossary and its references in the full book.
check-master-glossary:
    {{python}} scripts/check_master_glossary.py

# Audit for master glossary entries that are not referenced in the full book.
check-stranded-glossary:
    {{python}} scripts/create_custom_glossary.py --check --check-stranded NeuralNetworksCogsci.tex

# Alphabetize the canonical master glossary after editing it.
format-glossary:
    {{python}} scripts/create_custom_glossary.py --format

# Run the Release workflow (builds PDF, creates draft release); version defaults to next Year.N
release version="":
    #!/usr/bin/env bash
    set -euo pipefail
    git fetch --quiet origin main
    warn=""
    [ -n "$(git status --porcelain)" ] && warn="${warn}- uncommitted changes\n"
    [ -n "$(git log origin/main..HEAD --oneline)" ] && warn="${warn}- unpushed commits\n"
    if [ -n "$warn" ]; then
        printf "Warning: the release builds origin/main, which won't include your:\n${warn}"
        read -r -p "Continue anyway? [y/N] " ok
        [ "$ok" = y ] || exit 1
    fi
    gh workflow run release.yml {{ if version != "" { "-f version=" + version } else { "" } }}
    sleep 5
    gh run watch $(gh run list --workflow=release.yml --limit 1 --json databaseId -q '.[0].databaseId')
    echo "Edit the notes on the releases page, then publish there or with: just release-publish <tag>"

# Publish a draft release, e.g. just release-publish v2026.3
release-publish tag:
    gh release edit {{tag}} --draft=false

# Delete a release and its tag so the workflow can be re-run, e.g. just release-delete v2026.3
release-delete tag:
    gh release delete {{tag}} --cleanup-tag --yes
    -git tag -d {{tag}}
