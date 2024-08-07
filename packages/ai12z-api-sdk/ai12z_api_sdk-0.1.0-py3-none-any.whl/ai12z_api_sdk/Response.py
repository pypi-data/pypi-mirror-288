class Ai12zResponse:
    def __init__(self):
        self.response = None
        self.error = None

    def __init__(self, response, error):
        self.response = response
        self.error = error

    def getResponse(self):
        return self.response

    def setResponse(self, response):
        self.response = response

    def getError(self):
        return self.error

    def setError(self, error):
        self.error = error
