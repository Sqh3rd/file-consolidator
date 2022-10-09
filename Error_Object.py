class Error_Object:
    def __init__(self, text: str, exception: type[Exception]):
        self.text = text
        self.exception = exception(self.text)