import os
from Import_Object import Import_Object
from Logger import Logger
from Local_String_Utils import Local_String_Utils
from Import_Object_Factory import Import_Object_Factory

class Import_Logic:
    def __init__(self, logger: Logger):
        self.lsu: Local_String_Utils = Local_String_Utils()
        self.import_object_factory: Import_Object_Factory = Import_Object_Factory()
        self.LOGGER: Logger = logger
        self._cache: dict = {}
        self._external_imports = {}

    def get_and_cache_imports(self, in_file_name: str, out_file_name: str) -> None:
        self._cache_imports(in_file_name)
        self._improve_cache()
        self._get_and_write_imports(in_file_name, out_file_name)

    def _cache_imports(self, in_file_name: str) -> None:
        imp_obj: Import_Object = self.import_object_factory.create_import_object(self.LOGGER, in_file_name)
        for file in imp_obj.imports:
            if file in self._cache:
                self._cache[file].extend(imp_obj.imports[file])
                self._cache[file] = list(set(self._cache[file]))
            else:
                self._cache[file] = list(set(imp_obj.imports[file]))
            self.LOGGER.info(f"{imp_obj.imports[file]} from {file} added to Cache.")
            self._cache_imports(file)
        for external_imp in imp_obj.external_imports:
            if external_imp in self._external_imports:
                self._external_imports[external_imp].extend(imp_obj.external_imports[external_imp])
                self._external_imports[external_imp] = list(set(self._external_imports[external_imp]))
            else:
                self._external_imports[external_imp] = list(set(imp_obj.external_imports[external_imp]))
            self.LOGGER.info(f"{external_imp} added to Cache.")
    
    def _improve_cache(self) -> None:
        self.LOGGER.info(f"Started Cache improvement")
        for file in self._cache:
            if any(["f*" == e[0] for e in self._cache[file]]):
                self._cache[file] = [("f*", False)]
            elif any(['*' == e[0] for e in self._cache[file]]):
                self._cache[file] = [('*', False)]
        self.LOGGER.info(f"Cache improvement successful")
    
    def _get_and_write_imports(self, in_file_name: str, out_file_name: str) -> None:
        _temp_lines = self._get_everything_from_file(in_file_name)
        if _temp_lines:
            self._append_on_top_of_file(out_file_name, _temp_lines, f"----- {in_file_name} -----")
        for file_name in self._cache:
            for obj in self._cache[file_name]:
                _temp_lines = []
                if obj[0].isupper() and not '*' in obj[0]:
                    _temp_lines = self._get_constant(file_name, obj[0])
                elif not '*' in obj[0]:
                    _temp_lines = self._get_function_or_class(file_name, obj[0])
                else:
                    _temp_lines = self._get_everything_from_file(file_name)
                if _temp_lines:
                    self._append_on_top_of_file(out_file_name, _temp_lines, f"----- {file_name} -----")
            self.LOGGER.info(f"Started Cache improvement")
        _temp_lines = []
        for e in self._external_imports:
            if "f*" in self._external_imports[e][0]:
                _temp_lines.append(f"from {e} import *")
            elif '*' in self._external_imports[e][0]:
                _temp_lines.append(f"import {e}")
            else:
                _temp_lines.append(f"from {e} import {','.join([e_i[0] for e_i in self._external_imports[e]])}")
        if not _temp_lines:
            return
        if _temp_lines:
            self._append_on_top_of_file(out_file_name, _temp_lines, "----- General Imports -----")

    def _get_constant(self, file_name: str, name: str) -> list[str]:
        _temp_lines = []
        with open(file_name, 'r') as f:
            _constant_is_closed = False
            for line in f:
                if name in line and '=' in line:
                    _temp_lines.append(line)
                    if self.lsu.is_variable_assignment_closed(line):
                        _constant_is_closed = True
                elif _constant_is_closed:
                    if line.startswith('.'):
                        _temp_lines.append(line)
                    elif line:
                        break
        return _temp_lines

    def _get_function_or_class(self, file_name: str, name: str) -> list[str]:
        _temp_lines = []
        with open(file_name, 'r') as f:
            _function_is_found = False
            depth = 0
            for line in f:
                if (("def" in line) or ("class" in line)) and name in line and not _function_is_found:
                    depth = len(line) - len(line.lstrip())
                    _function_is_found = True
                    _temp_lines.append(line)
                elif _function_is_found:
                    if len(line) - len(line.lstrip()) <= depth:
                        break
                    if line.strip():
                        _temp_lines.append(line)
        return _temp_lines

    def _get_everything_from_file(self, file_name: str) -> list[str]:
        _temp_lines = []
        with open(file_name, 'r') as f:
            _temp_lines = f.readlines()
        _temp_lines = list(filter(lambda x: not(x.startswith("import") or x.startswith("from")) and x.strip(), _temp_lines))
        return _temp_lines

    def _append_on_top_of_file(self, file_name: str, text_to_append: str, section_title: str):
        _old_lines = []
        with open(file_name, 'r') as f_r:
            _old_lines = f_r.readlines()
        with open(file_name, 'w') as f_w:
            f_w.write(f"# {section_title}\n")
            f_w.writelines(text_to_append)
            if _old_lines:
                f_w.write("\n\n")
                f_w.writelines(_old_lines)