from langchain_text_splitters import RecursiveCharacterTextSplitter

def text_splitting(
    documents,
    chunk_size=1000,
    chunk_overlap=200
):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            " ",
            ""
        ]
    )

    split_docs = text_splitter.split_documents(
        documents
    )

    print(
        f"Original documents: {len(documents)}"
    )

    print(
        f"Total chunks: {len(split_docs)}"
    )

    if split_docs:
        print(
            f"First chunk metadata: "
            f"{split_docs[0].metadata}"
        )

        print(
            f"First chunk text: "
            f"{split_docs[0].page_content[:200]}"
        )

    return split_docs