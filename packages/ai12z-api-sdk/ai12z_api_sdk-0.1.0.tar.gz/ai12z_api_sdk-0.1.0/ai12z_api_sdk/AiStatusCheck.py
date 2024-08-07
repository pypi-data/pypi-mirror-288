import datetime
class StatusCheck:
    def __init__(self):
        self.status = ""
        self.date = None
        self.my_server_id = ""
        self.server_time = ""
        self.inProgress = []
        self.failed = []

    def getInProgress(self):
        return self.inProgress

    def setInProgress(self, inProgress):
        self.inProgress = inProgress

    def getFailed(self):
        return self.failed

    def setFailed(self, failed):
        self.failed = failed

    def getMy_server_id(self):
        return self.my_server_id

    def setMy_server_id(self, my_server_id):
        self.my_server_id = my_server_id

    def getServer_time(self):
        return self.server_time

    def setServer_time(self, server_time):
        self.server_time = server_time

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getDate(self):
        return self.date

    def setDate(self, date):
        self.date = date

    def setDate(self, date):
        self.date = datetime.datetime.now()
        try:
            self.date = datetime.datetime.strptime(date, "%Y-%m-%d - %I:%M %p")
        except ValueError as e:
            print(e)
