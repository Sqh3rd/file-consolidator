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
        self._external_imports: dict = {}

    def get_and_cache_imports(self, in_file_name: str, out_file_name: str) -> None:
        file_order_list = []
        self._cache_imports(in_file_name, file_order_list)
        self._improve_imports()
        self._get_and_write_imports(out_file_name, file_order_list)

    def _cache_imports(self, in_file_name: str, file_list: list[str]) -> None:
        imp_obj: Import_Object = self.import_object_factory.create_import_object(self.LOGGER, in_file_name)
        for file in imp_obj.imports:
            self.LOGGER.variable("file", file)
            self.LOGGER.variable(f"imp_obj.imports{file}", imp_obj.imports[file])
            if file in self._cache:
                self._cache[file].extend(imp_obj.imports[file])
                self._cache[file] = list(set(self._cache[file]))
            else:
                self._cache[file] = list(set(imp_obj.imports[file]))
            _object_list_str = ', '.join(imp_obj.imports[file])
            self.LOGGER.info(f"{_object_list_str} from {file} added to Cache.")
            self._cache_imports(file, file_list)
        for external_imp in imp_obj.external_imports:
            self.LOGGER.variable("external_imp", external_imp)
            self.LOGGER.variable(f"external_imports{external_imp}", imp_obj.external_imports[external_imp])
            if external_imp in self._external_imports:
                self._external_imports[external_imp].extend(imp_obj.external_imports[external_imp])
                self._external_imports[external_imp] = list(set(self._external_imports[external_imp]))
            else:
                self._external_imports[external_imp] = list(set(imp_obj.external_imports[external_imp]))
            self.LOGGER.info(f"{external_imp} added to Cache.")
        if not in_file_name in file_list:
            file_list.append(in_file_name)
    
    def _improve_imports(self) -> None:
        self.LOGGER.info(f"Started Cache improvement")
        for imp in self._external_imports:
            if any(["f*" == e[0] for e in self._external_imports[imp]]):
                self._external_imports[imp] = ["f*"]
            elif any(['*' == e[0] for e in self._external_imports[imp]]):
                self._external_imports[imp] = ['*']
        self.LOGGER.info(f"Cache improvement successful")
    
    def _get_and_write_imports(self, out_file_name: str, file_order_list: list[str]) -> None:
        # Append general imports
        _temp_lines: list[str] = []
        for e in self._external_imports:
            self.LOGGER.variable("e", e)
            self.LOGGER.variable(f"_external_imports[{e}]", self._external_imports[e])
            if "f*" in self._external_imports[e]:
                _temp_lines.append(f"from {e} import *\n")
            elif '*' in self._external_imports[e]:
                _temp_lines.append(f"import {e}\n")
            else:
                _temp_lines.append(f"from {e} import {','.join(self._external_imports[e])}\n")
        if _temp_lines:
            self._append_section_to_file(out_file_name, _temp_lines, "----- General Imports -----")

        # Append specific imports
        for file_name in file_order_list:
            if not file_name in self._cache:
                _temp_lines = self._get_everything_from_file(file_name)
                self._append_section_to_file(out_file_name, _temp_lines, f"----- {file_name} -----")
                self.LOGGER.info(f"Appended {file_name} to {out_file_name}")
                continue
            for obj in self._cache[file_name]:
                _temp_lines = []
                _temp_lines = self._get_class_from_file(file_name, obj)
                self._append_section_to_file(out_file_name, _temp_lines, f"----- {file_name} -----")
            obj_str = ", ".join([obj for obj in self._cache[file_name]])
            self.LOGGER.info(f"Appended {obj_str} from {file_name} to {out_file_name}")

    def _get_class_from_file(self, file_name: str, name: str) -> list[str]:
        _temp_lines = []
        with open(file_name, 'r') as f:
            _class_is_found = False
            depth = 0
            for line in f:
                if "class" in line and name in line and not _class_is_found:
                    depth = len(line) - len(line.lstrip())
                    _class_is_found = True
                    _temp_lines.append(line)
                elif _class_is_found:
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

    def _append_section_to_file(self, file_name: str, text_to_append: list[str], section_title: str) -> None:
        section_text = []
        section_text.append(f"# {section_title}\n")
        section_text.extend(text_to_append)
        section_text.append("\n\n")
        self._append_to_file(file_name, section_text)
    
    def _append_to_file(self, file_name: str, text_to_append: list[str]) -> None:
        with open(file_name, 'a') as f:
            f.writelines(text_to_append)