import os
from Local_String_Utils import Local_String_Utils

class Import_Logic:
    def __init__(self):
        self.lsu = Local_String_Utils()

    def read_imports_from_file(self, file_name:str) -> list[str, list[str], list[str]]:
        imports = []
        file = ""
        imp = []
        rename = []
        with open(f"{file_name}") as f:
            for line in f:
                if line.startswith("import"):
                    temp_imp = line.split(' ')[1].split('.')[-2].strip()
                    file = f"{file_name.split('/')[:-2]}/{'/'.join(line.split(' ')[1].split('.')[:-2])}.py"
                    rename = line.split('as')[1].strip() if 'as' in line else temp_imp
                    imports.append((file, imp, rename))
                elif line.startswith("from"):
                    file = line.split(' ')[1].strip()
                    temp_imp = line.split('import')[1].strip()
                    if 'as' in temp_imp:
                        rename = temp_imp.split('as')[1]
                        if ',' in rename:
                            rename = rename.split(',')
                        temp_imp = temp_imp.split('as')[0]
                    if ',' in temp_imp:
                        imp = temp_imp.split(',')
                    l_rename = len(rename)
                    for i in range(len(imp) - l_rename):
                        rename.append(imp[l_rename + i])
                    for i in range(len(imp)):
                        imp[i] = imp[i].strip()
                        rename[i] = rename[i].strip()
                    imports.append((file, imp, rename))
                elif line and not line.strip().startswith('#'):
                    return imports
        return imports

    def read_imported_funcs_from_file(self, imports) -> list[str]:
        for imp in imports:
            file = imp[0]
            objs = imp[1]
            renames = imp[2]
            temp_lines = []
            if not os.path.exists(file):
                import_target = file.split('/')[-1].replace('.py', '')
                import_string = f"from {import_target} import {', '.join(objs)} as {', '.join(renames)}"
                return import_string
            with open(file, "r") as f:
                for obj in objs:
                    if obj.isupper():
                        temp_lines.append(self.get_constant(f.readlines(), obj))
                    else:
                        temp_lines.append(self.get_function_or_class(f.readlines(), obj))
            return temp_lines

    def get_function_or_class(self, lines, name) -> list[str]:
        depth = 0
        function_or_class_is_found = False
        function_or_class = []
        for line in lines:
            if not function_or_class_is_found and ('def' in line or 'class' in line) and name in line:
                depth = len(line) - len(line.lstrip())
                function_or_class.append(line)
            if function_or_class_is_found:
                if len(line) - len(line.lstrip()) < depth:
                    if len(function_or_class) > 0:
                        function_or_class.append('\n')
                    return function_or_class
                if line:
                    function_or_class.append(line)
        if len(function_or_class) > 0:
            function_or_class.append('\n')
        return function_or_class

    def get_constant(self, lines: list[str], name: str) -> list[str]:
        constant_is_found = False
        constant = []
        is_closed = False
        opening_and_closing_sum = 0
        start_and_end_sum = 0
        for line in lines:
            if not constant_is_found and name in line and '=' in line:
                constant_is_found = True
            if constant_is_found:
                constant.append(line)
                temp_multiline, temp_opening_and_closing = self.lsu.keep_track_of_openings_and_closings(line)
                if not is_closed:
                    start_and_end_sum += sum([i % 2] for i in temp_multiline)
                    opening_and_closing_sum += sum([i[0] - i[1]] for e in temp_opening_and_closing for i in temp_opening_and_closing[e])
                    is_closed = start_and_end_sum == 0 and opening_and_closing_sum == 0
                constant_is_found = not is_closed
            if not constant_is_found and is_closed:
                if line.startswith('.'):
                    constant.append(line)
                else:
                    break
        return constant