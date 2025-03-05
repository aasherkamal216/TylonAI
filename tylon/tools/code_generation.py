# tylon/tools/code_generation.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from tylon.config import settings

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=settings.google_api_key)
@tool
def generate_code(description: str) -> str:
    """Generate code from description"""
    prompt = f"Generate Python code for: {description}"
    return llm.invoke(prompt).content