import json
import logging
import uuid
from typing import List, Dict, Optional

from astra_assistants.tools.tool_interface import ToolInterface
from cassandra.cqltypes import cqltype_to_python
from pydantic import BaseModel, Field, validator

from datastore.providers.cassandra_util import CassandraType

logger = logging.getLogger(__name__)

class Column(BaseModel):
    name: str = Field(..., description="Name of the column")
    type: str = Field(..., description="Cassandra data type of the column. Must be either a base type: \nascii, bigint, blob, boolean, counter, date, decimal, double, duration, float, inet, int, smallint, text, time, timestamp, timeuuid, tinyint, uuid, varchar, varint\nOr a collection where text could be replaced with a base type set<text>, list<text>, map<text, text>\n or finally a vector type which is always float and takes the number of dimensions: vector<float, 1024>")
    @validator('type')
    def validate_type(cls, v):
        try:
            cls._validate_cassandra_type(v)
        except ValueError:
            raise ValueError(f"Unsupported type {v}. Must be a valid Cassandra type.")
        return v

    @staticmethod
    def _validate_cassandra_type(type_str: str):
        python_type = cqltype_to_python(type_str)
        if len(python_type) > 1:
            if python_type[0] == 'set' or python_type[0] == 'list':
                Column._validate_cassandra_type(python_type[1][0])
            elif python_type[0] == 'map':
                Column._validate_cassandra_type(python_type[1][0])
                Column._validate_cassandra_type(python_type[1][1])
            elif python_type[0] == 'vector':
                # No need for further validation; vectors are lists of floats
                return
            else:
                raise ValueError(f"Unsupported collection type {type_str}")
        elif python_type[0] not in {item.value for item in CassandraType}:
            raise ValueError(f"Unsupported type {type_str}")


class DDLModel(BaseModel):
    thoughts: Optional[str] = Field(..., description="The message to be described to the user explaining why the DDL statement is being proposed.")
    keyspace_name: str = Field(..., description="Name of the keyspace")
    table_name: str = Field(..., description="Name of the table")
    columns: List[Column] = Field(..., description="List of columns with their types, this includes partition key and clustering columns")
    partition_key: List[str] = Field(..., description="List of partition key column names, *NOTE ORDER MATTERS*")
    clustering_columns: List[str] = Field(..., description="List of clustering column column names, *NOTE ORDER MATTERS*")

    def to_string(self, keyspace_name: str = None, table_name: str = None):
        if keyspace_name is not None:
            self.keyspace_name = keyspace_name
        if table_name is not None:
            self.table_name = table_name
        ddl_statement = f"CREATE TABLE {self.keyspace_name}.{self.table_name} (\n" + \
            ",\n".join([f"    {column.name} {column.type}" for column in self.columns]) + \
            ",\n    PRIMARY KEY ((" + \
            ", ".join(self.partition_key) + ")"
        if len(self.clustering_columns) > 0:
            ddl_statement += ", " + ", ".join(self.clustering_columns)
        ddl_statement += ")\n);"
        return ddl_statement

class MakeDDLTool(ToolInterface):
    def __init__(self, ddl_list: List):
        self.ddl_cache = ddl_list

    def call(self, arguments: DDLModel) -> str:
        ddl_object = {
            "output": arguments,
            "design_id": uuid.uuid4()
        }
        self.ddl_cache.append(ddl_object)
        return ddl_object