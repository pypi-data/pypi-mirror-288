from src.apis.model import Base


class {{ cookiecutter.class_name }}Model(Base, table=True):
    """
    {{ cookiecutter.class_name }} Model
    """

    __tablename__ = "{{ cookiecutter.name }}"
    ...