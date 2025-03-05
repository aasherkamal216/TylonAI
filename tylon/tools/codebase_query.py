# tylon/tools/codebase_query.py
import subprocess
from langchain.tools import tool
@tool
def query_codebase(query: str) -> str:
    """Query the codebase with natural language"""
    result = subprocess.run(["rg", query, "."], capture_output=True, text=True)
    return result.stdout or "No matches found."