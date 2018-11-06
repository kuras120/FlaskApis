

class Counter:
    __instance = None

    @staticmethod
    def get_instance():
        if Counter.__instance is None:
            Counter()
        return Counter.__instance

    def __init__(self):
        if Counter.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            '''INIT LIST'''
            self.__likes = 2500

            Counter.__instance = self

    def add_like(self):
        self.__likes += 1

    def get_likes(self):
        return self.__likes
