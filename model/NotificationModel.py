import json


class Notification:

    id = None
    error = None

    def __init__(self, id, error):
        self.id_error = id
        self.error = error

    def Message(self):
        return json.dumps(self.__dict__)
