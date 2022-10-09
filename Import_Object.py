import os
from Error_Object import Error_Object

from Logger import Logger

class Import_Object:
    def __init__(self, logger: Logger, file_name: str):
        self.LOGGER = logger
        self._files = []
        self._imports = []
        self._renamings = []
        self._current_file = file_name
        self._path = os.path.dirname(self._current_file)
        self.external_imports = {}
        with open(file_name, 'r') as f:
            for line in f:
                if "import" in line and not '#' in line:
                    if " as " in line:
                        error_obj = Error_Object("Renaming of imported classes is not allowed!", SyntaxError)
                        self.LOGGER.error(error_obj)
                    if self._get_external_imports(line):
                        continue
                    self._files.extend(self._get_modules_from_import(line))
                    self._imports.append(self._get_objects_from_import(line))
                elif line.strip() and not line.strip().startswith('#'):
                    break
        self.imports = {}
        for i in range(len(self._files)):
            _temp_file = os.path.join(self._path, f"{self._files[i]}.py").replace("\\", '/')
            self.imports[_temp_file] = self._imports[i]

    def _get_external_imports(self, import_str: str) -> bool:
        if "from" in import_str:
            _potential_file_or_folder_name = import_str.split("from")[1].split("import")[0].strip()
            _potential_file_name = import_str.split("import")[1]
            if ',' in _potential_file_name:
                _potential_file_name = _potential_file_name.split(',')[0]
            if not self._is_import_file(_potential_file_or_folder_name):
                if not self._is_import_file(os.path.join(_potential_file_or_folder_name, _potential_file_name)):
                    self.external_imports[_potential_file_or_folder_name] = self._get_objects_from_import(import_str)
                    return True
        elif "import" in import_str:
            if ',' in import_str:
                _potential_file_names = import_str.split("import")[1].split(',')
            else:
                _potential_file_names = [import_str.split("import")[1]]
            _external_import_exists = False
            for pfn in _potential_file_names:
                if not self._is_import_file(pfn):
                    _external_import_exists = True
                    self.external_imports[pfn.strip()] = ['*']
            return _external_import_exists
        return False

    def _get_modules_from_import(self, import_str: str) -> list[str]:
        _files: list = []
        error_obj = Error_Object("Importing entire modules is not allowed. Import Classes instead!", SyntaxError)
        if import_str.startswith("import"):
            self.LOGGER.error(error_obj)
        elif import_str.startswith("from"):
            _potential_file = import_str.split("from")[1].split("import")[0]
            if self._is_import_file(_potential_file):
                _files = [_potential_file]
            else:
                self.LOGGER.warn("Importing entire modules is inefficient in this application!")
                _files = [import_str.split("import")[1]] if not ',' in import_str else import_str.split(',')
        _files = list(filter(lambda x: self._is_import_file(x), map(lambda x: x.strip(), _files)))
        return _files
    
    def _get_objects_from_import(self, import_str: str) -> list[str]:
        imports = []
        if import_str.startswith("import"):
            temp = import_str.split("import")[1]
            imports = ['*'] * (temp.count(',') + 1)
        elif import_str.startswith("from"):
            temp = import_str.split("import")[1]
            _potential_file = import_str.split("from")[1].split("import")[0]
            if self._is_import_file(_potential_file):
                if ',' in temp:
                    imports = [temp.strip()]
                else:
                    imports = temp.split(',')
            else:
                if ',' in temp:
                    imports = [t.strip() for t in temp.split(',')]
                else:
                    imports = [temp.strip()]
                for i in range(len(imports)):
                    if imports[i] == '*':
                        imports[i] = "f*"
        imports = [x.strip() for x in imports]
        return imports

    def _is_import_file(self, file_name: str) -> bool:
        return os.path.exists(os.path.join(self._path, f"{file_name.strip()}.py"))