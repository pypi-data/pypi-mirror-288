from pydantic import BaseModel


class ExecSection(BaseModel):
    test_procedure: str
    modules: str
    conda_env: str
