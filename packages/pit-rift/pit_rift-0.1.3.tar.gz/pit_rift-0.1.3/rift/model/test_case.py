import logging
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

from rift.model.exec_section import ExecSection
from rift.model.git_section import GitSection

logger = logging.getLogger("test_case")


class TestCase(BaseModel):
    path: Path
    environment: dict = Field(alias="ENVIRONMENT")
    exec: ExecSection = Field(alias="EXEC")
    repositories: List[GitSection] = Field(alias="REPOSITORIES")

    @property
    def name(self):
        return self.path.name

    @property
    def procedure_name(self):
        return self.exec.test_procedure

    def environ(self) -> dict:
        return {
            **self.environment,
            **self.exec.model_dump(by_alias=True)
        }
