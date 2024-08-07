class AskApiData:
    def __init__(self):
        self.answer = ""
        self.title = ""
        self.link = ""
        self.description = ""
        self.relevance_score = ""
        self.asset_type = ""
        self.did_answer = ""
        self.context = []
        self.insight_id = ""
        self.conversation_id = ""
        self.completion_answer = ""
        self.error = ""

    def getError(self):
        return self.error

    def setError(self, error):
        self.error = error

    def getAnswer(self):
        return self.answer

    def setAnswer(self, answer):
        self.answer = answer

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getLink(self):
        return self.link

    def setLink(self, link):
        self.link = link

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def getRelevance_score(self):
        return self.relevance_score

    def setRelevance_score(self, relevance_score):
        self.relevance_score = relevance_score

    def getAsset_type(self):
        return self.asset_type

    def setAsset_type(self, asset_type):
        self.asset_type = asset_type

    def getDid_answer(self):
        return self.did_answer

    def setDid_answer(self, did_answer):
        self.did_answer = did_answer

    def getContext(self):
        return self.context

    def setContext(self, context):
        self.context = context

    def getInsight_id(self):
        return self.insight_id

    def setInsight_id(self, insight_id):
        self.insight_id = insight_id

    def getConversation_id(self):
        return self.conversation_id

    def setConversation_id(self, conversation_id):
        self.conversation_id = conversation_id

    def getCompletion_answer(self):
        return self.completion_answer

    def setCompletion_answer(self, completion_answer):
        self.completion_answer = completion_answer
