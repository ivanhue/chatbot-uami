from .tfidf import TFIDF
import pandas as pd 
import numpy as np
import pickle

data_path = "actions/tfidf/textos_2023_08_0111_50_30.json"
model_path = "actions/tfidf/model_2023_08_0111_50_30_5.pickle"

df = pd.read_json(data_path)
corpus = np.array(df["document"])
metadatas = np.array(df["metadata"])
urls = df["metadata"].apply(lambda x: x.get("url"))
keywords = df["metadata"].apply(lambda x: x.get("keywords"))

class MyCustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "actions.tfidf"
        return super().find_class(module, name)


with open(model_path, 'rb') as file:  # open a text file
    unpicker = MyCustomUnpickler(file)
    model:TFIDF = unpicker.load() # serialize the list

vocabulary = model.get_vocabulary()