from pydantic import BaseModel
from enum import Enum
from datetime import date, time, datetime, timedelta
from typing import List, Dict, Type, Any, Union
from cassandra.cqltypes import cqltype_to_python
import uuid


class CassandraType(Enum):
    ASCII = "ascii"
    BIGINT = "bigint"
    BLOB = "blob"
    BOOLEAN = "boolean"
    COUNTER = "counter"
    DATE = "date"
    DECIMAL = "decimal"
    DOUBLE = "double"
    DURATION = "duration"
    FLOAT = "float"
    INET = "inet"
    INT = "int"
    SMALLINT = "smallint"
    TEXT = "text"
    TIME = "time"
    TIMESTAMP = "timestamp"
    TIMEUUID = "timeuuid"
    TINYINT = "tinyint"
    UUID = "uuid"
    VARCHAR = "varchar"
    VARINT = "varint"
    SET = "set"
    MAP = "map"
    LIST = "list"
    VECTOR = "vector"


class PydanticType(BaseModel):
    type_str: str

    @property
    def python_type(self) -> Type[Any]:
        python_type = cqltype_to_python(self.type_str)
        if len(python_type) > 1:
            if python_type[0] == CassandraType.SET.value or python_type[0] == CassandraType.LIST.value:
                return List[get_pydantic_type(python_type[1][0])]
            if python_type[0] == CassandraType.MAP.value:
                return Dict[get_pydantic_type(python_type[1][0]), get_pydantic_type(python_type[1][1])]
            if python_type[0] == CassandraType.VECTOR.value:
                return List[float]
            else:
                print(f"Unsupported type {self.type_str}")
                return Any
        else:
            return self._simple_python_type(python_type[0])

    @staticmethod
    def _simple_python_type(cassandra_type: str) -> Type[Any]:
        return {
            CassandraType.ASCII.value: str,
            CassandraType.BIGINT.value: int,
            CassandraType.BLOB.value: bytes,
            CassandraType.BOOLEAN.value: bool,
            CassandraType.COUNTER.value: int,
            CassandraType.DATE.value: date,
            CassandraType.DECIMAL.value: float,
            CassandraType.DOUBLE.value: float,
            CassandraType.DURATION.value: timedelta,
            CassandraType.FLOAT.value: float,
            CassandraType.INET.value: str,
            CassandraType.INT.value: int,
            CassandraType.SMALLINT.value: int,
            CassandraType.TEXT.value: str,
            CassandraType.TIME.value: time,
            CassandraType.TIMESTAMP.value: datetime,
            CassandraType.TIMEUUID.value: uuid.UUID,
            CassandraType.TINYINT.value: int,
            CassandraType.UUID.value: uuid.UUID,
            CassandraType.VARCHAR.value: str,
            CassandraType.VARINT.value: int,
        }.get(cassandra_type, Any)

    @property
    def openapi_type(self) -> Dict[str, Union[str, Dict]]:
        python_type = cqltype_to_python(self.type_str)
        if len(python_type) > 1:
            if python_type[0] == CassandraType.SET.value or python_type[0] == CassandraType.LIST.value:
                return {"type": "array", "items": self._simple_openapi_type(python_type[1][0])}
            if python_type[0] == CassandraType.MAP.value:
                return {
                    "type": "object",
                    "additionalProperties": {
                        "type": self._simple_openapi_type(python_type[1][1])["type"]
                    }
                }
            if python_type[0] == CassandraType.VECTOR.value:
                return {"type": "array", "items": {"type": "number", "format": "float"}}
            else:
                print(f"Unsupported type {self.type_str}")
                return {"type": "string"}
        else:
            return self._simple_openapi_type(python_type[0])

    @staticmethod
    def _simple_openapi_type(cassandra_type: str) -> Dict[str, Union[str, Dict]]:
        return {
            CassandraType.ASCII.value: {"type": "string"},
            CassandraType.BIGINT.value: {"type": "integer", "format": "int64"},
            CassandraType.BLOB.value: {"type": "string", "format": "byte"},
            CassandraType.BOOLEAN.value: {"type": "boolean"},
            CassandraType.COUNTER.value: {"type": "integer", "format": "int64"},
            CassandraType.DATE.value: {"type": "string", "format": "date"},
            CassandraType.DECIMAL.value: {"type": "number", "format": "double"},
            CassandraType.DOUBLE.value: {"type": "number", "format": "double"},
            CassandraType.DURATION.value: {"type": "string"},
            CassandraType.FLOAT.value: {"type": "number", "format": "float"},
            CassandraType.INET.value: {"type": "string"},
            CassandraType.INT.value: {"type": "integer", "format": "int32"},
            CassandraType.SMALLINT.value: {"type": "integer", "format": "int32"},
            CassandraType.TEXT.value: {"type": "string"},
            CassandraType.TIME.value: {"type": "string", "format": "time"},
            CassandraType.TIMESTAMP.value: {"type": "string", "format": "date-time"},
            CassandraType.TIMEUUID.value: {"type": "string", "format": "uuid"},
            CassandraType.TINYINT.value: {"type": "integer", "format": "int32"},
            CassandraType.UUID.value: {"type": "string", "format": "uuid"},
            CassandraType.VARCHAR.value: {"type": "string"},
            CassandraType.VARINT.value: {"type": "integer", "format": "int64"},
        }.get(cassandra_type, {"type": "string"})


def get_pydantic_type(type_str: str) -> Type[Any]:
    return PydanticType(type_str=type_str).python_type

def get_openapi_type(type_str: str) -> Dict[str, Union[str, Dict]]:
    return PydanticType(type_str=type_str).openapi_type

def python_to_cassandra(py_type: Type[Any]) -> str:
    return {
        str: CassandraType.TEXT.value,
        int: CassandraType.INT.value,
        bytes: CassandraType.BLOB.value,
        bool: CassandraType.BOOLEAN.value,
        date: CassandraType.DATE.value,
        float: CassandraType.DOUBLE.value,
        timedelta: CassandraType.DURATION.value,
        time: CassandraType.TIME.value,
        datetime: CassandraType.TIMESTAMP.value,
        uuid.UUID: CassandraType.UUID.value,
        List: CassandraType.LIST.value,
        Dict: CassandraType.MAP.value,
    }.get(py_type, CassandraType.TEXT.value)