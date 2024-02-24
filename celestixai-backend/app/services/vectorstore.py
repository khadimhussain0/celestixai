import os
import pysqlite3
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import glob
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
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.docstore.document import Document


class DocumentProcessor:
    def __init__(
        self,
        files,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embeddings_model_name: str = 'all-MiniLM-L6-v2',
        ollama_embedder = None
    ):
        self.files = files
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings_model_name = embeddings_model_name
        self.ollama_embedder = ollama_embedder
        if self.ollama_embedder is None:
            self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        else:
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
        return texts

    def process_documents(self, collection_name: str, ignored_files: List[str] = []) -> None:
        url = "<---qdrant url here --->"
        texts = self._process_documents()
        print(f"Creating embeddings. May take some minutes...")
        qdrant = Qdrant.from_texts(
            texts,
            self.ollama_embedder,
            location=":memory:",
            # url=url,
            # prefer_grpc=True,
            collection_name="my_documents",
        )
        # db = Qdrant.from_documents(documents, embeddings, "http://localhost:6333")
        # db = Chroma.from_documents(texts, self.embeddings, persist_directory=self.persist_directory)
        print("Document Embedding complete!")


if __name__ == "__main__":
    ollama_embedder= OllamaEmbeddings(base_url='http://celestixai-ollama-1:11434')
    print(os.listdir("/app/vectorestore/1/source_documents"))
    files= ["/app/vectorestore/1/source_documents/file.txt"]
    processor = DocumentProcessor(files=files, ollama_embedder=ollama_embedder)
    processor.process_documents("docs")
