from pydantic import BaseModel


class VisualDescription(BaseModel):
    subject: str
    action: str
    setting: str
    key_elements: list[str]


class Panel(BaseModel):
    panel_number: int
    visual_description: VisualDescription
