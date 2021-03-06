import pickle


def save_dict_to_file(dic, file_name):
    """
    save dic to file with name res/{file_name}
    :param dic:
    :param file_name:
    :return:
    """
    with open("res/" + file_name, "wb") as file:
        pickle.dump(dic, file)


def load_dict_from_file(file_name):
    """
    load dic from file with name res/{file_name} (if can't -> return {})
    :param file_name:
    :return:
    """
    try:
        with open("res/" + file_name, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

