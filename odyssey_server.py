import os
import re

# Define the codebase and its corresponding directory
codebase_dir = "/home/eijiotieno/Projects/odyssey-server"

# Directories to include for this codebase
include_dirs = [
    "prisma",
    "src",
    "tools",
]  # Explicitly include subfolders

# Define the specific file extensions to be considered
accepted_extensions = [
    ".ts",
    ".js",
    ".prisma",
    ".json",
]  # Add the extensions you want to include

# Output file where the combined codebase will be saved
output_file = "output/odyssey_server.txt"


def remove_comments(code):
    """
    Remove single-line and multi-line comments from the code.
    """
    # Remove single-line comments (//)
    code = re.sub(r"//.*", "", code)
    # Remove multi-line comments (/* ... */)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    # Remove any additional newlines or spaces
    code = re.sub(
        r"\n\s*\n+", "\n", code
    )  # Replace multiple newlines with a single newline
    return code.strip()  # Remove leading/trailing whitespace


# Clear the output file by opening it in write mode
with open(output_file, "w") as output:
    for dir_to_include in include_dirs:
        full_path = os.path.join(codebase_dir, dir_to_include)

        for root, dirs, files in os.walk(full_path):
            for file in files:
                # Check for accepted file extensions
                if not any(file.endswith(ext) for ext in accepted_extensions):
                    continue

                # Exclude files that end with .ico
                if file.endswith(".ico"):
                    continue

                file_path = os.path.join(root, file)

                # Construct the relative path starting from the codebase directory
                relative_path = os.path.relpath(
                    file_path, codebase_dir
                )  # Get relative path from codebase
                relative_path_with_slash = "/" + relative_path  # Add leading slash

                try:
                    with open(file_path, "r") as f:
                        # Write the file path
                        output.write("Path: " f"{relative_path_with_slash}\n\n")

                        # Read and clean the content
                        code_content = f.read()
                        cleaned_code = remove_comments(
                            code_content
                        )  # Remove comments from the code

                        if cleaned_code:  # Only write if there's any code left
                            output.write(cleaned_code)  # Write cleaned content
                            output.write("\n")  # Add a newline after the content

                        # Add a separator between file contents (3 dashes long)
                        output.write(f"---\n")  # Line separator between files
                except Exception as e:
                    output.write(
                        f"Error reading file: {relative_path_with_slash}\n"
                    )  # Shortened error message

    # Add a final newline for clarity at the end of the file
    output.write("\n")
