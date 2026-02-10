#!/bin/bash

# Get parent of parent directory of this script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
parent_dir="$(cd "$(dirname "$script_dir")" && pwd)"
top_dir="$(cd "$(dirname "$parent_dir")" && pwd)"

# Check if README.md exists
if [ ! -f "$top_dir/README.md" ]; then
    echo "\n✗ Error: README.md not found"
    exit 1
fi

readme_file="$top_dir/README.md"
sha=$(git log --oneline --diff-filter=A -- README.md | awk '{print $1}')
diff_output=$(git diff $sha HEAD README.md)
lines_changed=$(echo "$diff_output" | grep -e "^\+" | wc -l)

echo "README.md has $lines_changed lines changed"

# check if the number of lines changed is greater than 20, if so, meets requirements otherwise error
if ((lines_changed > 20)); then
    echo -e "\n✓ README.md meets all requirements"
    exit 0
else
    echo -e "\n✗ README.md does not meet requirements (modify it further)"
    exit 1
fi 
