import pickle


def save_dict_to_file(dic, file_name):
    with open(file_name, "wb") as file:
        pickle.dump(dic, file)


def load_dict_from_file(file_name):
    with open(file_name, "rb") as file:
        return pickle.load(file)

