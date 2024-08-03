import logging
import os
import subprocess
from traceback import format_exc
from typing import Any

from git import Repo, Diff
from langchain_community.tools.github.prompt import CREATE_BRANCH_PROMPT, GET_ISSUES_PROMPT, DELETE_FILE_PROMPT, \
    READ_FILE_PROMPT
from langchain_core.pydantic_v1 import root_validator, BaseModel, create_model
from langchain_core.tools import ToolException
from pydantic.fields import FieldInfo

logger = logging.getLogger(__name__)
CREATE_FILE_PROMPT = """Create new file in your local repository."""

UPDATE_FILE_PROMPT = """
Updates the contents of a file in a GitHub repository. **VERY IMPORTANT**: Your input to this tool MUST strictly follow these rules:

- First you must specify which file to modify by passing a full file path (**IMPORTANT**: the path must not start with a slash)
- Then you must specify at lest 2 lines of the old contents which you would like to replace wrapped in OLD <<<< and >>>> OLD
- Then you must specify the new contents which you would like to replace the old contents with wrapped in NEW <<<< and >>>> NEW
- **VERY IMPORTANT**: NEW content may contain lines from OLD content in case you want to add content without removing the old content.

Example 1: you would like to replace the contents of the file /test/test.txt from "old contents" to "new contents", you would pass in the following string:

test/test.txt

This is text that will not be changed
OLD <<<<
old contents
>>>> OLD
NEW <<<<
new contents
>>>> NEW

Example 2: if you would like to add the contents of the file /test/test.txt where "existing contents" will be extended with "new contents", you would pass in the following string:

test/test.txt

This is text that will not be changed
OLD <<<<
existing contents
>>>> OLD
NEW <<<<
existing contents
new contents
>>>> NEW

"""

NoInput = create_model(
    "NoInput"
)

CheckOutCommit = create_model(
    "CheckOutCommit",
    commit_sha=(
        str, FieldInfo(description="Checkout commit SHA, for example, ac520b146fe3eaa2edbfaedb827f591320911cb0"))
)

DeleteFile = create_model(
    "DeleteFile",
    file_path=(str, FieldInfo(description="File path e.g test/inventory.py"))
)

CreateFile = create_model(
    "CreateFile",
    file_path=(str, FieldInfo(description="File path e.g test/inventory.py")),
    file_content=(str, FieldInfo(description="Content of a file to be put into chat."))
)

CommitChanges = create_model(
    "CommitChanges",
    commit_message=(str, FieldInfo(description="Descriptive commit message e.g changed file"))
)

CheckoutBranch = create_model(
    "CheckoutBranch",
    branch_name=(str, FieldInfo(description="Branch name to checkout to"))
)

ReadFile = create_model(
    "ReadFile",
    file_path=(str, FieldInfo(description="File path e.g test/inventory.py to read content from"))
)

UpdateFileContentByLines = create_model(
    "UpdateFileCommitByLines",
    file_path=(str, FieldInfo(description="File path e.g test/inventory.py to update in")),
    start_line_index=(int, FieldInfo(description="Start line index in the file from where update will start")),
    end_line_index=(int, FieldInfo(description="End line index in the file from where update will end")),
    new_content=(str, FieldInfo(description="New content which will be inserted in the file"))
)

UpdateFile = create_model(
    "UpdateFile",
    file_query=(str, FieldInfo(description="""File query by which the entire file content will be updated. 
                                              It contains file path and update instructions""")),
)


class LocalGit(BaseModel):
    repo_path: str
    base_path: str
    repo_url: str = None
    commit_sha: str = None

    @root_validator()
    def validate_toolkit(cls, values):
        repo_path = values['repo_path']
        base_path = values['base_path']
        repo_url = values.get('repo_url')
        commit_sha = values.get('commit_sha')
        os.makedirs(base_path, exist_ok=True)
        full_repo_path = os.path.join(base_path, repo_path)
        if not os.path.exists(full_repo_path) and repo_url:
            repo = Repo.clone_from(url=repo_url, to_path=str(full_repo_path))
        else:
            repo = Repo(path=str(full_repo_path))
        if commit_sha:
            repo.head.reset(commit=commit_sha, working_tree=True)
        values['repo'] = repo
        return values

    def extract_old_new_pairs(self, file_query):
        # Split the file content by lines
        code_lines = file_query.split("\n")

        # Initialize lists to hold the contents of OLD and NEW sections
        old_contents = []
        new_contents = []

        # Initialize variables to track whether the current line is within an OLD or NEW section
        in_old_section = False
        in_new_section = False

        # Temporary storage for the current section's content
        current_section_content = []

        # Iterate through each line in the file content
        for line in code_lines:
            # Check for OLD section start
            if "OLD <<<" in line:
                in_old_section = True
                current_section_content = []  # Reset current section content
                continue  # Skip the line with the marker

            # Check for OLD section end
            if ">>>> OLD" in line:
                in_old_section = False
                old_contents.append("\n".join(current_section_content).strip())  # Add the captured content
                current_section_content = []  # Reset current section content
                continue  # Skip the line with the marker

            # Check for NEW section start
            if "NEW <<<" in line:
                in_new_section = True
                current_section_content = []  # Reset current section content
                continue  # Skip the line with the marker

            # Check for NEW section end
            if ">>>> NEW" in line:
                in_new_section = False
                new_contents.append("\n".join(current_section_content).strip())  # Add the captured content
                current_section_content = []  # Reset current section content
                continue  # Skip the line with the marker

            # If currently in an OLD or NEW section, add the line to the current section content
            if in_old_section or in_new_section:
                current_section_content.append(line)

        # Pair the OLD and NEW contents
        paired_contents = list(zip(old_contents, new_contents))

        return paired_contents

    def checkout_commit(self, commit_sha: str) -> str:
        """ Checkout specific commit from repository """
        try:
            self.repo.head.reset(commit=commit_sha, working_tree=True)
            return 'Successfully checked out commit {}'.format(commit_sha)
        except Exception:
            stacktrace = format_exc()
            logger.error(
                f"Error checking out the commit from repo - {self.repo_path} using following commit hash - {commit_sha}: {stacktrace}")
            return 'Unable to checkout commit - {}'.format(commit_sha)

    def get_diff(self) -> str:
        """ Show difference of the file for which changes have been made"""
        output = subprocess.run(
            ["git", "diff"], cwd=self.repo.working_dir, check=True, text=True, capture_output=True
        )

        return output.stdout

    def delete_file(self, file_path: str) -> str:
        """ Delete file from the repository by its path """
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            return 'Successfully deleted file {}'.format(file_path)
        else:
            return f"File '{file_path}' cannot be deleted because it does not exist"

    def create_file(self, file_path: str, file_content: str) -> str:
        """ Create file in repository by specific path and content """
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return f"File - '{file_path}' already exists"
        else:
            with open(file_path, 'w') as f:
                f.write(file_content)
            self.repo.index.add([file_path])
        return 'Successfully created file {} with content - {}'.format(file_path, file_content)

    def commit_changes(self, commit_message: str) -> str:
        """ Commit changes to the repo """
        self.repo.index.commit(commit_message)
        return f'Successfully committed changes with the commit message - {commit_message}'

    def checkout_branch(self, branch_name: str) -> str:
        """ Checkout specific branch of repository """
        self.repo.git.checkout(branch_name)
        return 'Successfully checked out branch {}'.format(branch_name)

    def read_file(self, file_path: str) -> str:
        """ Read file from repository """
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        else:
            return "File '{}' cannot be read because it is not existed".format(file_path)

    def update_file_content_by_lines(self, file_path: str, start_line_index: int, end_line_index: int,
                                     new_content: str) -> str:
        """ Update file content by lines """
        # Validate line numbers
        if start_line_index < 1 or end_line_index < start_line_index:
            raise ToolException(
                f"Invalid start or end line number during content update for file {file_path} with content {new_content}")

        try:
            # Read the file into a list of lines
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Ensure the end line is within the bounds of the file
            if end_line_index > len(lines):
                raise ToolException("End line number exceeds the number of lines in the file")

            # Split the new content into lines
            new_content_lines = new_content.splitlines()

            # Ensure the new content has the same number of lines as the range being replaced
            if len(new_content_lines) != (end_line_index - start_line_index + 1):
                raise ToolException("The number of lines in the new content does not match the range being replaced")

            # Update the lines within the specified range, preserving indentation
            for i in range(start_line_index - 1, end_line_index):
                original_line = lines[i]
                new_line = new_content_lines[i - (start_line_index - 1)]
                leading_spaces = len(original_line) - len(original_line.lstrip())
                indented_new_line = ' ' * leading_spaces + new_line.lstrip()
                lines[i] = indented_new_line + '\n'

            # Write the updated lines back to the file
            with open(file_path, 'w') as file:
                file.writelines(lines)

            logger.info(f"File '{file_path}' updated successfully.")
            return f"File '{file_path}' updated successfully with following content: {new_content}."
        except Exception as e:
            logger.error(f"Error updating file '{file_path}': {e}")
            return f"Unable to update file '{file_path}' with content: {new_content}"

    def update_file(self, file_query: str) -> str:
        """ Updates a file with new content. """
        try:

            file_path: str = file_query.split("\n")[0]

            file_content = self.read_file(file_path)
            updated_file_content = file_content
            for old, new in self.extract_old_new_pairs(file_query):
                if not old.strip():
                    continue
                updated_file_content = updated_file_content.replace(old, new)

            if file_content == updated_file_content:
                return (
                    "File content was not updated because old content was not found or empty."
                    "It may be helpful to use the read_file action to get "
                    "the current file contents."
                )

            with(open(file_path, 'w')) as f:
                f.write(updated_file_content)
            return "Updated file " + str(file_path)
        except Exception as e:
            return "Unable to update file due to error:\n" + str(e)

    def get_available_tools(self):
        return [
            {
                "ref": self.create_file,
                "name": "create_file",
                "mode": "create_file",
                "description": CREATE_FILE_PROMPT,
                "args_schema": CreateFile,
            },
            {
                "ref": self.read_file,
                "name": "read_file",
                "mode": "read_file",
                "description": """Useful when you need to read the contents of a file. Simply pass in the full file path of the file you would like to read. **IMPORTANT**: the path must not start with a slash""",
                "args_schema": ReadFile,
            },
            {
                "ref": self.update_file,
                "name": "update_file",
                "mode": "update_file",
                "description": UPDATE_FILE_PROMPT,
                "args_schema": UpdateFile,
            },
            {
                "ref": self.delete_file,
                "name": "delete_file",
                "mode": "delete_file",
                "description": """Useful when you need to delete a file in a local repository. Simply pass in the full file path of the file you would like to delete. **IMPORTANT**: the path must not start with a slash""",
                "args_schema": DeleteFile,
            },
            {
                "ref": self.checkout_branch,
                "name": "checkout_branch",
                "mode": "checkout_branch",
                "description": "This tool is designed to checkout particular branch by its name. You should pass the branch name to this tool.",
                "args_schema": CheckoutBranch,
            },
            {
                "ref": self.checkout_commit,
                "name": "checkout_commit",
                "mode": "checkout_commit",
                "description": "This tool should be used to checkout specific commit from the repository. You should provide commit hash to the tool e.g. 'ac520b146fe3eaa2edbfaedb827f591320911cb0'.",
                "args_schema": CheckOutCommit,
            },
            {
                "ref": self.get_diff,
                "name": "get_diff",
                "mode": "get_diff",
                "description": "This tool provide the difference report after changes performed in the repository. No input needed.",
                "args_schema": NoInput,
            },
            {
                "ref": self.update_file_content_by_lines,
                "name": "update_file_content_by_lines",
                "mode": "update_file_content_by_lines",
                "description": "This tool is designed to do content update by start and en indexes in the file. Following parameters should be passed to the tool: full file path where content should be changed, start line index - the index from where update should start, end line index - the line index where update will end, new conten which should be placed into the file.",
                "args_schema": UpdateFileContentByLines,
            }
        ]

    def run(self, name: str, *args: Any, **kwargs: Any):
        for tool in self.get_available_tools():
            if tool["name"] == name:
                return tool["ref"](*args, **kwargs)
        else:
            raise ValueError(f"Unknown mode: {name}")
