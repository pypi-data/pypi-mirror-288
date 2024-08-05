import subprocess
import sys
import os
import time

class ChangeLogGenerator:
    CHANGELOG_FILE = os.path.join('docs', 'CHANGELOG.md')
    HEADER = """# Change Log

## Overview

This document provides a detailed record of all changes made to the project. It includes version updates, new features, bug fixes, improvements, and any other modifications.

"""

    @staticmethod
    def ensure_header():
        """Ensure the changelog file contains the header."""
        if not os.path.exists(ChangeLogGenerator.CHANGELOG_FILE):
            os.makedirs(os.path.dirname(ChangeLogGenerator.CHANGELOG_FILE), exist_ok=True)
            with open(ChangeLogGenerator.CHANGELOG_FILE, 'w') as changelog_file:
                changelog_file.write(ChangeLogGenerator.HEADER)
        else:
            with open(ChangeLogGenerator.CHANGELOG_FILE, 'r+') as changelog_file:
                content = changelog_file.read()
                if not content.startswith(ChangeLogGenerator.HEADER):
                    changelog_file.seek(0, 0)
                    changelog_file.write(ChangeLogGenerator.HEADER + '\n' + content)

    @staticmethod
    def generate_changelog_content():
        """Generate the new changelog content using conventional-changelog."""
        print("Running conventional-changelog...")
        result = subprocess.run(
            ['npx', 'conventional-changelog', '-p', 'angular', '--infile', ChangeLogGenerator.CHANGELOG_FILE, '--same-file'],
            check=True,
            text=True,
            capture_output=True
        )
        print("Conventional-changelog output captured.")
        return result.stdout

    @staticmethod
    def remove_multiple_blank_lines(text):
        """Remove multiple consecutive blank lines from the text."""
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            if line.strip() != '' or (cleaned_lines and cleaned_lines[-1].strip() != ''):
                cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)

    @staticmethod
    def generate_changelog():
        try:
            # Ensure the header is present in the changelog file
            ChangeLogGenerator.ensure_header()
            
            time.sleep(10)  # Adding a delay to ensure file operations complete

            # Generate the new changelog content
            new_changelog_content = ChangeLogGenerator.generate_changelog_content()
            if new_changelog_content.strip():  # Check if the output is not empty or just whitespace
                # Remove multiple blank lines from the new changelog content
                cleaned_new_content = ChangeLogGenerator.remove_multiple_blank_lines(new_changelog_content)
                print("Cleaned new changelog content:")
                print(cleaned_new_content)

                # Read the existing content of the changelog file
                with open(ChangeLogGenerator.CHANGELOG_FILE, 'r') as changelog_file:
                    existing_content = changelog_file.read().strip()

                # Ensure header is present only once and prepare final content
                if existing_content.startswith(ChangeLogGenerator.HEADER):
                    existing_content = existing_content[len(ChangeLogGenerator.HEADER):].strip()

                # Combine header, new changelog content, and existing content
                final_output = ChangeLogGenerator.HEADER + '\n\n' + cleaned_new_content + '\n\n' + existing_content

                # Remove multiple blank lines from the final output
                final_output = ChangeLogGenerator.remove_multiple_blank_lines(final_output)
                print("Final output:")
                print(final_output)

                # Write the final output back to the file
                with open(ChangeLogGenerator.CHANGELOG_FILE, 'w') as changelog_file:
                    changelog_file.write(final_output.strip() + '\n')

                print("Changelog updated and header added if necessary.")

                # Stage the updated changelog for commit
                result = subprocess.run(['git', 'add', ChangeLogGenerator.CHANGELOG_FILE], check=True, text=True)
                print("Git add output:", result.stdout)
                print("Changelog staged for commit.")
            else:
                print("The changelog is empty or only contains whitespace. No changes made to CHANGELOG.md.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running subprocess: {e.stderr}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"Command not found: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    ChangeLogGenerator.generate_changelog()

if __name__ == "__main__":
    main()
