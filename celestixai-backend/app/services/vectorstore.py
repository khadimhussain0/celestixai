import os
import glob
from typing import List
from multiprocessing import Pool
from tqdm import tqdm
from langchain.document_loaders import (
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
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from chromadb.config import Settings


class DocumentProcessor:
    def __init__(
        self,
        source_directory: str,
        persist_directory: str = 'db',
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embeddings_model_name: str = 'all-MiniLM-L6-v2',
    ):
        self.source_directory = source_directory
        self.persist_directory = persist_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings_model_name = embeddings_model_name
        self.CHROMA_SETTINGS = Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        )
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

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

    def _load_documents(self, ignored_files: List[str] = []) -> List[Document]:
        all_files = []
        for ext in self.LOADER_MAPPING:
            all_files.extend(glob.glob(os.path.join(self.source_directory, f"**/*{ext}"), recursive=True))
        filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]
        with Pool(processes=os.cpu_count()) as pool:
            results = []
            with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
                for i, docs in enumerate(pool.imap_unordered(self._load_single_document, filtered_files)):
                    results.extend(docs)
                    pbar.update()
        return results

    def _process_documents(self, ignored_files: List[str] = []) -> List[Document]:
        print(f"Loading documents from {self.source_directory}")
        documents = self._load_documents(ignored_files)
        if not documents:
            print("No new documents to load")
            exit(0)
        print(f"Loaded {len(documents)} new documents from {self.source_directory}")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        texts = text_splitter.split_documents(documents)
        print(f"Split into {len(texts)} chunks of text (max. {self.chunk_size} tokens each)")
        return texts

    def _does_vectorstore_exist(self) -> bool:
        if os.path.exists(os.path.join(self.persist_directory, 'index')):
            if os.path.exists(os.path.join(self.persist_directory, 'chroma-collections.parquet')) and os.path.exists(os.path.join(self.persist_directory, 'chroma-embeddings.parquet')):
                list_index_files = glob.glob(os.path.join(self.persist_directory, 'index/*.bin'))
                list_index_files += glob.glob(os.path.join(self.persist_directory, 'index/*.pkl'))
                if len(list_index_files) > 3:
                    return True
        return False

    def process_documents(self, ignored_files: List[str] = []) -> None:
        if self._does_vectorstore_exist():
            print(f"Appending to existing vectorstore at {self.persist_directory}")
            db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings, client_settings=self.CHROMA_SETTINGS)
            collection = db.get()
            texts = self._process_documents([metadata['source'] for metadata in collection['metadatas']])
            print(f"Creating embeddings. May take some minutes...")
            db.add_documents(texts)
        else:
            print("Creating new vectorstore")
            texts = self._process_documents()
            print(f"Creating embeddings. May take some minutes...")
            db = Chroma.from_documents(texts, self.embeddings, persist_directory=self.persist_directory)
        db.persist()
        db = None
        print("Ingestion complete!")


if __name__ == "__main__":
    source_dir = os.environ.get('SOURCE_DIRECTORY', 'source_documents')
    persist_dir = os.environ.get('PERSIST_DIRECTORY', 'db')
    processor = DocumentProcessor(source_directory=source_dir, persist_directory=persist_dir)
    processor.process_documents()
