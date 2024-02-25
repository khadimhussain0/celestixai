import os
import pysqlite3
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import time
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Qdrant
import qdrant_client
from langchain_community.llms import Ollama


class RAGChat:
    def __init__(self, ollama_embedder, ollama, target_source_chunks=4, mute_stream=False, hide_source=False):
        self.ollama= ollama
        self.embeddings = ollama_embedder
        self.target_source_chunks = target_source_chunks
        self.mute_stream = mute_stream
        self.hide_source = hide_source

    def ask_question(self, query, collection_name: str = "vectorstore"):
        url = "http://celestixai-qdrant-1:6333"
        print(f"Fetching embeddings. May take some minutes...")
        client = qdrant_client.QdrantClient("http://celestixai-qdrant-1:6333", prefer_grpc=True)
        doc_store = Qdrant(
                    client=client, collection_name=collection_name, 
                    embeddings=self.embeddings,
                )
        retriever = doc_store.as_retriever(search_kwargs={"k": self.target_source_chunks})
        llm = self.ollama
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=not self.hide_source)

        start = time.time()
        res = qa(query)
        end = time.time()

        answer, docs = res['result'], [] if self.hide_source else res['source_documents']
        print(f"Took to retrieve: {end-start}s")
        print("this is answer", answer)
        print("this is doc", docs)
        return answer, docs


if __name__=="__main__":
    ollama_embedder = OllamaEmbeddings(base_url='http://celestixai-ollama-1:11434', model="nomic-embed-text")
    ollama_server = Ollama(base_url='http://celestixai-ollama-1:11434', model="llama2")
    chat = RAGChat(ollama_embedder=ollama_embedder, ollama=ollama_server)
    chat.ask_question('what is GalacticMart', collection_name="docs")

    client = qdrant_client.QdrantClient("http://celestixai-qdrant-1:6333", prefer_grpc=True)
    print(client.get_collections())


