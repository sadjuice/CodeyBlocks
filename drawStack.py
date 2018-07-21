class drawStack():
    def __init__(self):
        self.stack = []

    def addToStack(self, obj):
        self.stack.append(obj)

    def clearStack(self):
        self.stack = []

stackToDraw = drawStack()