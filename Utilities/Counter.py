

class Counter:
    def __init__(self, init_value=0):
        self.__data_to_count = init_value

    def add_like(self):
        self.__data_to_count += 1

    def get_likes(self):
        return self.__data_to_count
