from .browser_models import BrowserTask
from .desktop_models import DeskTopTask
from .email_generation_models import EmailGenerationTask
from .pdf_assistant_models import PdfAssistantTask

from pydantic import BaseModel, Field
from typing import Annotated

Task = Annotated[
    BrowserTask | DeskTopTask | EmailGenerationTask | PdfAssistantTask,
    Field(discriminator="module"),
]


class TaskRouterResponse(BaseModel):
    acknowledgement_before_task: str
    tasks: list[Task]