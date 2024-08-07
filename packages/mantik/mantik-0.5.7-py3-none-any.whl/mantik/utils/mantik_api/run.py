import dataclasses
import logging
import typing as t
import uuid

import mantik.utils.mantik_api.client as client
import mantik.utils.other as other_utils

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class GPUInfo:
    name: str
    id: str
    driver: str
    total_memory: str

    @classmethod
    def from_dict(cls, _dict):
        return cls(
            name=_dict["name"],
            id=_dict["id"],
            driver=_dict["driver"],
            total_memory=_dict["totalMemory"],
        )

    def to_json(self):
        return {
            "name": self.name,
            "id": self.id,
            "driver": self.driver,
            "totalMemory": self.total_memory,
        }


@dataclasses.dataclass
class RunInfrastructure:
    os: str
    cpu_cores: int
    gpu_count: int
    gpu_info: t.List[GPUInfo]
    hostname: str
    memory_gb: str
    platform: str
    processor: str
    python_version: str
    python_executable: str

    def to_json(self):
        return {
            "os": self.os,
            "cpuCores": self.cpu_cores,
            "gpuCount": self.gpu_count,
            "gpuInfo": [_gpu.to_json() for _gpu in self.gpu_info],
            "hostname": self.hostname,
            "memoryGb": self.memory_gb,
            "platform": self.platform,
            "processor": self.processor,
            "pythonVersion": self.python_version,
            "pythonExecutable": self.python_executable,
        }

    @classmethod
    def from_system(cls):
        _gpu_info = other_utils.get_gpu_info()
        return cls(
            os=other_utils.get_os(),
            cpu_cores=other_utils.get_cpu_cores(),
            gpu_count=len(_gpu_info),
            gpu_info=[GPUInfo.from_dict(_gpu) for _gpu in _gpu_info],
            hostname=other_utils.get_hostname(),
            memory_gb=other_utils.get_memory_gb(),
            platform=other_utils.get_platform(),
            processor=other_utils.get_processor(),
            python_version=other_utils.get_python_version(),
            python_executable=other_utils.get_python_executable(),
        )


def submit_run(project_id: uuid.UUID, submit_run_data: dict, token: str):
    endpoint = f"/projects/{project_id}/runs"
    response = client.send_request_to_mantik_api(
        method="POST", data=submit_run_data, url_endpoint=endpoint, token=token
    )
    logger.info("Run has been successfully submitted")
    return response


def save_run(project_id: uuid.UUID, run_data: dict, token: str):
    endpoint = f"/projects/{project_id}/runs"
    response = client.send_request_to_mantik_api(
        method="POST",
        data=run_data,
        url_endpoint=endpoint,
        token=token,
        query_params={"submit": False},
    )
    logger.info("Run has been successfully saved")
    return response


def update_run_status(
    project_id: uuid.UUID, run_id: uuid.UUID, status: str, token: str
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/status"
    response = client.send_request_to_mantik_api(
        method="PUT", data=status, url_endpoint=endpoint, token=token
    )
    logger.info("Run status has been successfully updated")
    return response


def update_logs(
    project_id: uuid.UUID, run_id: uuid.UUID, logs: str, token: str
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/logs"
    response = client.send_request_to_mantik_api(
        method="PUT", data=logs, url_endpoint=endpoint, token=token
    )
    logger.info("Run logs has been successfully updated")
    return response


def get_download_artifact_url(
    project_id: uuid.UUID, run_id: uuid.UUID, token: str
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/artifacts"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    logger.info("Artifacts' download url successfully fetched")
    return response.json()["url"]


def update_run_infrastructure(
    project_id: uuid.UUID,
    run_id: uuid.UUID,
    infrastructure: RunInfrastructure,
    token: str,
):
    endpoint = f"/projects/{project_id}/runs/{run_id}/infrastructure"
    response = client.send_request_to_mantik_api(
        method="PUT",
        data=infrastructure.to_json(),
        url_endpoint=endpoint,
        token=token,
    )
    logger.info("Run infrastructure has been successfully updated")
    return response
