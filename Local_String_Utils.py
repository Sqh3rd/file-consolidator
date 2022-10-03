from Local_Dict_Utils import Local_Dict_Utils

class Local_String_Utils:
    def __init__(self):
        self.dict_utils = Local_Dict_Utils()
        self.OPENING_CHARACTERS = ['(', '[', '{']
        self.CLOSING_CHARACTERS = [')', ']', '}']
        self.CORRESPONDING_OPENING_CHARACTERS = {self.CLOSING_CHARACTERS[i]: self.OPENING_CHARACTERS[i] for i in range(len(self.OPENING_CHARACTERS))}
        self.MULTILINE_CHARACTERS = ["\'\'\'", "\"\"\""]
    
    def keep_track_of_openings_and_closings(self, line) -> dict[str, int]:
        tracking_dict = {}
        if '=' in line:
            exp_str = line.split('=')[1].strip()
        else:
            exp_str = line
        # Check for opening characters
        for c in self.OPENING_CHARACTERS:
            if c == exp_str[0]:
                self.dict_utils.increase_counter(tracking_dict, c)
        # Check for beginning multiline characters
        for c in self.MULTILINE_CHARACTERS:
            if c == exp_str[:3]:
                self.dict_utils.increase_counter(tracking_dict, c)
        # Check for ending multiline characters
        for c in self.MULTILINE_CHARACTERS:
            if not c in exp_str or not c in tracking_dict:
                continue
            if c in exp_str[-3:]:
                self.dict_utils.increase_counter(tracking_dict, c)
            elif exp_str.split(c)[-1][0] == '.':
                self.dict_utils.increase_counter(tracking_dict, c)
        # Check for closing characters
        for c in self.CLOSING_CHARACTERS:
            if not c in exp_str and  not self.CORRESPONDING_OPENING_CHARACTERS[c] in tracking_dict:
                continue
            if '.' in exp_str and exp_str.split('.')[1]
            if c == exp_str[-1]:
                self.dict_utils.increase_counter(tracking_dict, c)
            
        return tracking_dict

if __name__ == "__main__":
    lsu = Local_String_Utils()
    line = ""
    print(lsu.keep_track_of_openings_and_closings(line))