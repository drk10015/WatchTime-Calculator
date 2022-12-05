import pickle
def loadAll(name):
    with open(name, 'rb') as file:
        return pickle.load(file)