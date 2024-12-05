class SingletonStateManager:
    _instance = None
    _state = 0
    _row = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonStateManager, cls).__new__(cls)
        return cls._instance

    def getCurrentState(self):
        return self._state

    def setState(self, value):
        if isinstance(value, int):
            self._state = value
        else:
            raise ValueError("State must be an integer")

    def getRow(self):
        return self._row

    def setRow(self, value):
        if isinstance(value, int):
            self._row = value
        else:
            raise ValueError("Row must be an integer")

    def incrementRow(self):
        self._row += 1
        return self._row


