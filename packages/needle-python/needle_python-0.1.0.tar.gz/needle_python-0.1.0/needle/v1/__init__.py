from typing import Optional
import os
from dataclasses import dataclass, asdict
import requests

from needle.v1.model import (
    CreateCollectionRequest,
    AddFilesRequest,
    SearchCollectionRequest,
    Collection,
    CollectionFile,
    SearchResult,
    Error,
)


@dataclass(frozen=True)
class NeedleConfig:
    api_key: Optional[str]
    url: Optional[str]
    search_url: Optional[str]


@dataclass(frozen=True)
class NeedleBaseClient:
    config: NeedleConfig
    headers: dict


class NeedleClient(NeedleBaseClient):
    def __init__(
        self,
        api_key: Optional[str] = os.environ.get("NEEDLE_API_KEY"),
        url: Optional[str] = None,
        search_url: Optional[str] = None,
    ):
        config = NeedleConfig(api_key, url, search_url)
        headers = {"x-api-key": config.api_key}
        super().__init__(config, headers)
        self.collections = NeedleCollections(config, headers)


class NeedleCollections(NeedleBaseClient):
    def __init__(self, config: NeedleConfig, headers: dict):
        super().__init__(config, headers)
        self.endpoint = f"{config.url}/api/v1/collections"
        self.files = NeedleCollectionsFiles(config, headers)

    def create(self, params: CreateCollectionRequest):
        resp = requests.post(
            f"{self.endpoint}", headers=self.headers, json=asdict(params)
        )
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        c = body.get("result")
        return Collection(**c)

    def get(self, collection_id: str):
        resp = requests.get(f"{self.endpoint}/{collection_id}", headers=self.headers)
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        c = body.get("result")
        return Collection(**c)

    def list(self):
        resp = requests.get(self.endpoint, headers=self.headers)
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        return [Collection(**c) for c in body.get("result")]

    def search(self, params: SearchCollectionRequest):
        endpoint = (
            f"{self.config.search_url}/api/v1/collections/{params.collection_id}/search"
        )
        resp = requests.post(endpoint, headers=self.headers, json=asdict(params))

        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        return [SearchResult(**c) for c in body.get("result")]


class NeedleCollectionsFiles(NeedleBaseClient):
    def __init__(self, config: NeedleConfig, headers: dict):
        super().__init__(config, headers)

    def add(self, params: AddFilesRequest):
        params_dict = asdict(params)
        collection_id = params_dict.pop("collection_id")
        endpoint = f"{self.config.url}/api/v1/collections/{collection_id}/files"
        resp = requests.post(f"{endpoint}", headers=self.headers, json=params_dict)
        body = resp.json()
        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)
        return [CollectionFile(**cf) for cf in body.get("result")]

    def list(self):
        raise NotImplementedError("Under construction...")
