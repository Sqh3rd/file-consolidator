import os

from Logger import Logger

class Import_Object:
    def __init__(self, logger: Logger, file_name: str):
        self.LOGGER = logger
        self._files = []
        self._imports = []
        self._renamings = []
        self._current_file = file_name
        self.external_imports = {}
        with open(file_name, 'r') as f:
            for line in f:
                if "import" in line and not '#' in line:
                    if "as" in line:
                        self.LOGGER.error("No keyword \"as\" after import statement allowed!", SyntaxError)
                    if self._get_external_imports(line):
                        continue
                    self._files.extend(self._get_modules_from_import(line))
                    self._imports.extend(self._get_objects_from_import(line))
                    self._renamings.extend(self._get_renamings_from_import(line))
                elif line.strip() and not line.strip().startswith('#'):
                    break
        self.imports = {}
        for i in range(len(self._files)):
            _temp_imports = self._imports[i]
            _temp_renamings = [] if not i < len(self._renamings) else self._renamings[i]
            _temp_renamings.extend([False] * (len(_temp_imports) - len(_temp_renamings)))
            _temp_file = f"{'/'.join(file_name.split('/')[:-1])}/{self._files[i]}.py"
            self.imports[_temp_file] = [(_temp_imports[j], _temp_renamings[j]) for j in range(len(_temp_imports))]

    def _get_external_imports(self, import_str: str) -> None:
        if "from" in import_str:
            _potential_file_name = import_str.split("from")[1].split("import")[0].strip()
            if not self._is_import_file(_potential_file_name):
                self.external_imports[_potential_file_name] = self._get_objects_from_import(import_str)
                return True
        elif "import" in import_str:
            _potential_file_names = [import_str.split("import")[1]] if not ',' in import_str else import_str.split("import")[1].split(',')
            _potential_file_names = [x if not "as" in x else x.split("as") for x in _potential_file_names]
            _external_import_exists = False
            for pfn in _potential_file_names:
                if not self._is_import_file(pfn):
                    _external_import_exists = True
                    self.external_imports[pfn.strip()] = [('*', False)]
            return _external_import_exists
        return False

    def _get_modules_from_import(self, import_str: str) -> list[str]:
        _files: list = []
        import_str = import_str if not "as" in import_str else import_str.split("as")[0]
        if import_str.startswith("import"):
            self.LOGGER.warn("Importing entire modules is inefficient in this application!")
            _files = import_str.split("import")[1]
            if ',' in _files:
                _files = _files.split(',')
        elif import_str.startswith("from"):
            _potential_file = import_str.split("from")[1].split("import")[0]
            if self._is_import_file(_potential_file):
                _files = [_potential_file]
            else:
                self.LOGGER.warn("Importing entire modules is inefficient in this application!")
                _files = [import_str.split("import")[1]] if not ',' in import_str else import_str.split(',')
        _files = list(map(lambda x: x.strip(), _files))
        return _files
    
    def _get_objects_from_import(self, import_str: str) -> list[list[str]]:
        imports = []
        import_str = import_str if not "as" in import_str else import_str.split("as")[0]
        if import_str.startswith("import"):
            temp = import_str.split("import")[1]
            imports = [['*']] * (temp.count(',') + 1)
        elif import_str.startswith("from"):
            temp = import_str.split("import")[1]
            _potential_file = import_str.split("from")[1].split("import")[0]
            if self._is_import_file(_potential_file):
                imports = [[temp]] if not ',' in temp else [temp.split(',')]
            else:
                imports = [["f*"]] * (temp.count(',') + 1)
        imports = [list(map(lambda x: x.strip(), i)) for i in imports]
        return imports

    def _get_renamings_from_import(self, import_str: str) -> list[str]:
        if import_str.startswith("import"):
            if not "as" in import_str:
                return [[False]] * (import_str.split("import")[1].count(',') + 1)
        elif import_str.startswith("from"):
            if not "as" in import_str:
                return [[False]]
        else:
            return []
        temp = import_str.split("as")[1]
        renamings = [[temp]] if not ',' in temp else [temp.split(',')]
        renamings = [list(map(lambda x: x.strip(), r)) for r in renamings]
        return renamings

    def _is_import_file(self, file_name: str) -> bool:
        return os.path.exists(f"{'/'.join(self._current_file.split('/')[:-1])}/{file_name.strip()}.py")