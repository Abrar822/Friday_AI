from pydantic import BaseModel, Field
from typing import Literal, Annotated


class SearchSpecificWebsiteParams(BaseModel):
    website_name: Literal[
        "youtube",
        "google",
        "github",
        "wikipedia",
        "reddit",
        "amazon",
        "linkedin",
        "facebook",
        "instagram",
        "twitter",
        "x",
        "spotify",
    ]
    query: str


class SearchSpecificWebsite(BaseModel):
    id: int
    module: Literal["browser"]
    action: Literal["search_specific_website"]
    parameters: SearchSpecificWebsiteParams


class OpenWebsiteParams(BaseModel):
    url: str


class OpenWebsite(BaseModel):
    id: int
    module: Literal["browser"]
    action: Literal["open_website"]
    parameters: OpenWebsiteParams


class SummarizeWebsiteParams(BaseModel):
    url: str


class SummarizeWebsite(BaseModel):
    id: int
    module: Literal["browser"]
    action: Literal["summarize_website"]
    parameters: SummarizeWebsiteParams

class ComposeEmailParams(BaseModel):
    subject: str
    body: str


class ComposeEmail(BaseModel):
    id: int
    module: Literal["browser"]
    action: Literal["compose_email"]
    parameters: ComposeEmailParams


BrowserTask = Annotated[
    OpenWebsite | SummarizeWebsite | SearchSpecificWebsite | ComposeEmail,
    Field(discriminator="action"),
]
