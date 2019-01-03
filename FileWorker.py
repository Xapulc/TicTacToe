import pickle


def save_dict_to_file(dic):
    with open("games.txt", "wb") as file:
        pickle.dump(dic, file)


def load_dict_from_file():
    with open("games.txt", "rb") as file:
        return pickle.load(file)

