# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

import pathlib
import tempfile
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Type

import requests
from typing_extensions import Self

from pymbse.commons.schemas import ModelExecution, ModelExecutionReference, ModelSource


class ModelSourceAdapter(ABC):
    registry: Dict[str, Type[Self]] = {}

    def __init_subclass__(cls, io_name: str, **kwargs):
        super().__init_subclass__(**kwargs)
        if io_name in cls.registry:
            raise ValueError(
                f"ModelSource for {io_name} already registered in adapter. Duplicate?"
            )
        cls.registry[io_name] = cls

    @abstractmethod
    def __init__(self, mod_source: ModelSource):
        self.mod_source = mod_source

    @abstractmethod
    def load_inputs(
        self, exection_ref: ModelExecutionReference
    ) -> Tuple[pathlib.Path, List[pathlib.Path]]:
        raise NotImplementedError()

    @abstractmethod
    def store_outputs(
        self,
        execution_reference: ModelExecutionReference,
        outputs: List[Tuple[str, pathlib.Path]],
    ) -> None:
        raise NotImplementedError()

    @classmethod
    def get_adapter(cls, mod_source: ModelSource) -> Self:
        if mod_source.name not in cls.registry:
            raise ValueError(
                f"ModelSource for {mod_source.name} not registered in adapter. Possible values: {','.join(cls.registry.keys())}"
            )

        return cls.registry[mod_source.name](mod_source)


class PymbseCacheFileAdapter(ModelSourceAdapter, io_name="pymbse-cache"):
    def __init__(self, mod_source: ModelSource):
        super().__init__(mod_source)
        self.uri = mod_source.uri
        self.temp_directory = tempfile.TemporaryDirectory()
        self.session = requests.Session()

    def __del__(self):
        self.temp_directory.cleanup()

    def load_inputs(
        self, execution_reference: ModelExecutionReference
    ) -> Tuple[pathlib.Path, List[pathlib.Path]]:
        # load execution
        execution_url = (
            self.uri
            + f"/systems/{execution_reference.system}/models/{execution_reference.model}/executions/{execution_reference.execution}"
        )
        tmp_path = pathlib.Path(self.temp_directory.name)  # type: ignore
        inputs = []
        response = self.session.get(execution_url)
        response.raise_for_status()
        model_execution = ModelExecution(**response.json())
        for input in model_execution.inputs:
            response = self.session.get(execution_url + f"/inputs/{input}")
            response.raise_for_status()
            input_name = tmp_path / input
            with open(input_name, "wb") as f:
                f.write(response.content)
            inputs.append(input_name)

        return (tmp_path, inputs)

    def store_outputs(
        self,
        execution_reference: ModelExecutionReference,
        outputs: List[Tuple[str, pathlib.Path]],
    ) -> None:
        execution_url = (
            self.uri
            + f"/systems/{execution_reference.system}/models/{execution_reference.model}/executions/{execution_reference.execution}"
        )
        for name, out_path in outputs:
            self.session.post(
                execution_url + f"/outputs/{name}",
                files={"file": open(out_path, "rb")},
            )

        # lock execution output
        result = self.session.post(execution_url + "/lock_outputs")
        result.raise_for_status()
