from pydantic import BaseModel, root_validator


class ProjectContext(BaseModel):
    name: str
    folder_name: str

    class Config:
        use_enum_values = True

    @root_validator(pre=True)
    def validate_app(cls, values: dict):
        values["folder_name"] = values["name"].lower().replace(" ", "-").strip()
        return values


class AppContext(BaseModel):
    name: str
    folder_name: str

    @root_validator(pre=True)
    def validate_app(cls, values: dict):
        values["folder_name"] = values["name"].lower().replace(" ", "-").strip()
        return values