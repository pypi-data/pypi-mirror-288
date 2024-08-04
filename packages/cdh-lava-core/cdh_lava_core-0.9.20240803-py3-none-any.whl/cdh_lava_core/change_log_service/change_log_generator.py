import subprocess
import sys
import os

class ChangeLogGenerator:
    CHANGELOG_FILE = 'CHANGELOG.md'
    HEADER = """# Change Log

## Overview

This document provides a detailed record of all changes made to the project. It includes version updates, new features, bug fixes, improvements, and any other modifications.

"""

    @staticmethod
    def ensure_header(content):
        """Ensure the header is present in the content."""
        if not content.startswith(ChangeLogGenerator.HEADER):
            return ChangeLogGenerator.HEADER + '\n' + content
        return content

    @staticmethod
    def generate_changelog_content():
        """Generate the new changelog content using conventional-changelog."""
        print("Running conventional-changelog...")
        result = subprocess.run(
            ['npx', 'conventional-changelog', '-p', 'angular', '-i', ChangeLogGenerator.CHANGELOG_FILE, '-s'],
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
            # Generate the new changelog content
            new_changelog_content = ChangeLogGenerator.generate_changelog_content()
            if new_changelog_content.strip():  # Check if the output is not empty or just whitespace
                # Remove multiple blank lines from the new changelog content
                cleaned_new_content = ChangeLogGenerator.remove_multiple_blank_lines(new_changelog_content)

                # Read the existing content of the changelog file
                if os.path.exists(ChangeLogGenerator.CHANGELOG_FILE):
                    with open(ChangeLogGenerator.CHANGELOG_FILE, 'r') as changelog_file:
                        existing_content = changelog_file.read().strip()
                else:
                    existing_content = ""

                # Ensure header is present only once and prepare final content
                existing_content_with_header = ChangeLogGenerator.ensure_header(existing_content)

                # Prepare final content by combining new changelog content and existing content
                final_output = cleaned_new_content + '\n\n' + existing_content_with_header[len(ChangeLogGenerator.HEADER):]

                # Remove multiple blank lines from the final output
                final_output = ChangeLogGenerator.remove_multiple_blank_lines(final_output)

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
            raise
        except FileNotFoundError as e:
            print(f"Command not found: {e}", file=sys.stderr)
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            raise

def main():
    ChangeLogGenerator.generate_changelog()

if __name__ == "__main__":
    main()
