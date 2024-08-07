class Ai12zQueryResponse:
    def __init__(self):
        self.docs = []
        self.error = False
        self.times = {}

    def isError(self):
        return self.error

    def setError(self, error):
        self.error = error

    def getTimes(self):
        return self.times

    def setTimes(self, times):
        self.times = times

    def getDocs(self):
        return self.docs

    def setDocs(self, docs):
        self.docs = docs