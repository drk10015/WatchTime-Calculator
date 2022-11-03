import pickle
dict = []
def loadAll(name):
    with open(name, 'rb') as file:
        while True:
            try:
                dict.append(pickle.load(file))
            except EOFError:
                break
    return dict