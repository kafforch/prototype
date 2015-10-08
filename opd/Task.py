class Task():

    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            self.__dict__[key] = value