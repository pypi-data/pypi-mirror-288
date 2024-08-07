import os
import typer
from typing import TypeVar

from pydantic.main import BaseModel
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import OutputDirExistsException

from startfastapi.context import ProjectContext, AppContext
from startfastapi.config import TEMPLATES_DIR

ContextType = TypeVar("ContextType", bound=BaseModel)


def fill_template(template_name: str, context: ContextType):
    try:
        cookiecutter(
            os.path.join(TEMPLATES_DIR, template_name),
            extra_context=context.dict(),
            no_input=True,
        )
    except OutputDirExistsException:
        typer.echo(f"Folder '{context.folder_name}' already exists. 😞")
    else:
        typer.echo(f"FastAPI {template_name} created successfully! 🎉")


def generate_project(context: ProjectContext):
    fill_template("project", context)


def generate_app(context: AppContext):
    fill_template("app", context)
