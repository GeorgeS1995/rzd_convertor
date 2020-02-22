

class ConvertErr(Exception):
    def __init__(self, err):
        self.err_output = err

    def __str__(self):
        return f"Can't convert file: {self.err_output}"