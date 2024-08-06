from typing import Any, Optional, Literal
from dataclasses import dataclass, asdict
import json


FileType = Literal["application/pdf"]


@dataclass()
class Error(BaseException):
    code: int
    message: str
    data: Optional[Any] = None

    def __str__(self):
        return json.dumps(asdict(self), allow_nan=False)


@dataclass(frozen=True)
class Collection:
    id: str
    name: str
    embedding_model: str
    embedding_dimensions: str
    search_queries: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class CreateCollectionRequest:
    name: str
    file_ids: list[str]


@dataclass(frozen=True)
class FileToAdd:
    url: str
    type: FileType
    name: str


@dataclass(frozen=True)
class AddFilesRequest:
    files: list[FileToAdd]
    collection_id: str


@dataclass(frozen=True)
class CollectionFile:
    id: str
    name: str
    type: FileType
    url: str
    user_id: str
    connector_id: str
    size: int
    md5_hash: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class SearchCollectionRequest:
    text: str
    collection_id: str


@dataclass(frozen=True)
class SearchResult:
    content: str
    file_id: str
