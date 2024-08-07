""" This module contains the Pydantic models for the ModelHub API. """
from typing import List, Optional
from pydantic import BaseModel


class Stage(BaseModel):
    """
    Represents a stage in a pipeline.
    """

    name: str
    type: str
    params: Optional[dict] = None
    depends_on: Optional[List[str]] = []
    script: Optional[str] = None
    requirements: Optional[str] = None
    resources: Optional[dict] = None


class PipelineCreateRequest(BaseModel):
    """
    Represents a request to create a pipeline.
    """

    name: str
    description: Optional[str] = None
    experiment_id: str
    dataset_id: str
    image_tag: str
    stages: List[Stage]


class Pipeline(BaseModel):
    """
    Represents a pipeline.
    """

    pipeline_id: str
    name: str
    description: Optional[str] = None
    experiment_id: str
    dataset_id: str
    image_tag: str
    stages: List[Stage]
    status: Optional[str] = None
    workflows: Optional[List[dict]] = []
