import os
import time
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import Ollama


class PrivateGPT:
    def __init__(self, embeddings_model_name="all-MiniLM-L6-v2", ollama_model="llama2-uncensored", persist_directory="db", target_source_chunks=4, mute_stream=False, hide_source=False):
        self.ollama_model = ollama_model
        self.embeddings_model_name = embeddings_model_name
        self.persist_directory = persist_directory
        self.target_source_chunks = target_source_chunks
        self.mute_stream = mute_stream
        self.hide_source = hide_source

    def ask_question(self, query):
        embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_model_name)
        db = Chroma(persist_directory=self.persist_directory, embedding_function=embeddings)
        retriever = db.as_retriever(search_kwargs={"k": self.target_source_chunks})
        callbacks = [] if self.mute_stream else [StreamingStdOutCallbackHandler()]
        llm = Ollama(model=self.ollama_model, callbacks=callbacks)
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=not self.hide_source)

        start = time.time()
        res = qa(query)
        end = time.time()

        answer, docs = res['result'], [] if self.hide_source else res['source_documents']
        print(f"Took to retrieve: {end-start}s")
        return answer, docs


if __name__=="__main__":
    pass
