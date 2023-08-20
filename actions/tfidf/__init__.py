from .tfidf import TFIDF
import pandas as pd 
import numpy as np
import pickle
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


data_path = "actions/tfidf/textos_2023_08_0111_50_30.json"
model_path = "actions/tfidf/model_2023_08_0111_50_30_4.pickle"

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

# # Función para procesar el texto y obtener las palabras clave
# def procesar_palabras_clave(texto):
#     return set(re.findall(r'\b\w+\b', texto.lower()))

# # Función para buscar los documentos más parecidos a una pregunta dada
# def buscar_documentos_similares(keywords, pregunta):
#     # Procesar la pregunta y obtener sus palabras clave
#     palabras_clave_pregunta = procesar_palabras_clave(pregunta)

#     # Inicializar el vectorizador y calcular la matriz de términos
#     vectorizador = CountVectorizer()
#     matriz_terminos = vectorizador.fit_transform(keywords)

#     # Procesar la pregunta y calcular su vector de términos
#     vector_pregunta = vectorizador.transform([" ".join(palabras_clave_pregunta)])

#     # Calcular la similitud entre la pregunta y los documentos
#     similitud = cosine_similarity(vector_pregunta, matriz_terminos)

#     # Ordenar los documentos en función de su similitud con la pregunta
#     documentos_similares = sorted(zip(similitud[0], range(len(keywords))), reverse=True)

#     # Obtener los 3 documentos más parecidos
#     # documentos_mas_parecidos = [json_data[i] for _, i in documentos_similares[:3]]

#     return documentos_similares # documentos_mas_parecidos

# [json_data[i] for _, i in documentos_similares[:3]]