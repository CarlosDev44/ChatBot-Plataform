from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def generate_embeddings(documents: list[Document]):

    texts = [
        document.page_content
        for document in documents
    ]

    embeddings = get_model().encode(texts)

    return embeddings


def generate_query_embedding(query: str):

    embedding = get_model().encode(query)

    return embedding
