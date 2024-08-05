import argparse
import hashlib
import os
import subprocess
import re

class Application:
    def __init__(self):
        self.name = "vergen"
        self.description = "vergen is a version generator which uses git tags to generate a branch-dependent version."
        self.version = "1.0.1"

    def run(self):
        parser = argparse.ArgumentParser(prog=self.name, description=self.description)
        parser.add_argument("--version", action="version", version=f"%(prog)s {self.version}")
        parser.add_argument("--verbose", action="store_true", help="print verbose information")

        args = parser.parse_args()

        if not self.__is_git_working_directory():
            raise RuntimeError("Current working directory is not a git-controlled directory.")

        branch = self.__get_active_branch()
        tag = self.__get_latest_tag()
        commit_count = self.__get_commit_count_since_tag(tag)
        version = self.__generate_version(branch, tag, commit_count)

        if args.verbose:
            print(f"Active branch: {branch}")
            print(f"Latest tag: {tag}")
            print(f"Commits since tag: {commit_count}")
            print(f"Generated version: {version}")
        else:
            print(version)

    def __is_git_working_directory(self):
        return os.path.exists(".git")

    def __get_active_branch(self):
        try:
            result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, check=True, text=True)
            return result.stdout.strip()
        except Exception:
            raise RuntimeError("Cannot find the active branch.")

    def __get_latest_tag(self):
        # Retrieve all tags matching the broad pattern
        try:
            result = subprocess.run(
                ["git", "tag", "--list", "[0-9]*.[0-9]*"],
                stdout=subprocess.PIPE,
                check=True,
                text=True
            )
        except subprocess.CalledProcessError:
            raise RuntimeError("Cannot find the latest tag.")

        # Split the output into individual tags
        tags = result.stdout.split()

        # Define a regex pattern to match only X.Y format tags
        pattern = re.compile(r"^\d+\.\d+$")

        # Filter tags that match the precise pattern
        filtered_tags = [tag for tag in tags if pattern.match(tag)]

        # Find the latest tag among the filtered tags using `git describe`
        latest_tag = None
        for tag in filtered_tags:
            try:
                # Check if the tag is reachable from the current commit
                subprocess.run(["git", "describe", "--tags", tag], stdout=subprocess.DEVNULL, check=True)
                latest_tag = tag
            except subprocess.CalledProcessError:
                continue

        if latest_tag is None:
            raise RuntimeError("Cannot find the latest tag.")

        return latest_tag

    def __get_commit_count_since_tag(self, tag):
        try:
            result = subprocess.run(["git", "rev-list", f"{tag}..HEAD", "--count"], stdout=subprocess.PIPE, check=True, text=True)
            return int(result.stdout.strip())
        except Exception:
            raise RuntimeError("Cannot count commits since the latest tag.")

    def __generate_version(self, branch, major_minor, commit_count):
        if branch in {"main", "master"}:
            return f"{major_minor}.{commit_count}"
        elif branch == "develop":
            branch_id = 1
        elif branch.startswith("hotfix/"):
            branch_id = self.__hash(branch, 10, 99)
        elif branch.startswith("release/"):
            branch_id = self.__hash(branch, 100, 999)
        elif branch.startswith("feature/"):
            branch_id = self.__hash(branch, 1000, 9999)
        else:
            raise RuntimeError(f"Unexpected branch: {branch}")
        
        return f"{major_minor}.{commit_count}.{branch_id}"
    
    def __hash(self, branch, min_version, max_version):
        count = max_version - min_version + 1
        return int(hashlib.sha256(branch.encode()).hexdigest(), 16) % count + min_version
