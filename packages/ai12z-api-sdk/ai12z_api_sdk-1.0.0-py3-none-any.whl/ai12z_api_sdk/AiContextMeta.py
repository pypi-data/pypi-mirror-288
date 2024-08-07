class ContextMeta:
    def __init__(self):
        self.asset_type = ""
        self.created_at = 0
        self.description = ""
        self.lang = ""
        self.name = ""
        self.relevance_score = 0.0
        self.title = ""
        self.url = ""
        self.wordCount = 0

    def getAsset_type(self):
        return self.asset_type

    def setAsset_type(self, asset_type):
        self.asset_type = asset_type

    def getCreated_at(self):
        return self.created_at

    def setCreated_at(self, created_at):
        self.created_at = created_at

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def getLang(self):
        return self.lang

    def setLang(self, lang):
        self.lang = lang

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getRelevance_score(self):
        return self.relevance_score

    def setRelevance_score(self, relevance_score):
        self.relevance_score = relevance_score

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getUrl(self):
        return self.url

    def setUrl(self, url):
        self.url = url

    def getWordCount(self):
        return self.wordCount

    def setWordCount(self, wordCount):
        self.wordCount = wordCount