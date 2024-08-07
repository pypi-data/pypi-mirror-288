# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

from enum import Enum
from typing import Any, ClassVar, Dict, List

from pydantic import BaseModel, ConfigDict, SerializeAsAny, model_validator
from typing_extensions import Self


class ExecEnvironment(BaseModel):
    name: str
    version: str

    model_config = ConfigDict(from_attributes=True)


class DockerEnvironment(ExecEnvironment):
    image: str


class PythonEnvironment(ExecEnvironment):
    requirements: str


class ResourceType(str, Enum):
    unknown = "unknown"
    file = "file"
    dictionary = "dictionary"


class Resource(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

    subclass_registry: ClassVar[Dict[str, type]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        Resource.subclass_registry[cls.__name__] = cls

    class Settings:
        is_root = True


class ArtefactResource(Resource):
    resource_type: ResourceType
    model_config = ConfigDict(from_attributes=True)


class ArtefactResourceRef(Resource):
    ref_system: str
    ref_model: str
    ref_name: str

    model_config = ConfigDict(from_attributes=True)


class Model(BaseModel):
    name: str
    system: str
    env: ExecEnvironment
    inputs: List[SerializeAsAny[Resource]] = []
    outputs: List[ArtefactResource] = []

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def check_references_unique(self) -> Self:
        inp_names = {ref.name for ref in self.inputs}
        if len(inp_names) != len(self.inputs):
            raise ValueError("Input names must be unique")
        outp_names = {outp.name for outp in self.outputs}
        if len(outp_names) != len(self.outputs):
            raise ValueError("Output names must be unique")
        return self

    def __init__(self, **kwargs):
        if "inputs" in kwargs:
            for index in range(len(kwargs["inputs"])):
                current_input = kwargs["inputs"][index]
                if isinstance(current_input, dict):
                    input_keys = sorted(current_input.keys())
                    for _, subclass in Resource.subclass_registry.items():
                        registry_keys = sorted(subclass.model_fields.keys())
                        if input_keys == registry_keys:
                            current_input = subclass(**current_input)
                            break
                    kwargs["inputs"][index] = current_input
        super().__init__(**kwargs)


class ModelExecution(BaseModel):
    model: Model
    uuid: str
    execution_hash: str

    inputs: List[str]
    outputs: List[str]

    model_config = ConfigDict(from_attributes=True)


class System(BaseModel):
    name: str
    models: List[Model] = []


class ModelExecutionReference(BaseModel):
    """Reference to a model execution. Used in roxie-exec api."""

    system: str
    model: str
    execution: str


class ModelSource(BaseModel):
    """Reference to a model source. Used in roxie-exec api."""

    name: str
    uri: str


class ExecutionJob(BaseModel):
    """Reference to a running job. Used in roxie-exec api."""

    id: str
    status: str
