class ExecutionPathsMixin:
    def get_log_dir(self):
        return self.execution_path / "log"

    def get_work_dir(self):
        return self.execution_path / "work"

    def get_out_dir(self):
        return self.execution_path / "out"
