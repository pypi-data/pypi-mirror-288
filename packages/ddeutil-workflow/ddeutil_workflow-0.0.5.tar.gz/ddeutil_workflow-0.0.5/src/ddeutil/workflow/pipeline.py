# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import contextlib
import inspect
import itertools
import logging
import subprocess
import sys
import time
import uuid
from abc import ABC, abstractmethod
from inspect import Parameter
from pathlib import Path
from queue import Queue
from subprocess import CompletedProcess
from typing import Any, Callable, Optional, Union

from pydantic import BaseModel, Field
from pydantic.functional_validators import model_validator
from typing_extensions import Self

from .__regex import RegexConf
from .__types import DictData, DictStr
from .exceptions import TaskException
from .loader import Loader, map_params
from .utils import Params, TaskSearch, make_exec, make_registry


class BaseStage(BaseModel, ABC):
    """Base Stage Model that keep only id and name fields for the stage
    metadata. If you want to implement any custom stage, you can use this class
    to parent and implement ``self.execute()`` method only.
    """

    id: Optional[str] = Field(
        default=None,
        description=(
            "The stage ID that use to keep execution output or getting by job "
            "owner."
        ),
    )
    name: str = Field(
        description="The stage name that want to logging when start execution."
    )

    @abstractmethod
    def execute(self, params: DictData) -> DictData:
        """Execute abstraction method that action something by sub-model class.
        This is important method that make this class is able to be the stage.

        :param params: A parameter data that want to use in this execution.
        :rtype: DictData
        """
        raise NotImplementedError("Stage should implement ``execute`` method.")

    def set_outputs(self, rs: DictData, params: DictData) -> DictData:
        """Set an outputs from execution process to an input params.

        :param rs: A result data that want to extract to an output key.
        :param params: A context data that want to add output result.
        :rtype: DictData
        """
        if self.id is None:
            return params

        if "stages" not in params:
            params["stages"] = {}

        params["stages"][self.id] = {"outputs": rs}
        return params


class EmptyStage(BaseStage):
    """Empty stage that do nothing (context equal empty stage) and logging the
    name of stage only to stdout.
    """

    def execute(self, params: DictData) -> DictData:
        """Execution method for the Empty stage that do only logging out to
        stdout.

        :param params: A context data that want to add output result. But this
            stage does not pass any output.
        """
        logging.info(f"[STAGE]: Empty-Execute: {self.name!r}")
        return params


class ShellStage(BaseStage):
    """Shell stage that execute bash script on the current OS. That mean if your
    current OS is Windows, it will running bash in the WSL.
    """

    shell: str = Field(description="A shell statement that want to execute.")
    env: DictStr = Field(
        default_factory=dict,
        description=(
            "An environment variable mapping that want to set before execute "
            "this shell statement."
        ),
    )

    @contextlib.contextmanager
    def __prepare_shell(self):
        """Return context of prepared shell statement that want to execute. This
        step will write the `.sh` file before giving this file name to context.
        After that, it will auto delete this file automatic.
        """
        f_name: str = f"{uuid.uuid4()}.sh"
        f_shebang: str = "bash" if sys.platform.startswith("win") else "sh"
        with open(f"./{f_name}", mode="w", newline="\n") as f:
            f.write(f"#!/bin/{f_shebang}\n")

            for k in self.env:
                f.write(f"{k}='{self.env[k]}';\n")

            # NOTE: make sure that shell script file does not have `\r` char.
            f.write(self.shell.replace("\r\n", "\n"))

        make_exec(f"./{f_name}")

        yield [f_shebang, f_name]

        Path(f_name).unlink()

    def set_outputs(self, rs: CompletedProcess, params: DictData) -> DictData:
        """Set outputs to params"""
        # NOTE: skipping set outputs of stage execution when id does not set.
        if self.id is None:
            return params

        if "stages" not in params:
            params["stages"] = {}

        params["stages"][self.id] = {
            # NOTE: The output will fileter unnecessary keys from ``_locals``.
            "outputs": {
                "return_code": rs.returncode,
                "stdout": rs.stdout.rstrip("\n"),
            },
        }
        return params

    def execute(self, params: DictData) -> DictData:
        """Execute the Shell & Powershell statement with the Python build-in
        ``subprocess`` package.
        """
        with self.__prepare_shell() as sh:
            logging.info(f"[STAGE]: Shell-Execute: {sh}")
            rs: CompletedProcess = subprocess.run(
                sh,
                shell=False,
                capture_output=True,
                text=True,
            )
        if rs.returncode > 0:
            err: str = (
                rs.stderr.encode("utf-8").decode("utf-16")
                if "\\x00" in rs.stderr
                else rs.stderr
            )
            logging.error(f"{err}\nRunning Statement:\n---\n{self.shell}")
            raise TaskException(f"{err}\nRunning Statement:\n---\n{self.shell}")
        self.set_outputs(rs, params)
        return params


class PyStage(BaseStage):
    """Python executor stage that running the Python statement that receive
    globals nad additional variables.
    """

    run: str
    vars: DictData = Field(default_factory=dict)

    def get_vars(self, params: DictData) -> DictData:
        """Return variables"""
        rs = self.vars.copy()
        for p, v in self.vars.items():
            rs[p] = map_params(v, params)
        return rs

    def set_outputs(self, rs: DictData, params: DictData) -> DictData:
        """Set an outputs from execution process to an input params.

        :param rs: A result data that want to extract to an output key.
        :param params: A context data that want to add output result.
        :rtype: DictData
        """
        # NOTE: skipping set outputs of stage execution when id does not set.
        if self.id is None:
            return params

        if "stages" not in params:
            params["stages"] = {}

        params["stages"][self.id] = {
            # NOTE: The output will fileter unnecessary keys from ``_locals``.
            "outputs": {k: rs[k] for k in rs if k != "__annotations__"},
        }
        return params

    def execute(self, params: DictData) -> DictData:
        """Execute the Python statement that pass all globals and input params
        to globals argument on ``exec`` build-in function.

        :param params: A parameter that want to pass before run any statement.
        :type params: DictData

        :rtype: DictData
        :returns: A parameters from an input that was mapped output if the stage
            ID was set.
        """
        _globals: DictData = globals() | params | self.get_vars(params)
        _locals: DictData = {}
        try:
            exec(map_params(self.run, params), _globals, _locals)
        except Exception as err:
            raise TaskException(
                f"{err.__class__.__name__}: {err}\nRunning Statement:\n---\n"
                f"{self.run}"
            ) from None

        # NOTE: set outputs from ``_locals`` value from ``exec``.
        self.set_outputs(_locals, params)
        return params | {k: _globals[k] for k in params if k in _globals}


class TaskStage(BaseStage):
    """Task executor stage that running the Python function."""

    task: str
    args: DictData

    @staticmethod
    def extract_task(task: str) -> Callable[[], Callable[[Any], Any]]:
        """Extract Task string value to task function."""
        if not (found := RegexConf.RE_TASK_FMT.search(task)):
            raise ValueError("Task does not match with task format regex.")
        tasks: TaskSearch = TaskSearch(**found.groupdict())

        # NOTE: Registry object should implement on this package only.
        # TODO: This prefix value to search registry should dynamic with
        #   config file.
        rgt = make_registry(f"ddeutil.workflow.{tasks.path}")
        if tasks.func not in rgt:
            raise NotImplementedError(
                f"ddeutil.workflow.{tasks.path}.registries does not "
                f"implement registry: {tasks.func}."
            )

        if tasks.tag not in rgt[tasks.func]:
            raise NotImplementedError(
                f"tag: {tasks.tag} does not found on registry func: "
                f"ddeutil.workflow.{tasks.path}.registries."
                f"{tasks.func}"
            )
        return rgt[tasks.func][tasks.tag]

    def execute(self, params: DictData) -> DictData:
        """Execute the Task function."""
        task_caller = self.extract_task(self.task)()
        if not callable(task_caller):
            raise ImportError("Task caller function does not callable.")

        # NOTE: check task caller parameters
        ips = inspect.signature(task_caller)
        if any(
            k not in self.args
            for k in ips.parameters
            if ips.parameters[k].default == Parameter.empty
        ):
            raise ValueError(
                f"necessary parameters, ({', '.join(ips.parameters.keys())}), "
                f"does not set to args"
            )
        try:
            rs = task_caller(**map_params(self.args, params))
        except Exception as err:
            raise TaskException(f"{err.__class__.__name__}: {err}") from err
        self.set_outputs(rs, params)
        return params


# NOTE: Order of parsing stage data
Stage = Union[
    PyStage,
    ShellStage,
    TaskStage,
    EmptyStage,
]


class Strategy(BaseModel):
    """Strategy Model that will combine a matrix together for running the
    special job.

    Examples:
        >>> strategy = {
        ...     'matrix': {
        ...         'first': [1, 2, 3],
        ...         'second': ['foo', 'bar']
        ...     },
        ...     'include': [{'first': 4, 'second': 'foo'}],
        ...     'exclude': [{'first': 1, 'second': 'bar'}],
        ... }
    """

    fail_fast: bool = Field(default=False)
    max_parallel: int = Field(default=-1)
    matrix: dict[str, Union[list[str], list[int]]] = Field(default_factory=dict)
    include: list[dict[str, Union[str, int]]] = Field(default_factory=list)
    exclude: list[dict[str, Union[str, int]]] = Field(default_factory=list)

    @model_validator(mode="before")
    def __prepare_keys(cls, values: DictData) -> DictData:
        if "max-parallel" in values:
            values["max_parallel"] = values.pop("max-parallel")
        if "fail-fast" in values:
            values["fail_fast"] = values.pop("fail-fast")
        return values


class Job(BaseModel):
    """Job Model that is able to call a group of stages."""

    runs_on: Optional[str] = Field(default=None)
    stages: list[Stage] = Field(default_factory=list)
    needs: list[str] = Field(
        default_factory=list,
        description="A list of the job ID that want to run before this job.",
    )
    strategy: Strategy = Field(default_factory=Strategy)

    @model_validator(mode="before")
    def __prepare_keys(cls, values: DictData) -> DictData:
        if "runs-on" in values:
            values["runs_on"] = values.pop("runs-on")
        return values

    def stage(self, stage_id: str) -> Stage:
        """Return stage model that match with an input stage ID."""
        for stage in self.stages:
            if stage_id == (stage.id or ""):
                return stage
        raise ValueError(f"Stage ID {stage_id} does not exists")

    def make_strategy(self) -> list[DictStr]:
        """Return List of combination of matrix values that already filter with
        exclude and add include values.
        """
        if not (mt := self.strategy.matrix):
            return [{}]
        final: list[DictStr] = []
        for r in [
            {_k: _v for e in mapped for _k, _v in e.items()}
            for mapped in itertools.product(
                *[[{k: v} for v in vs] for k, vs in mt.items()]
            )
        ]:
            if any(
                all(r[k] == v for k, v in exclude.items())
                for exclude in self.strategy.exclude
            ):
                continue
            final.append(r)

        if not final:
            return [{}]

        for include in self.strategy.include:
            if include.keys() != final[0].keys():
                raise ValueError("Include should have the keys equal to matrix")
            if any(all(include[k] == v for k, v in f.items()) for f in final):
                continue
            final.append(include)
        return final

    def execute(self, params: DictData | None = None) -> DictData:
        """Execute job with passing dynamic parameters from the pipeline."""
        for strategy in self.make_strategy():
            params.update({"matrix": strategy})

            # IMPORTANT: The stage execution only run sequentially one-by-one.
            for stage in self.stages:
                logging.info(
                    f"[JOB]: Start execute the stage: "
                    f"{(stage.id if stage.id else stage.name)!r}"
                )

                # NOTE:
                #       I do not use below syntax because `params` dict be the
                #   reference memory pointer and it was changed when I action
                #   anything like update or re-construct this.
                #       ... params |= stage.execute(params=params)
                stage.execute(params=params)
        # TODO: We should not return matrix key to outside
        return params


class Pipeline(BaseModel):
    """Pipeline Model this is the main feature of this project because it use to
    be workflow data for running everywhere that you want. It use lightweight
    coding line to execute it.
    """

    desc: Optional[str] = Field(default=None)
    params: dict[str, Params] = Field(default_factory=dict)
    on: dict[str, DictStr] = Field(default_factory=dict)
    jobs: dict[str, Job]

    @model_validator(mode="before")
    def __prepare_params(cls, values: DictData) -> DictData:
        # NOTE: Prepare params type if it passing with only type value.
        if params := values.pop("params", {}):
            values["params"] = {
                p: (
                    {"type": params[p]}
                    if isinstance(params[p], str)
                    else params[p]
                )
                for p in params
            }
        return values

    @classmethod
    def from_loader(
        cls,
        name: str,
        externals: DictData | None = None,
    ) -> Self:
        """Create Pipeline instance from the Loader object."""
        loader: Loader = Loader(name, externals=(externals or {}))
        if "jobs" not in loader.data:
            raise ValueError("Config does not set ``jobs`` value")
        return cls(
            jobs=loader.data["jobs"],
            params=loader.data["params"],
        )

    @model_validator(mode="after")
    def job_checking_needs(self):
        return self

    def job(self, name: str) -> Job:
        """Return Job model that exists on this pipeline.

        :param name: A job name that want to get from a mapping of job models.
        :type name: str

        :rtype: Job
        :returns: A job model that exists on this pipeline by input name.
        """
        if name not in self.jobs:
            raise ValueError(f"Job {name!r} does not exists")
        return self.jobs[name]

    def execute(
        self,
        params: DictData | None = None,
        time_out: int = 60,
    ) -> DictData:
        """Execute pipeline with passing dynamic parameters to any jobs that
        included in the pipeline.

        :param params: An input parameters that use on pipeline execution.
        :param time_out: A time out in second unit that use for limit time of
            this pipeline execution.

        ---

        See Also:

            The result of execution process for each jobs and stages on this
        pipeline will keeping in dict which able to catch out with all jobs and
        stages by dot annotation.

            For example, when I want to use the output from previous stage, I
        can access it with syntax:

            ... "<job-name>.stages.<stage-id>.outputs.<key>"

        """
        params: DictData = params or {}
        if check_key := tuple(f"{k!r}" for k in self.params if k not in params):
            raise ValueError(
                f"Parameters that needed on pipeline does not pass: "
                f"{', '.join(check_key)}."
            )

        if any(p not in params for p in self.params if self.params[p].required):
            raise ValueError("Required parameter does not pass")

        # NOTE: mapping type of param before adding it to params variable.
        params: DictData = {
            "params": (
                params
                | {
                    k: self.params[k].receive(params[k])
                    for k in params
                    if k in self.params
                }
            ),
            "jobs": {},
        }

        # NOTE: create a job queue that keep the job that want to running after
        #   it dependency condition.
        jq = Queue()
        for job_id in self.jobs:
            jq.put(job_id)

        ts: float = time.monotonic()
        not_time_out_flag = True

        # IMPORTANT: The job execution can run parallel and waiting by needed.
        while not jq.empty() and (
            not_time_out_flag := ((time.monotonic() - ts) < time_out)
        ):
            job_id: str = jq.get()
            logging.info(f"[PIPELINE]: Start execute the job: {job_id!r}")
            job: Job = self.jobs[job_id]

            # TODO: Condition on ``needs`` of this job was set. It should create
            #   multithreading process on this step.
            #   But, I don't know how to handle changes params between each job
            #   execution while its use them together.
            #   ---
            #   >>> import multiprocessing
            #   >>> with multiprocessing.Pool(processes=3) as pool:
            #   ...     results = pool.starmap(merge_names, ('', '', ...))
            #
            if any(params["jobs"].get(need) for need in job.needs):
                jq.put(job_id)

            job.execute(params=params)
            params["jobs"][job_id] = {
                "stages": params.pop("stages", {}),
                "matrix": params.pop("matrix", {}),
            }
        if not not_time_out_flag:
            raise RuntimeError("Execution of pipeline was time out")
        return params
