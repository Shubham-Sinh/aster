import os
from langchain_community.vectorstores import FAISS


class VectorStore:

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vectorstore = None

    def create_vector_store(self, chunks):
        if not chunks:
            raise ValueError("No chunks provided to create vector store.")

        batch_size = 32

        print(
            f"Creating vector store for {len(chunks)} chunks "
            f"in batches of {batch_size}..."
        )

        initial_batch = chunks[:batch_size]

        self.vectorstore = FAISS.from_documents(
            documents=initial_batch,
            embedding=self.embedding_model
        )

        for i in range(batch_size, len(chunks), batch_size):

            batch = chunks[i:i + batch_size]

            self.vectorstore.add_documents(batch)

            print(
                f"Processed "
                f"{min(i + batch_size, len(chunks))}/{len(chunks)} chunks..."
            )

        print("Vector store created successfully!")

    def save_vector_store(self, folder_path):
        if self.vectorstore is None:
            raise ValueError("Vector store has not been created yet.")

        os.makedirs(folder_path, exist_ok=True)

        self.vectorstore.save_local(folder_path)

        print(
            f"FAISS vector store saved to: {folder_path}"
        )

    def load_vector_store(self, folder_path):
        if not os.path.exists(folder_path):
            return False

        try:
            self.vectorstore = FAISS.load_local(
                folder_path,
                self.embedding_model,
                allow_dangerous_deserialization=True
            )

            print(
                f"FAISS vector store loaded from: {folder_path}"
            )

            return True

        except Exception as e:

            print(
                f"Could not load FAISS vector store: {e}"
            )

            self.vectorstore = None

            return False

    def create_retriever(self, k=3):

        if self.vectorstore is None:
            raise ValueError(
                "Create or load vector store first."
            )

        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )

        print(
            f"Retriever created with k={k}"
        )

        return self.retriever