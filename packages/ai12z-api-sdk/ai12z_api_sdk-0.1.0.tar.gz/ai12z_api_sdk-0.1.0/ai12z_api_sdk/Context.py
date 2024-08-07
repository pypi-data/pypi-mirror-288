
class AskAiContext:
    def __init__(self):
        self.metadata = None
        self.page_content = ""

    def getMetadata(self):
        return self.metadata

    def setMetadata(self, metadata):
        self.metadata = metadata

    def getPage_content(self):
        return self.page_content

    def setPage_content(self, page_content):
        self.page_content = page_content