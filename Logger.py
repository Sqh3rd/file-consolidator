from datetime import datetime
from Color import Color

class Logger:
    def __init__(self, name):
        self.style_end = Color.END
        self.name = name
    
    def warn(self, text: str):
        self._output_string("WARN", text, Color.YELLOW)

    def error(self, text: str, exception: Exception):
        self._output_string("ERROR", text, Color.BRIGHT_RED, Color.RED)
        raise exception
    
    def _output_string(self, prefix: str, text: str, prefix_color: Color, text_color: Color = Color.END):
        _date = datetime.now().strftime("%y.%m.%d %H:%M:%S")
        print(f"{Color.BRIGHT_BLUE.value}{self.name} at {_date} | " +
        f"{Color.END.value} {prefix_color.value}[{prefix}]{self.style_end.value}: " +
        f"{text_color.value}{text}{self.style_end.value}")
