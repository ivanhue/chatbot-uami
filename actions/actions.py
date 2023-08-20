# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .tfidf import model, corpus, urls, keywords, vocabulary, metadatas
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
import sentence_transformers
from sklearn.metrics.pairwise import cosine_similarity

embedding = HuggingFaceEmbeddings(model_name="hiiamsid/sentence_similarity_spanish_es")


class ActionDarInfoGeneral(Action):

    def name(self) -> Text:
        return "action_dar_info_general"
    
    
    def get_documents(self, query):
        indices = model.query_documents(query)
        
        indices_no_encontrados = (0.0 in indices.values())
        if indices_no_encontrados:
            return None
        
        # if indices_no_encontrados:
        #     dispatcher.utter_message(template="utter_out_of_scope")
        #     return []
        # documentos_mas_parecidos = [] # [corpus[i] for _, i in indices]
        # metadatas_mas_parecidas  = [] #[metadatas[i] for _, i in indices]
        
        return indices # , documentos_mas_parecidos, metadatas_mas_parecidas
        
    
    def search_engine(self, query, indices):
        texto_results = [corpus[idx] for idx in indices]
        metadatas_results = [metadatas[idx] for idx in indices]
        
        new_results = []
        for doc, metadata in zip(texto_results, metadatas_results):
            new_results.append(Document(page_content=doc, metadata=metadata))
            
        
        embeddings = embedding.embed_documents([result.page_content for result in new_results])
        query_embedding = embedding.embed_query(query)
        
        result = cosine_similarity([query_embedding], embeddings)
        
        documentos_similares = sorted(zip(result[0], indices), reverse=True)
        print(documentos_similares)
        
        # urls_mas_parecidas = [metadata['url'] for metadata in metadatas_mas_parecidas] # metadatas_mas_parecidas.apply(lambda x: x.get("url")) doc['url'] for doc in lista_documentos
        return documentos_similares # documentos_mas_parecidos, urls_mas_parecidas, valores
    
    

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = tracker.latest_message["text"]
        
        try:
            indices_result = self.get_documents(query)
        except Exception as e:
            print("No entendio", e)
            dispatcher.utter_message(template="utter_out_of_scope")
            return []
        # documentos_similares = self.search_engine(query, indices_result)
        # print(indices_result)
        # valores = [value[0] for value in indices_result]
        # indices_filtrados = [value[1] for value in indices_result]
        indices_filtrados = list(indices_result.keys())
        valores = list(indices_result.values())
        
        print("##############################",valores)
        print("##############################",indices_filtrados)
        
        documents_most_similar =  [corpus[i] for i in indices_filtrados]
        metadatas_mas_parecidas  = [metadatas[i] for i in indices_filtrados]
        
        # documents_most_similar = [texto_results[i] for i in indices_filtrados]
        # metadatas_mas_parecidas  = [metadatas_results[i] for i in indices_filtrados]
        urls_most_similar = [metadata['url'] for metadata in metadatas_mas_parecidas] 
        
        
        splits = [document.split('\n') for document in documents_most_similar]
        titles = [split[0] for split in splits]
        response = ""
        for title, url, valor in zip(titles, urls_most_similar, valores):
            if valor < 0.05:
                continue
            if title == "" or url.endswith('.pdf'):
                title = "Documento PDF"
            if len(title) > 15:
                title = title[:30] + "..."
            response+=f"{title}: {url}\n"
        
        

        # Cargar el JSON y realizar la búsqueda con una pregunta dada
        # json_data = json.loads(documentos_json)
        # pregunta = "Qué puedo hacer en servicios escolares?"
        # documentos_similares = buscar_documentos_similares(keywords, query)
                
        msg = f"{valores}\nEstas son algunas páginas relacionadas que pude encontrar\n\n"+response+"\n\n"
        # model.tfidf_matrix

        dispatcher.utter_message(text=msg)

        return []
