# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

import pathlib
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Type

from typing_extensions import Self

from pymbse.commons.schemas import ExecEnvironment


class ToolAdapter(ABC):
    registry: Dict[str, Dict[str, Type[Self]]] = {}

    def __init_subclass__(cls, tool_name: str, **kwargs):
        super().__init_subclass__(**kwargs)
        if tool_name in cls.registry:
            raise ValueError(
                f"Execution environment for {tool_name} already registered in adapter. Duplicate?"
            )
        cls.registry[tool_name] = {"*": cls}

    @abstractmethod
    def __init__(self, exec_environment: ExecEnvironment):
        self.exec_environment = exec_environment

    @abstractmethod
    def execute_tool(
        self,
        execution_env: ExecEnvironment,
        io_dir: pathlib.Path,
        input_files: List[pathlib.Path],
    ) -> Tuple[int, List[Tuple[str, pathlib.Path]]]:
        """
        Execute tool

        :param execution_env: The execution environment
        :type execution_env: ExecEnvironment
        :param io_dir: The input/output directory
        :type io_dir: pathlib.Path
        :param input_files: List of input files
        :type input_files: List[pathlib.Path]
        :return: A Tuple of io_dir and Inputs
        :rtype: List[Tuple[str, pathlib.Path]]
        """
        raise NotImplementedError()

    @classmethod
    def get_adapter(cls, execution_env: ExecEnvironment) -> Self:
        if execution_env.name not in cls.registry:
            raise ValueError(
                f"Execution environment for {execution_env.name} not registered in adapter. Possible values: {','.join(cls.registry.keys())}"
            )
        if execution_env.version in cls.registry[execution_env.name]:
            return cls.registry[execution_env.name][execution_env.version](
                execution_env
            )

        return cls.registry[execution_env.name]["*"](execution_env)
