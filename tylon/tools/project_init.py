# tylon/tools/project_init.py
import subprocess
from jinja2 import Template
import os
from langchain.tools import tool
from tylon.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=settings.google_api_key)

def parse_project_description(description: str) -> dict:
    prompt = f"""
    Parse this description and extract:
    - Project type (e.g., FastAPI, Django)
    - Dependencies (e.g., SQLAlchemy, JWT)
    Description: {description}
    Return as JSON.
    """
    response = llm.invoke(prompt).content
    return json.loads(response)

@tool
def initialize_project(description: str) -> str:
    """Initialize a new project based on description"""
    details = parse_project_description(description)
    project_type = details.get("project_type", "").lower()
    deps = details.get("dependencies", [])
    project_name = "my_project"

    if project_type == "fastapi":
        os.makedirs(project_name, exist_ok=True)
        subprocess.run(["poetry", "init", "-n"], cwd=project_name, check=True)
        base_deps = ["fastapi", "uvicorn"]
        subprocess.run(["poetry", "add"] + base_deps + deps, cwd=project_name, check=True)
        
        with open("tylon/templates/fastapi_main.j2") as f:
            template = Template(f.read())
        code = template.render({"dependencies": deps})
        with open(f"{project_name}/main.py", "w") as f:
            f.write(code)
        return f"Initialized {project_type} project '{project_name}'."
    return "Unsupported project type."