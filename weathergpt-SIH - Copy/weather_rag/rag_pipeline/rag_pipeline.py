from .process_pdf import pdf_loader
from .splitting_text import text_splitting
from .embedding import EmbeddingModel
from .vector_db import VectorStore
import os


class RagPipeline:

    def __init__(self):
        self.pdf_loader = pdf_loader
        self.text_splitting = text_splitting

        embedding = EmbeddingModel(
            model_name="nomic-embed-text"
        )

        self.embedding_model = embedding.load_model()

        self.vector_store = VectorStore(
            self.embedding_model
        )

    def build_pipeline(self):

        current_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        pdf_folder_path = os.path.join(
            current_dir,
            "pdf_file"
        )

        # Folder where FAISS will be stored
        faiss_folder = os.path.join(
            current_dir,
            "faiss_index"
        )

        # -----------------------------------------
        # TRY TO LOAD EXISTING FAISS
        # -----------------------------------------

        loaded = self.vector_store.load_vector_store(
            faiss_folder
        )

        if loaded:

            print("✅ Existing FAISS knowledge base loaded.")

            return self.vector_store.create_retriever(
                k=3
            )

        # -----------------------------------------
        # FAISS DOES NOT EXIST
        # BUILD IT
        # -----------------------------------------

        print("🔄 Building FAISS knowledge base...")

        documents = self.pdf_loader(
            pdf_folder_path
        )

        print(
            f"Loaded documents count: {len(documents)}"
        )

        if not documents:

            raise ValueError(
                f"No documents found at path: "
                f"{pdf_folder_path}"
            )

        chunks = self.text_splitting(
            documents
        )

        print(
            f"Creating vector store for "
            f"{len(chunks)} chunks..."
        )

        self.vector_store.create_vector_store(
            chunks
        )

        # -----------------------------------------
        # SAVE FAISS TO DISK
        # -----------------------------------------

        self.vector_store.save_vector_store(
            faiss_folder
        )

        print(
            "✅ FAISS knowledge base saved successfully."
        )

        return self.vector_store.create_retriever(
            k=3
        )


# =================================================
# CACHE RETRIEVER IN MEMORY
# =================================================

_rag_retriever = None


def get_rag_retriever():

    global _rag_retriever

    if _rag_retriever is None:

        print(
            "🔄 Loading WeatherGPT knowledge base..."
        )

        pipeline = RagPipeline()

        _rag_retriever = pipeline.build_pipeline()

        print(
            "✅ WeatherGPT RAG is ready!"
        )

    return _rag_retriever


def build_pipeline(question=None):

    retriever = get_rag_retriever()

    if question:

        return retriever.invoke(
            question
        )

    return retriever