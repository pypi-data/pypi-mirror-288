import typer

from startfastapi.context import ProjectContext, AppContext
from startfastapi.generator import generate_project, generate_app


app = typer.Typer(
    add_completion=False,
    help="Managing FastAPI projects made easy!",
    name="Manage FastAPI",
)


@app.command(help="Creates a FastAPI project.")
def startproject(name: str):
    context = ProjectContext(name=name)
    generate_project(context)


@app.command(help="Creates a FastAPI app.")
def startapp(name: str):
    context = AppContext(name=name)
    generate_app(context)