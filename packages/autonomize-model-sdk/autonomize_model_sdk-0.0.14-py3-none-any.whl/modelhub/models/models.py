""" This module contains the Pydantic models for the ModelHub API. """
from typing import List, Optional, Dict, Union
from pydantic import BaseModel


class ResourceRequests(BaseModel):
    """
    Represents the resource requests for a stage.
    """
    cpu: Union[str, int]
    memory: str


class ResourceLimits(BaseModel):
    """
    Represents the resource limits for a stage.
    """
    cpu: Optional[Union[str, int]] = None
    memory: Optional[str] = None
    gpu: Optional[Union[str, int]] = None


class Resources(BaseModel):
    """
    Represents the resources for a stage.
    """
    requests: ResourceRequests
    limits: Optional[ResourceLimits] = None


class Toleration(BaseModel):
    """
    Represents a toleration for a stage.
    """
    key: str
    operator: str
    value: str
    effect: str


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
    resources: Optional[Resources] = None
    tolerations: Optional[List[Toleration]] = None
    node_selector: Optional[Dict[str, str]] = None


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

class SubmitPipelineRequest(BaseModel):
    """ Submit pipeline request model """
    modelhub_base_url: Optional[str] = None
    modelhub_client_id: Optional[str] = None
    modelhub_client_secret: Optional[str] = None