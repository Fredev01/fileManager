import os
import shutil
class FileManager:
    def __init__(self, path: str):
        self.path = path
        self.list_files: list = list()
        self.list_dirs: list = list()
        self.file_extensions: set = set()

    def exists(self):
        return os.path.exists(self.path)

    def is_file(self):
        return os.path.isfile(self.path)

    def is_dir(self):
        return os.path.isdir(self.path)

    def move_file(self, old_name: str, new_name: str):
        if os.path.exists(os.path.join(self.path, old_name)):
            if not os.path.exists(os.path.join(self.path, new_name)):
                shutil.move(os.path.join(self.path, old_name), os.path.join(self.path, new_name))

    def create_dir(self, name: str):
        if not os.path.exists(os.path.join(self.path, name)):
            os.mkdir(os.path.join(self.path, name))

    def create_dirs(self, names: set):
        for name in names:
            self.create_dir(name)

    def init(self) -> tuple[bool, str]:
        if not self.exists():
            return False, 'path not found'
        if not self.is_dir():
            return False, 'path is not a directory'
        self.list_files = self.get_files()
        self.file_extensions = self.get_extensions()

        return True, 'finished'


    def get_files(self) -> list:
        list_files: list = list()
        files = os.listdir(self.path)
        for file in files:
            if os.path.isfile(os.path.join(self.path, file)):
                list_files.append(file)
        return list_files

    def get_extensions(self) -> set:
        file_extensions: set = set()
        if not self.list_files:
            return file_extensions
        for file in self.list_files:
            file_extensions.add(file.split('.')[-1])
        return file_extensions


    def get_dirs(self):
        pass
    def read(self):
        pass

    def write(self):
        pass


class OrganizedFileInDirectory(FileManager):
    def __init__(self, path: str):
        super().__init__(path)
        self.new_dirs: set = set()
        self._names_file_extension: NameFileExtension = NameFileExtension()
        self._files_organized: dict = dict()

    def organize(self) -> tuple[bool, str]:
        is_success, message = self.init()
        if not is_success:
            return False, message
        self.new_dirs = self.get_new_dirs(self.file_extensions)
        if not len(self.list_files) >= 1:
            return False, 'no files found'
        for file in self.list_files:
            file_extension = file.split('.')[-1]
            name_dir = self._add_prefix_based_on_extension('files', file_extension)
            self._files_organized[name_dir].append(file)

        self.create_dirs(self.new_dirs)
        for name_dir, files in self._files_organized.items():
            for file in files:
                # test =  f'{file}, {str(os.path.join(name_dir, file))}'
                # print(test)
                self.move_file(file, str(os.path.join(name_dir, file)))

        return True, 'executed successfully'

    def get_new_dirs(self, file_extensions: set) -> set:
        new_dirs: set = set()
        # new_dirs: list = [ self._names_file_extension.get_name_file_extension(file_extension) for file_extension in file_extensions]
        for file_extension in file_extensions:
            name_dir: str = self._add_prefix_based_on_extension('files', file_extension)
            new_dirs.add(name_dir)
        for new_dir in new_dirs:
            self._files_organized[new_dir] = list()
        return new_dirs

    def _add_prefix_based_on_extension(self, prefix: str, file_extension: str):
        return 'images' if self._names_file_extension.get_name_file_extension(file_extension) == 'image' \
            else f'{prefix}_{self._names_file_extension.get_name_file_extension(file_extension)}'

class NameFileExtension:
    name_file_extension: dict = {'py': 'python',
                                 'c': 'c',
                                 'cpp': 'c++',
                                 'js': 'javascript',
                                 'html': 'html',
                                 'css': 'css',
                                 'json': 'json',
                                 'txt': 'text',
                                 'md': 'markdown',
                                 'java': 'java',
                                 'go': 'go',
                                 'sh': 'shell',
                                 'doc': 'word',
                                 'docx': 'word',
                                 'xls': 'excel',
                                 'xlsx': 'excel',
                                 'ppt': 'powerpoint',
                                 'pptx': 'powerpoint',
                                 'pdf': 'pdf',
                                 'zip': 'zip',
                                 'rar': 'zip',
                                 'tar': 'zip',
                                 'gz': 'zip',
                                 '7z': 'zip',
                                 'iso': 'zip',
                                 'jpg': 'image',
                                 'jpeg': 'image',
                                 'png': 'image',
                                 'gif': 'image',
                                 'svg': 'image',
                                 }
    def __init__(self):
        pass
    def get_name_file_extension(self, file_extension: str):
        return self.name_file_extension.get(file_extension, 'other')



if __name__ == '__main__':
    test = OrganizedFileInDirectory('/home/angel/Downloads')
    is_success, message = test.organize()
    print(is_success, message)