import pickle

PATH_TO_MODELS = 'models/'
filename = 'model.pkl'

model = PATH_TO_MODELS + filename

def load_model():
    loaded_model = pickle.load(open(model, 'rb'))
    return loaded_model