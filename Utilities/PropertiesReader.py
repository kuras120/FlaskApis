import os
from enum import Enum


class Method(Enum):
    Automatic = 0
    Manual_dictionary = 1
    Manual_properties = 2


class PropertiesReader:
    def __init__(self, file):
        self.__file = file
        self.__dict_properties = {}

    def read(self, key, method=Method.Automatic):
        if method == Method.Automatic:
            if key in self.__dict_properties:
                return self.__dict_properties[key]
            else:
                return self.__read_from_source(key)

        elif method == Method.Manual_dictionary:
            if key in self.__dict_properties:
                return self.__dict_properties[key]
            else:
                raise Exception("Data with specific key doesn't exist")

        elif method == Method.Manual_properties:
            return self.__read_from_source(key)

    def __read_from_source(self, key):
        found = False
        properties = open(self.__file)
        for line in properties:
            if "key" in line:
                temp = line.strip().split("=")
                print(temp)
                if temp[1] == key:
                    found = True
                    print("key was found")
                    break
        if found:
            return self.__read_key_source(key, properties)
        else:
            raise Exception("Questionnaire data cannot be found")

    def __read_key_source(self, key, properties):
        new_dict = []
        question, answers = [], []
        for line in properties:
            if "key" in line:
                break
            elif "title" in line:
                # if question is not empty
                if question:
                    question.append(answers)
                    new_dict.append(question)
                    question, answers = [], []
                temp = line.strip().split("=")
                question.append(temp[1])
            elif "answer" in line:
                temp = line.strip().split("=")
                answers.append(temp[1])

        question.append(answers)
        new_dict.append(question)
        self.__dict_properties[key] = new_dict
        return new_dict


if __name__ == "__main__":
    reader = PropertiesReader("feedback_index.properties")
    print(reader.read("key1"))


