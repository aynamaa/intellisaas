from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    length_function=len,
)

async def summarize_document(text: str) -> str:
    if not text or len(text.strip()) < 50:
        return "Document is too short to summarize."
    truncated = text[:8000]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Please provide a clear concise summary of this document in 3-5 sentences:\n\n{truncated}"
        }],
        max_tokens=500
    )
    return response.choices[0].message.content

async def chat_with_document(text: str, question: str) -> str:
    if not text:
        return "No document content available."
    truncated = text[:8000]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Based on this document:\n\n{truncated}\n\nAnswer this question: {question}"
        }],
        max_tokens=500
    )
    return response.choices[0].message.content

def split_text(text: str) -> list[str]:
    return text_splitter.split_text(text)