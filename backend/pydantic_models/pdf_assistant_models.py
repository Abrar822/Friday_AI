from pydantic import BaseModel, Field
from typing import Literal, Annotated


class PdfAssistant(BaseModel):
    query: str


class PdfAssistantParams(BaseModel):
    id: int
    module: Literal["pdf"]
    action: Literal["pdf_assistant"]
    parameters: PdfAssistantParams


PdfAssistantTask = Annotated[PdfAssistantParams, Field(discriminator="action")]
