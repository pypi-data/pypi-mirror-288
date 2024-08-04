import subprocess
import sys

class ChangelogGenerator:
    @staticmethod
    def generate_changelog():
        try:
            print("Running conventional-changelog...")
            # Run the conventional-changelog command
            result = subprocess.run(
                ['npx', 'conventional-changelog', '-p', 'angular', '-i', 'CHANGELOG.md', '-s'],
                check=True,
                text=True,
                capture_output=True
            )
            print("Conventional-changelog output:", result.stdout)
            print("Changelog generated successfully.")

            # Stage the updated changelog for commit
            result = subprocess.run(['git', 'add', 'CHANGELOG.md'], check=True, text=True)
            print("Git add output:", result.stdout)
            print("Changelog staged for commit.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running subprocess: {e.stderr}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"Command not found: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    ChangelogGenerator.generate_changelog()
