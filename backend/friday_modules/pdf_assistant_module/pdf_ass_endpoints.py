from fastapi import APIRouter, UploadFile, Form, File
import pymupdf
from .pdf_assistant_clients import load_model, to_llm
from ...pydantic_models.pdf_assistant_models import PdfAssistant
import chromadb
from pathlib import Path

pdf_upload_endpoints = APIRouter()
model = None
collection = None
chroma_db_client = None


@pdf_upload_endpoints.post("/pdf/upload")
async def pdf_upload(
    files: list[UploadFile] = File(...), doc_ids: list[str] = Form(...)
):
    global model, collection, chroma_db_client
    model, collection, chroma_db_client = load_model(
        chroma_db_client, collection, model
    )
    filenames = [
        {"filename": f.filename, "doc_id": id} for f, id in zip(files, doc_ids)
    ]

    # reading the documents
    content = []
    for file, doc_id in zip(files, doc_ids):
        text = ""
        file_bytes = await file.read()
        document = pymupdf.open(stream=file_bytes, filetype="pdf")
        for page in document:
            text += page.get_text()
        document.close()
        content.append({"doc_id": doc_id, "text": text, "filename": file.filename})

    # chunking + embedding + storing
    chunks = []
    ids = []
    embeddings = []
    metadatas = []
    for fileObj in content:
        my_doc_id = fileObj["doc_id"]
        my_text = fileObj["text"]
        my_filename = fileObj["filename"]

        chunk_size = 800
        end = chunk_size
        for start in range(0, len(my_text), chunk_size):
            chunk = my_text[start : start + end]
            if chunk:
                embedding = model.encode(chunk).tolist()

                ids.append(f"chunk_{my_doc_id}_{start // chunk_size}")
                embeddings.append(embedding)
                chunks.append(chunk)
                metadatas.append({"filename": my_filename, "doc_id": my_doc_id})

    collection.add(
        ids=ids, metadatas=metadatas, documents=chunks, embeddings=embeddings
    )

    return filenames


@pdf_upload_endpoints.delete("/pdf/delete")
def delete_files():
    global model, collection, chroma_db_client

    path = Path.home() / "Friday_AI" / "chromadb.db"
    chroma_db_client = chromadb.PersistentClient(path=str(path))
    chroma_db_client.delete_collection(name="Friday_documents_collection")

    model = None
    chroma_db_client = None
    collection = None

    return {"message": "Files removed successfully."}


@pdf_upload_endpoints.post("/pdf/query")
def query(pdf_assist: PdfAssistant):
    global model, collection
    query = pdf_assist.query
    embedded_query = model.encode(query).tolist()

    results = collection.query(query_embeddings=[embedded_query], n_results=2)
    context = "".join(results["documents"][0])
    query = f"""
    USER QUERY: {query}
    PDF CONTEXT: {context}
    """
    result = to_llm(query)

    return result


@pdf_upload_endpoints.get("/pdf/get")
def get_data():
    def removeDuplicates(data):
        filenames = set()
        new_data = []
        for tupl in data:
            if tupl['filename'] not in filenames:
                new_data.append({'filename': tupl['filename'], 'doc_id': tupl['doc_id']})
                filenames.add(tupl['filename'])
        return new_data

    path = Path.home() / "Friday_AI" / "chromadb.db"
    chroma_db_client = chromadb.PersistentClient(path=str(path))
    collection = chroma_db_client.get_or_create_collection(
        name="Friday_documents_collection"
    )
    data = collection.get(include=["metadatas"])
    data = [{"filename": d['filename'], "doc_id": d['doc_id']} for d in data['metadatas']]
    data = removeDuplicates(data)
    return data
