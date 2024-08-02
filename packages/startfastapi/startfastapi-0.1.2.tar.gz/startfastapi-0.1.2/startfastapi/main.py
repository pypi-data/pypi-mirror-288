import typer

from startfastapi.context import ProjectContext
from startfastapi.generator import generate_project


app = typer.Typer(
    add_completion=False,
    help="Managing FastAPI projects made easy!",
    name="Manage FastAPI",
)


@app.command(help="Creates a FastAPI project.")
def project(name: str):
    context = ProjectContext(name=name)
    generate_project(context)