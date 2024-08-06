from pydantic import BaseModel
from typing import List, Optional


class Stage(BaseModel):
    name: str
    type: str
    params: Optional[dict] = None
    depends_on: Optional[List[str]] = []
    script: Optional[str] = None
    requirements: Optional[str] = None
    resources: Optional[dict] = None


class PipelineCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    experiment_id: str
    dataset_id: str
    image_tag: str
    stages: List[Stage]


class Pipeline(BaseModel):
    pipeline_id: str
    name: str
    description: Optional[str] = None
    experiment_id: str
    dataset_id: str
    image_tag: str
    stages: List[Stage]
    status: Optional[str] = None
    workflows: Optional[List[dict]] = []
