from Log_Mode import Log_Mode

class Log_Mode_Parser:
    def parse_str(self, txt: str):
        return Log_Mode[txt.upper()]