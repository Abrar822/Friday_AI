from .browser_models import BrowserTask
from .desktop_models import DeskTopTask

from pydantic import BaseModel, Field
from typing import Annotated

Task = Annotated[
    BrowserTask | DeskTopTask,
    Field(discriminator="module"),
]


class TaskRouterResponse(BaseModel):
    acknowledgement_before_task: str
    tasks: list[Task]