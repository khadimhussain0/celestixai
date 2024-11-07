import os
from app.core.config import QDRANT_SERVER_URL
from typing import List
from multiprocessing import Pool
from tqdm import tqdm
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from langchain.docstore.document import Document


class DocumentProcessor:
    def __init__(
        self,
        files,
        ollama_embedder,
        chunk_size: int = 1024,
        chunk_overlap: int = 200,
    ):
        self.files = files
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.ollama_embedder = ollama_embedder
        self.embeddings = self.ollama_embedder

        # Define loader mappings
        self.LOADER_MAPPING = {
            ".csv": (CSVLoader, {}),
            ".doc": (UnstructuredWordDocumentLoader, {}),
            ".docx": (UnstructuredWordDocumentLoader, {}),
            ".enex": (EverNoteLoader, {}),
            ".eml": (UnstructuredEmailLoader, {}),
            ".epub": (UnstructuredEPubLoader, {}),
            ".html": (UnstructuredHTMLLoader, {}),
            ".md": (UnstructuredMarkdownLoader, {}),
            ".odt": (UnstructuredODTLoader, {}),
            ".pdf": (PyMuPDFLoader, {}),
            ".ppt": (UnstructuredPowerPointLoader, {}),
            ".pptx": (UnstructuredPowerPointLoader, {}),
            ".txt": (TextLoader, {"encoding": "utf8"}),
        }

    def _load_single_document(self, file_path: str) -> List[Document]:
        ext = "." + file_path.rsplit(".", 1)[-1]
        if ext in self.LOADER_MAPPING:
            loader_class, loader_args = self.LOADER_MAPPING[ext]
            loader = loader_class(file_path, **loader_args)
            return loader.load()
        raise ValueError(f"Unsupported file extension '{ext}'")

    def _load_documents(self, files: List[str], ignored_files: List[str] = []) -> List[Document]:
        all_files = []
        for ext in self.LOADER_MAPPING:
            all_files.extend([file for file in files if file.endswith(ext)])
        filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]
        with Pool(processes=os.cpu_count()) as pool:
            results = []
            with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
                for i, docs in enumerate(pool.imap_unordered(self._load_single_document, filtered_files)):
                    results.extend(docs)
                    pbar.update()
        return results

    def _process_documents(self, ignored_files: List[str] = []) -> List[Document]:
        documents = self._load_documents(self.files, ignored_files)
        if not documents:
            print("No new documents to load")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        texts = text_splitter.split_documents(documents)
        print(f"Split into {len(texts)} chunks of text (max. {self.chunk_size} tokens each)")
        return documents, texts

    def process_documents(self, collection_name: str = "vectorstore", ignored_files: List[str] = []) -> None:
        documents, texts = self._process_documents(ignored_files)

        client = QdrantClient(url=QDRANT_SERVER_URL)
        try:
            collections = client.get_collection(collection_name)
            existing_vector_size = collections.config.params.vectors.size
            print(f"Collection '{collection_name}' already exists with {existing_vector_size} vectors.")
            if existing_vector_size != 768:
                print(f"Recreating collection '{collection_name}' with new vector size of 768.")
                client.delete_collection(collection_name)  # Delete the existing collection with incorrect dimensions
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
                )
        except UnexpectedResponse:
            print(f"Collection '{collection_name}' does not exist. Creating new collection.")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
            )
        vector_store = QdrantVectorStore(
                        client=client,
                        collection_name=collection_name,
                        embedding=self.ollama_embedder,
                        
                    )

        vector_store.add_documents(documents=documents)
        
        if False:
            retriever = vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={"k": 1, "fetch_k": 2, "lambda_mult": 0.5},
            )

            query = "hello"
            try:
                found_docs = vector_store.similarity_search_with_score(query)
                if found_docs:
                    document, score = found_docs[0]
                    print(document.page_content)
                    print(f"\nScore: {score}")
                else:
                    print("No documents found for the query.")
            except Exception as e:
                print(f"Error during similarity search: {e}")
        print("Document Embedding complete!")

if __name__ == "__main__":
    ollama_embedder = OllamaEmbeddings(base_url='http://ollama:11434', model='nomic-embed-text')
    files = ["dataset_storage/0f557ad1-73f4-4785-9dfb-24d6129803bd____Khadim_Hussain_Resume_one_page.pdf"]
    processor = DocumentProcessor(files=files, ollama_embedder=ollama_embedder)
    processor.process_documents()
    print("Embedding done")
