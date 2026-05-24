import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    length_function=len,
)

async def summarize_document(text: str) -> str:
    if not text or len(text.strip()) < 50:
        return "Document is too short to summarize."
    truncated = text[:4000]
    response = ollama.chat(
        model="llama3.2",
        messages=[{
            "role": "user",
            "content": f"Summarize this document in 3-5 clear sentences:\n\n{truncated}"
        }]
    )
    return response["message"]["content"]

async def chat_with_document(text: str, question: str) -> str:
    if not text:
        return "No document content available."
    truncated = text[:4000]
    response = ollama.chat(
        model="llama3.2",
        messages=[{
            "role": "user",
            "content": f"Based on this document:\n\n{truncated}\n\nAnswer this question: {question}"
        }]
    )
    return response["message"]["content"]

def split_text(text: str) -> list[str]:
    return text_splitter.split_text(text)