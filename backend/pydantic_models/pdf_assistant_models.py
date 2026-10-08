from pydantic import BaseModel, Field


class PdfAssistant(BaseModel):
    query: str
