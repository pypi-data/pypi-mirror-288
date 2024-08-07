
class Ai12zOptions:
    """ 
    This class is used to set the options for the AI12z API.
    Args:
        apiKey (str): The API key for the AI12z API.
        num_docs (int): The number of documents to return.
        format (str): The format of the response (html or text).
    """   
    def __init__(self, apiKey: str, num_docs: int):
        self.apiKey = apiKey
        self.num_docs = num_docs

    def __init__(self, apiKey: str, format: str):
        self.apiKey = apiKey
        self.format = format    

    def __init__(self):
        self.apiKey = None
        self.num_docs = None
        self.format = None
        self.conversationId = None

    def getApiKey(self) -> str:
        return self.apiKey

    def setApiKey(self, apiKey: str) -> None:
        self.apiKey = apiKey

    def getNum_docs(self) -> int:
        return self.num_docs

    def setNum_docs(self, num_docs: int) -> None:
        self.num_docs = num_docs

    def getFormat(self) -> str:
        return self.format

    def setFormat(self, format: str) -> None:
        self.format = format

    def getConversationId(self) -> str:
        return self.conversationId

    def setConversationId(self, conversationId: str) -> None:
        self.conversationId = conversationId



