#!/bin/sh

set -eu

document=crl_desiderata
tex_file="$document.tex"
bib_file="$document.bib"
log_file="build/$document.log"
status=0
tab=$(printf '\t')

latexmk

for source_file in "$tex_file" "$bib_file"; do
    if matches=$(LC_ALL=C grep -an '[^[:print:][:space:]]' "$source_file"); then
        printf '%s\n' "Non-ASCII bytes found in $source_file:" >&2
        printf '%s\n' "$matches" >&2
        status=1
    fi

    if matches=$(LC_ALL=C grep -n "$tab" "$source_file"); then
        printf '%s\n' "Tab characters found in $source_file; use four spaces for indentation:" >&2
        printf '%s\n' "$matches" >&2
        status=1
    fi

    if matches=$(LC_ALL=C grep -nE ' +$' "$source_file"); then
        printf '%s\n' "Trailing spaces found in $source_file:" >&2
        printf '%s\n' "$matches" >&2
        status=1
    fi
done

if matches=$(grep -nE 'Citation .* undefined|Reference .* undefined|There were undefined (citations|references)' "$log_file"); then
    printf '%s\n' 'Undefined citations or references found:' >&2
    printf '%s\n' "$matches" >&2
    status=1
fi

if matches=$(grep -nE 'Overfull \\[hv]box' "$log_file"); then
    printf '%s\n' 'Overfull boxes found:' >&2
    printf '%s\n' "$matches" >&2
    status=1
fi

if [ "$status" -ne 0 ]; then
    printf '%s\n' 'Manuscript validation failed.' >&2
    exit "$status"
fi

printf '%s\n' 'Manuscript validation passed.'
