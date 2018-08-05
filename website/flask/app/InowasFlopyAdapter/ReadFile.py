import os


class ReadFile:
    _filename = None
    _workspace = None

    def __init__(self, workspace):
        self._workspace = workspace
        pass

    def read_file(self, extension):

        workspace = self._workspace
        for file in os.listdir(self._workspace):
            if file.endswith("." + extension):
                self._filename = os.path.join(self._workspace, file)

        try:
            with open(self._filename) as f:
                return f.read()
        except:
            return ("Error reading file with extension '" + str(extension)) + "' in workspace '" + str(workspace) + "'."

    def read_file_list(self):
        workspace = self._workspace
        try:
            return os.listdir(workspace)
        except:
            return "Error reading files of workspace '" + str(workspace) + "'."
