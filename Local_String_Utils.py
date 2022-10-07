from Local_Dict_Utils import Local_Dict_Utils

class Local_String_Utils:
    def __init__(self):
        self.dict_utils = Local_Dict_Utils()
        self.OPENING_CHARACTERS = ['(', '[', '{']
        self.CLOSING_CHARACTERS = [')', ']', '}']
        self.CORRESPONDING_CLOSING_CHARACTERS = {self.OPENING_CHARACTERS[i]: self.CLOSING_CHARACTERS[i] for i in range(len(self.OPENING_CHARACTERS))}
        self.MULTILINE_CHARACTERS = ["\'\'\'", "\"\"\""]
    
    def is_variable_assignment_closed(self, line: str) -> bool:
        _conditions = []
        _temp_tuple = self._keep_track_of_openings_and_closings(line)
        _conditions.extend([True if x % 2 == 0 else False for t in _temp_tuple for y in t for x in t[y]])
        return all(_conditions)

    def _keep_track_of_openings_and_closings(self, line: str) -> tuple[dict[str, int], dict[tuple[str, str], tuple[int, int]]]:
        multiline_tracking_dict = {}
        opening_and_closing_tracking_dict = {(op, self.CORRESPONDING_CLOSING_CHARACTERS[op]):(0,0) for op in self.OPENING_CHARACTERS}
        if '=' in line:
            exp_str = line.split('=')[1].strip()
        else:
            exp_str = line
        # Check for beginning multiline characters
        for c in self.MULTILINE_CHARACTERS:
            if c == exp_str[:3]:
                self.dict_utils.increase_counter(multiline_tracking_dict, c)
        # Check for ending multiline characters
        for c in self.MULTILINE_CHARACTERS:
            if not c in exp_str or not c in multiline_tracking_dict:
                continue
            if c in exp_str[-3:]:
                self.dict_utils.increase_counter(multiline_tracking_dict, c)
            elif exp_str.split(c)[-1][0] == '.':
                self.dict_utils.increase_counter(multiline_tracking_dict, c)
        # Check for opening and closing characters
        for i, k in opening_and_closing_tracking_dict:
            opening_and_closing_tracking_dict[(i, k)] = (exp_str.count(i), exp_str.count(k))
        return (multiline_tracking_dict, opening_and_closing_tracking_dict)

if __name__ == "__main__":
    lsu = Local_String_Utils()
    line = ""
    print(lsu.keep_track_of_openings_and_closings(line))