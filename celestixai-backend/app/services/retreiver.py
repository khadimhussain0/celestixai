import time
from langchain.chains import RetrievalQA
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

    def ask_question(self, query, qdrant_url="http://qdrant:6333", collection_name: str = "vectorstore"):
        print(f"Fetching embeddings. May take some minutes...")
        client = qdrant_client.QdrantClient(qdrant_url, prefer_grpc=True)
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
        # print("this is answer", answer)
        # print("this is doc", docs)
        return answer, docs


if __name__=="__main__":
    ollama_embedder = OllamaEmbeddings(base_url='http://ollama:11434', model="nomic-embed-text")
    ollama_server = Ollama(base_url='http://ollama:11434', model="tinyllama")
    chat = RAGChat(ollama_embedder=ollama_embedder, ollama=ollama_server)
    chat.ask_question('what is GalacticMart', collection_name="1")

    client = qdrant_client.QdrantClient("http://qdrant:6333", prefer_grpc=True)
    print(client.get_collections())
