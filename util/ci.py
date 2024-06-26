# Import Statements
# ----------------------------------------------------------------
from json import load
from typing import Final
from shutil import rmtree
from os.path import isdir, join
from os import getcwd, listdir, makedirs

# ---

# ---

# ----------------------------------------------------------------

# File Docstring
# --------------------------------
# CI/CD workflow for updating project templates.
#
# @author @MaxineToTheStars <https://github.com/MaxineToTheStars>
# ----------------------------------------------------------------


# Class Definitions
class CI:
    # Enums

    # Interfaces

    # Constants
    TEMPLATE_DICTIONARY: dict[str, str] = None
    SOURCE_TEMPLATES_INPUT_DIRECTORY: Final[str] = getcwd().replace("/util", "/src")
    SOURCE_TEMPLATES_OUTPUT_DIRECTORY: Final[str] = getcwd().replace("/util", "/templates")
    EXCLUDE_FROM_EMBEDDED_DIRECTORY_CREATION: Final[list[str]] = ["configs", "misc"]

    # Public Variables

    # Private Variables

    # Constructor

    # Public Static Methods

    # Public Inherited Methods
    def runCI(self) -> None:
        """
        Runs the CI workflow.

        @return None - None
        """

        # Open the template dictionary
        with open("./dict.json", "r") as templateDictionary:
            # Save/load to memory
            self.TEMPLATE_DICTIONARY = load(templateDictionary)

            # Close the file handle
            templateDictionary.close()

        # Check if the output directory exists
        if isdir(self.SOURCE_TEMPLATES_OUTPUT_DIRECTORY) == True:
            # Delete the directory
            rmtree(self.SOURCE_TEMPLATES_OUTPUT_DIRECTORY)

        # Create a new output directory
        makedirs(self.SOURCE_TEMPLATES_OUTPUT_DIRECTORY)

        # Get all directories in the input directory
        allFoundInputDirectories: Final[list[str]] = listdir(self.SOURCE_TEMPLATES_INPUT_DIRECTORY)

        # Main process loop
        for foundInputDirectory in allFoundInputDirectories:
            # Get the full input directory base path
            fullInputDirectoryBasePath: Final[str] = join(self.SOURCE_TEMPLATES_INPUT_DIRECTORY, foundInputDirectory)

            # Get the full output directory base path
            fullOutputDirectoryBasePath: Final[str] = join(self.SOURCE_TEMPLATES_OUTPUT_DIRECTORY, foundInputDirectory)

            # Get all the files in the input directory
            allFoundInputFiles: Final[list[str]] = listdir(fullInputDirectoryBasePath)

            # Process files
            for foundInputFile in allFoundInputFiles:
                # Check if the file is NOT a (dot) file
                if (foundInputFile.startswith(".") == False and foundInputDirectory not in self.EXCLUDE_FROM_EMBEDDED_DIRECTORY_CREATION):
                    # Get the embedded file directory
                    embeddedFileDirectory: Final[list[str]] = foundInputFile.split(".")

                    # Amend directory paths
                    generatedPaths: str = ""
                    for path in range(0, len(embeddedFileDirectory) - 2):
                        generatedPaths += embeddedFileDirectory[path] + "/"

                    # Create the new sub directories
                    makedirs(join(fullOutputDirectoryBasePath, generatedPaths), exist_ok=True)

                    # Create the new output file
                    open(join(fullOutputDirectoryBasePath, generatedPaths, (embeddedFileDirectory[-2] + "." + embeddedFileDirectory[-1])), "x").close()

                    # Open the input file as Read-Only
                    with open(join(fullInputDirectoryBasePath, foundInputFile), "r") as readOnlyFile:
                        # Open the output file as Write-Only
                        with open(join(fullOutputDirectoryBasePath, generatedPaths, (embeddedFileDirectory[-2] + "." + embeddedFileDirectory[-1])), "w") as writeOnlyFile:
                            # Iterate through each line
                            for line in readOnlyFile.readlines():
                                # Write the new formatted line
                                writeOnlyFile.write(self._returnFormattedLine(line))

                            # Close the writeOnly file handle
                            writeOnlyFile.close()

                        # Close the readOnly file handle
                        readOnlyFile.close()

                elif (foundInputFile.startswith(".") == True or foundInputDirectory in self.EXCLUDE_FROM_EMBEDDED_DIRECTORY_CREATION):
                    # Create the new output directory
                    makedirs(fullOutputDirectoryBasePath, exist_ok=True)

                    # Create the new output file
                    open(join(fullOutputDirectoryBasePath, foundInputFile), "x").close()

                    # Open the input file as Read-Only
                    with open(join(fullInputDirectoryBasePath, foundInputFile), "r") as readOnlyFile:
                        # Open the output file as Write-Only
                        with open(join(fullOutputDirectoryBasePath, foundInputFile), "w") as writeOnlyFile:
                            # Iterate through each line
                            for line in readOnlyFile.readlines():
                                # Write the new formatted line
                                writeOnlyFile.write(self._returnFormattedLine(line))

                            # Close the writeOnly file handle
                            writeOnlyFile.close()

                        # Close the readOnly file handle
                        readOnlyFile.close()

    # Private Static Methods

    # Private Inherited Methods
    def _returnFormattedLine(self, input: str) -> str:
        """
        Returns a formatted line string.

        @param input - The input line
        @return str - A formatted line
        """

        # Declare out string
        out: str = input

        # Iterate through the dictionary keys
        for key in self.TEMPLATE_DICTIONARY.keys():
            # Check if the key is in the input string
            if key in input:
                # Replace the key with the dictionary value
                out = out.replace(key, self.TEMPLATE_DICTIONARY[key])

        # Return new formatted string
        return out


# Run
CI().runCI()
