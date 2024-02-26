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
from langchain_community.vectorstores import Qdrant
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
        return texts

    async def process_documents(self, collection_name: str = "vectorstore", ignored_files: List[str] = []) -> None:
        url = QDRANT_SERVER_URL
        texts = self._process_documents(ignored_files)
        print(f"Creating embeddings. May take some minutes...")
        qdrant = await Qdrant.afrom_documents(
            texts,
            self.ollama_embedder,
            url=url,
            prefer_grpc=True,
            collection_name=collection_name,
        )

        # query="hello"
        # found_docs = await qdrant.similarity_search_with_score(query)
        # document, score = found_docs[0]
        # print(document.page_content)
        # print(f"\nScore: {score}")
        print("Document Embedding complete!")


if __name__ == "__main__":
    ollama_embedder= OllamaEmbeddings(base_url='http://celestixai-ollama-1:11434', model='nomic-embed-text')
    files= ["/app/vectorestore/galaxticmart.txt"]
    processor = DocumentProcessor(files=files, ollama_embedder=ollama_embedder)
    processor.process_documents()
    print("embedding done")
