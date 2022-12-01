#start-of-file


class Population:
    def __init__(self):
        self.elements = {}

    def __iter__(self):
        return iter(self.elements.values())

    def __next__(self):
        return next(self)


