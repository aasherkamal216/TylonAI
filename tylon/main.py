# tylon/main.py
import typer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool
from langgraph.prebuilt import create_react_agent
from rich.console import Console
from tylon.config import settings, project_config, load_project_config
from tylon.tools import (
    initialize_project, 
    query_codebase, get_system_info, generate_code,

)

app = typer.Typer()
console = Console()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=settings.google_api_key)

tools = [
    initialize_project,
    query_codebase,
    get_system_info,
    generate_code,
]
agent = create_react_agent(model=llm, tools=tools)

@app.command()
def init():
    """Initialize the project context."""
    config = ProjectConfig(project_type="python", language="python", frameworks=[])
    with open(".tylonrc", "w") as f:
        f.write(config.json())
    console.print("[green]Project context initialized.[/green]")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, instruction: str = typer.Argument(None)):
    """Process natural language instructions with tylon."""
    if ctx.invoked_subcommand is None:
        if not instruction:
            console.print("[red]Please provide an instruction.[/red]")
            raise typer.Exit()
        result = agent.invoke({"messages": [{"role": "user", "content": f"Instruction: {instruction}\nProject Config: {project_config.model_dump_json()}"}]})
        console.print(result['messages'][-1].content)

if __name__ == "__main__":
    app()