import os


class FileRead:

    def __init__(self, path, file_name):
        self.xml = ''
        file = os.path.normpath(os.path.join(path, file_name))
        # todo: sync to thread pool
        with open(file, mode='r', encoding='utf-8') as f:
            self.xml = f.read()

    @property
    def content(self):
        return self.xml
