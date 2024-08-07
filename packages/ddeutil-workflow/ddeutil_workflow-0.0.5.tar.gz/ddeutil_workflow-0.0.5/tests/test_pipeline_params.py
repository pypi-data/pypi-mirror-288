from datetime import datetime

import ddeutil.workflow.pipeline as pipe


def test_pipe_params_py():
    pipeline = pipe.Pipeline.from_loader(
        name="transform_proc_mssql",
        externals={},
    )
    rs = pipeline.params["run-date"].receive("2024-01-01")
    assert rs == datetime(2024, 1, 1)
