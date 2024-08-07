class Ai12zENV:
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value