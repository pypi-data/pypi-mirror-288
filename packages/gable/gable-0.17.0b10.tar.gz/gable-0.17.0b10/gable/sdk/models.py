import re
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from gable.openapi import ContractSpec, EnforcementLevel, Status
from pydantic import BaseModel


# https://trino.io/docs/current/language/types.html
class TrinoDataType(str, Enum):
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    INT = "INT"
    TINYINT = "TINYINT"
    SMALLINT = "SMALLINT"
    BIGINT = "BIGINT"
    REAL = "REAL"
    DOUBLE = "DOUBLE"
    DECIMAL = "DECIMAL"
    VARCHAR = "VARCHAR"
    CHAR = "CHAR"
    VARBINARY = "VARBINARY"
    JSON = "JSON"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    TIME = "TIME"
    TIME_WITH_TIME_ZONE = "TIME_WITH_TIME_ZONE"
    TIMESTAMP_WITH_TIME_ZONE = "TIMESTAMP_WITH_TIME_ZONE"
    INTERVAL_YEAR_TO_MONTH = "INTERVAL_YEAR_TO_MONTH"
    INTERVAL_DAY_TO_SECOND = "INTERVAL_DAY_TO_SECOND"
    ARRAY = "ARRAY"
    MAP = "MAP"
    ROW = "ROW"
    UUID = "UUID"
    IPADDRESS = "IPADDRESS"

    def __call__(self, *args):
        if self == TrinoDataType.DECIMAL and not args:
            raise ValueError("DECIMAL type requires at least the precision argument")
        if self in {
            TrinoDataType.DECIMAL,
            TrinoDataType.VARCHAR,
            TrinoDataType.CHAR,
            TrinoDataType.TIME,
            TrinoDataType.TIME_WITH_TIME_ZONE,
            TrinoDataType.TIMESTAMP,
            TrinoDataType.TIMESTAMP_WITH_TIME_ZONE,
        }:
            return self, args
        raise TypeError(f"{self.value} does not support parameters")

    @staticmethod
    def parse(data_type: str):
        data_type = data_type.upper()
        args = None
        # Check for args like DECIMAL(10, 2)
        match = re.match(r"([A-Z\s]+)(\(.+\))", data_type)
        if match:
            data_type = match.group(1)
            args = [int(a.strip()) for a in match.group(2).strip("()").split(",")]
        # "TIME WITH TIME ZONE " -> "TIME_WITH_TIME_ZONE"
        data_type = re.sub(r"\s+", "_", data_type.strip())
        if args:
            return TrinoDataType(data_type)(*args)
        return TrinoDataType(data_type)


class GitMetadata(BaseModel):
    gitHash: str
    gitRepo: str
    gitUser: str
    mergedAt: datetime
    filePath: str
    reviewers: List[str]


class ExternalContractInput(BaseModel):
    version: Optional[str]
    status: Status
    enforcementLevel: Optional[EnforcementLevel]
    contractSpec: ContractSpec
    gitMetadata: Optional[GitMetadata]


class ContractPublishResponse(BaseModel):
    id: UUID
    message: Optional[str]
    success: bool
