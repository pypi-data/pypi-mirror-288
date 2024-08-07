# SPDX-FileCopyrightText: 2024 CERN
#
# SPDX-License-Identifier: BSD-4-Clause

from typing import Any, Dict

from celery import shared_task

from pymbse.commons.schemas import ExecEnvironment, ModelExecutionReference, ModelSource
from pymbse.exec.io import ModelSourceAdapter
from pymbse.exec.tools import ToolAdapter


@shared_task
def execute_model(
    exec_ref=Dict[str, Any],
    exec_env=Dict[str, Any],
    mod_source=Dict[str, Any],
    **kwargs,
) -> None:
    execution_reference: ModelExecutionReference = (
        ModelExecutionReference.model_validate(exec_ref)
    )
    execution_env: ExecEnvironment = ExecEnvironment.model_validate(exec_env)
    model_source: ModelSource = ModelSource.model_validate(mod_source)

    source_adapter = ModelSourceAdapter.get_adapter(model_source)
    tool_adapter = ToolAdapter.get_adapter(execution_env)

    exec_dir, inputs = source_adapter.load_inputs(execution_reference)
    return_code, outputs = tool_adapter.execute_tool(execution_env, exec_dir, inputs)
    source_adapter.store_outputs(execution_reference, outputs)

    if return_code != 0:
        raise Exception(f"Tool exited with code {return_code}")
