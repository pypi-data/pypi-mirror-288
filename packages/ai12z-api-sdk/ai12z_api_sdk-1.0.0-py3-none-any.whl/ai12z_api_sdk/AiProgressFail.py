import datetime
class ProgressFail:
    def __init__(self):
        self.orgId = ""
        self.projectId = ""
        self.documentId = ""
        self.modifiedAt = None
        self.message = ""
        self.task = ""
        self._id = ""

    def get_id(self):
        return self._id

    def set_id(self, _id):
        self._id = _id

    def getModifiedAt(self):
        return self.modifiedAt

    def setModifiedAt(self, modifiedAt):
        self.modifiedAt = modifiedAt

    def setModifiedAt(self, modifiedAt):
        self.modifiedAt = datetime.datetime.now()

        dateStr = modifiedAt
        inputFormat = "%Y-%m-%d %H:%M:%S.%f"
        outputFormat = "%Y-%m-%dT%H:%M:%S.%fZ"

        try:
            date = datetime.datetime.strptime(dateStr, inputFormat)
            formattedDateStr = date.strftime(outputFormat)

        except ValueError as e:
            print(e)

    def getOrgId(self):
        return self.orgId

    def setOrgId(self, orgId):
        self.orgId = orgId

    def getProjectId(self):
        return self.projectId

    def setProjectId(self, projectId):
        self.projectId = projectId

    def getDocumentId(self):
        return self.documentId

    def setDocumentId(self, documentId):
        self.documentId = documentId

    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message = message

    def getTask(self):
        return self.task

    def setTask(self, task):
        self.task = task