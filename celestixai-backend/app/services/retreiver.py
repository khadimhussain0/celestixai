import time
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Qdrant
import qdrant_client
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


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

        template = """Answer the following question using the provided context.
                If you can't find the answer, do not pretend you know it, but answer "I don't know":
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        print(prompt)
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            |self.ollama
            | StrOutputParser()
            )
        
        start = time.time()
        end = time.time()

        answer, docs = chain.invoke(query), []
        print(answer)
        print(f"Took to retrieve: {end-start}s")
        return answer, docs


if __name__=="__main__":
    ollama_embedder = OllamaEmbeddings(base_url='http://ollama:11434', model="nomic-embed-text")
    ollama_server = Ollama(base_url='http://ollama:11434', model="tinyllama")
    chat = RAGChat(ollama_embedder=ollama_embedder, ollama=ollama_server)
    chat.ask_question('what is GalacticMart', collection_name="1")

    client = qdrant_client.QdrantClient("http://qdrant:6333", prefer_grpc=True)
    print(client.get_collections())
