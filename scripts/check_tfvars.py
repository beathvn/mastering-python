#!/usr/bin/env python3
import sys
import re
import argparse

EXPECTED_VALUES = {"environment": "__environment__", "region": "__terraform_region__"}


def extract_values(content):
    # Match variable assignments, ignoring comments
    pattern = r'^\s*([\w-]+)\s*=\s*"([^"]*)"'
    values = {}
    for line in content.splitlines():
        match = re.match(pattern, line)
        if match:
            values[match.group(1)] = match.group(2)
    return values


def fix_values(filename, content):
    new_lines = []
    pattern = r'^(\s*)([\w-]+)(\s*=\s*)"([^"]*)"(.*)$'

    for line in content.splitlines():
        match = re.match(pattern, line)
        if match and match.group(2) in EXPECTED_VALUES:
            indent, var_name, equals, _, comment = match.groups()
            new_value = EXPECTED_VALUES[var_name]
            new_lines.append(f'{indent}{var_name}{equals}"{new_value}"{comment}')
        else:
            new_lines.append(line)

    with open(filename, "w") as f:
        f.write("\n".join(new_lines) + "\n")

    # Return True if changes were made
    return content != "\n".join(new_lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="Files to check")
    args = parser.parse_args()

    exit_code = 0
    for filename in args.files:
        with open(filename, "r") as f:
            content = f.read()
            actual_values = extract_values(content)

            if actual_values != EXPECTED_VALUES:
                print(f"Error: {filename} variable values are incorrect!")
                print("Expected values:")
                print(EXPECTED_VALUES)
                print("Actual values:")
                print(actual_values)

                # Always try to fix
                changes_made = fix_values(filename, content)
                if changes_made:
                    print(f"Fixed {filename}")
                    # Re-read the file to verify it was fixed correctly
                    with open(filename, "r") as f:
                        new_content = f.read()
                        if extract_values(new_content) != EXPECTED_VALUES:
                            exit_code = 1
                else:
                    exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
