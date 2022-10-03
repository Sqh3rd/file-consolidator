import os

class Import_Logic:
    def read_imports_from_file(self, file_name:str) -> list[str, list[str], list[str]]:
        imports = []
        file = ""
        imp = []
        rename = []
        with open(f"{file_name}.py") as f:
            for line in f:
                if line.startswith("import"):
                    imp = [line.split(' ')[1].split('.')[-2].strip()]
                    file = f"{file_name.split('/')[:-2]}/{imports[-1].split('.')[-2]}.py"
                    rename = line.split('as')[1].strip() if 'as' in line else imp
                    imports.append((file, imp, rename))
                elif line.startswith("from"):
                    file = line.split(' ')[1].strip()
                    imp = line.split('import')[1].strip()
                    if 'as' in imp:
                        rename = imp.split('as')[1]
                        if ',' in rename:
                            rename = rename.split(',')
                        imp = imp.split('as')[0]
                        if ',' in imp:
                            imp = imp.split(',')
                    l_rename = len(rename)
                    for i in range(l_rename < len(imp)):
                        rename.append(imp[l_rename + i])
                    for i in range(len(imp)):
                        imp[i] = imp[i].strip()
                        rename[i] = rename[i].strip()
                    imports.append((file, imp, rename))
                elif line and not line.strip().startswith('#'):
                    return imports

    def read_imported_funcs_from_file(self, imports) -> list[str]:
        for imp in imports:
            file = imp[0]
            objs = imp[1]
            renames = imp[2]

            depth = 0
            obj_is_found = False
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

    def get_constant(self, lines, name) -> list[str]:
        constant_is_found = False
        constant = []
        is_parenthesis_in_constant = False
        for line in lines:
            if not constant_is_found and name in line and '=' in line:
                constant_is_found = True
                if ['(', '[', '{', '\'\'\'', '\"\"\"'] in line:
                    is_parenthesis_in_constant = True
            if constant_is_found:
                constant.append(line)
                if is_parenthesis_in_constant:
                    if [')', ']', '}'] in line:
                        is_parenthesis_in_constant = False
                        return
                else:
                    return