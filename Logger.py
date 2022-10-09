from datetime import datetime
from Color import Color
from Error_Object import Error_Object
from Log_Mode import Log_Mode
from Output import Output

class Logger:
    def __init__(self, name: str, out: Output, log_mode: Log_Mode):
        self.style_end = Color.END
        self.name = name
        self.out = out
        self.log_mode = log_mode

    def new_line(self):
        if self.log_mode.value >= 1:
            self.output("\n")

    def variable(self, var_name, var):
        if self.log_mode.value >= 2:
            self._output_string("VAR", f"Name: {var_name} Type: {type(var)} Value: {var}", Color.BOLD_GREEN)

    def info(self, text: str):
        if self.log_mode.value >= 1:
            self._output_string("INFO", text, Color.BOLD_BRIGHT_CYAN)

    def warn(self, text: str):
        if self.log_mode.value >= 1:
            self._output_string("WARN", text, Color.BOLD_BRIGHT_YELLOW)

    def error(self, error_object: Error_Object):
        self._output_string("ERROR", error_object.text, Color.BOLD_RED, Color.RED)
        raise error_object.exception

    def _output_string(self, prefix: str, text: str, prefix_color: Color, text_color: Color = Color.END):
        _spaces_before_data = ' ' * 5
        _date = datetime.now().strftime("%y.%m.%d %H:%M:%S")
        self.output(f"{Color.BRIGHT_BLUE.value}{self.name} at {_date} |" +
        f"{Color.END.value}{_spaces_before_data}{prefix_color.value}[{prefix}]{self.style_end.value}: " +
        f"{text_color.value}{text}{self.style_end.value}")

    def output(self, text: str):
        if self.out == Output.STDOUT:
            print(text)