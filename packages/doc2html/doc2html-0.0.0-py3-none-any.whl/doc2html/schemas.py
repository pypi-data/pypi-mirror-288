from pydantic import BaseModel
from typing import Any, Union

from . import config as cfg


class HealthcheckOutput(BaseModel):
    """Schema of /healthcheck output"""
    status: str = "ok"
    service: str = cfg.TRANSFORM_SERVICE_NAME
    version: str = cfg.TRANSFORM_SERVICE_VERSION
    info: str = cfg.TRANSFORM_SERVICE_INFO


class TransformOutput(BaseModel):
    """Schema of /transform_format output"""
    status: str = 'ok'
    data: Union[str, bytes]
    runtime: float
