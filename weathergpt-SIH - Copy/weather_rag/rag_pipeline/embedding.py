from langchain_ollama import OllamaEmbeddings

class EmbeddingModel:
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
        self.model = None

    def load_model(self):
        self.model = OllamaEmbeddings(
            model=self.model_name,
            base_url="http://127.0.0.1:11434"
        )

        print(f"Embedding model loaded: {self.model_name}")

        return self.model

