class Ai12zError:
    def __init__(self):
        self.message = ""
        self.code = 0
    
    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message = message

    def getCode(self):
        return self.code

    def setCode(self, code):
        self.code = code