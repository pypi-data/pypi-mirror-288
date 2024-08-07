from ai12z_api_sdk.AiENV import Ai12zENV
class Config:
    ENV = Ai12zENV.PROD
    ACCESS_TOKEN = ""
    apiEndPoint = "https://dev-api.ai12z.net"
    stageApiEndPoint = apiEndPoint
    devApiEndPoint = apiEndPoint

    @staticmethod
    def getACCESS_TOKEN():
        return Config.ACCESS_TOKEN

    def getDefaultUrl(self):
        if Config.ENV == Ai12zENV.STAGE:
            return Config.stageApiEndPoint
        if Config.ENV == Ai12zENV.DEV:
            return Config.devApiEndPoint
        return Config.apiEndPoint

    def getStageUrl(self):
        return Config.stageApiEndPoint

    def getDevUrl(self):
        return Config.devApiEndPoint

    @staticmethod
    def getENV():
        return Config.ENV