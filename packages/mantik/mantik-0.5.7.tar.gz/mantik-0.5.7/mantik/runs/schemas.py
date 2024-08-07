import dataclasses
import pathlib
import typing as t
import uuid

import mantik.config


@dataclasses.dataclass
class RunConfiguration:
    name: str
    experiment_repository_id: uuid.UUID
    code_repository_id: uuid.UUID
    branch: t.Optional[str]
    commit: t.Optional[str]
    data_repository_id: t.Optional[uuid.UUID]
    mlflow_mlproject_file_path: str
    entry_point: str
    mlflow_parameters: dict
    backend_config: dict
    mlflow_run_id: t.Optional[uuid.UUID] = None
    data_branch: t.Optional[str] = None
    data_commit: t.Optional[str] = None

    def to_post_payload(self) -> dict:
        return {
            "name": self.name,
            "experimentRepositoryId": str(self.experiment_repository_id),
            "codeRepositoryId": str(self.code_repository_id),
            "branch": self.branch,
            "commit": self.commit,
            "dataRepositoryId": str(self.data_repository_id)
            if self.data_repository_id is not None
            else None,
            "dataBranch": self.data_branch if self.data_branch else None,
            "dataCommit": self.data_commit if self.data_commit else None,
            "mlflowMlprojectFilePath": self.mlflow_mlproject_file_path,
            "entryPoint": self.entry_point,
            "mlflowParameters": self.mlflow_parameters,
            "backendConfig": self.backend_config,
            "mlflowRunId": str(self.mlflow_run_id),
        }


@dataclasses.dataclass
class RemoteRunConfiguration:
    name: str
    experiment_repository_id: uuid.UUID
    code_repository_id: uuid.UUID
    branch: t.Optional[str]
    commit: t.Optional[str]
    data_repository_id: t.Optional[uuid.UUID]
    mlflow_mlproject_file_path: str
    entry_point: str
    mlflow_parameters: dict
    backend_config: t.Union[pathlib.Path, str, dict]
    connection_id: t.Optional[uuid.UUID]
    compute_budget_account: t.Optional[str]
    data_branch: t.Optional[str] = None
    data_commit: t.Optional[str] = None

    def to_post_payload(self) -> dict:
        # TODO: the validating has to be fixed
        #  currently it expects all file locally,
        #  probably it just needs to be reduced
        # mantik.config.validate.ProjectValidator(
        #     mlproject_path=self.mlflow_mlproject_file_path,
        #     config=self.backend_config,
        #     mlflow_parameters=self.mlflow_parameters,
        #     entry_point=self.entry_point,
        # ).validate()
        if isinstance(self.backend_config, dict):
            config = self.backend_config
        else:
            config = mantik.config.read.read_config(self.backend_config)

        return {
            "name": self.name,
            "experimentRepositoryId": str(self.experiment_repository_id),
            "codeRepositoryId": str(self.code_repository_id),
            "branch": self.branch,
            "commit": self.commit,
            "dataRepositoryId": str(self.data_repository_id)
            if self.data_repository_id is not None
            else None,
            "dataBranch": self.data_branch if self.data_branch else None,
            "dataCommit": self.data_commit if self.data_commit else None,
            "connectionId": str(self.connection_id),
            "computeBudgetAccount": self.compute_budget_account,
            "mlflowMlprojectFilePath": self.mlflow_mlproject_file_path,
            "entryPoint": self.entry_point,
            "mlflowParameters": self.mlflow_parameters,
            "backendConfig": config,
        }
