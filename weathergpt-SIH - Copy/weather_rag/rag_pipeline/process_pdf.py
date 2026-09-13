from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
def pdf_loader(path_loader):

    all_documents = []

    path_dir = Path(path_loader)

    pdf_files = list(path_dir.glob("**/*.pdf"))

    for data in pdf_files:
        try:
            loader = PyMuPDFLoader(str(data))

            documents = loader.load()

            for doc in documents:
                doc.metadata["source_file"] = data.name
                doc.metadata["file_type"] = "pdf"
            all_documents.extend(documents)
            print(
                f"Loaded {data.name}: {len(documents)} pages"
            )

        except Exception as e:
            print(f"Error loading {data}: {e}")

    print(
        f"Total documents/pages: {len(all_documents)}"
    )

    return all_documents