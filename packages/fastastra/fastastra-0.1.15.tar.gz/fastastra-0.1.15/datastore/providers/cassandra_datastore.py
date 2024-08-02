import os
import time
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple
from cassandra import ConsistencyLevel, AlreadyExists
import zipfile
import json
import requests
from cassandra.policies import RetryPolicy
from fastapi import Depends, Request, Response, HTTPException
from loguru import logger
from pydantic import BaseModel, create_model

from datastore.datastore import DataStore
from cassandra.cluster import Cluster, NoHostAvailable
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement, dict_factory, named_tuple_factory, UNSET_VALUE

from datastore.providers.cassandra_util import get_pydantic_type, get_openapi_type
from services.openai import get_embeddings

CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST", "localhost")
CASSANDRA_PORT = int(os.environ.get("CASSANDRA_PORT", 9042))
CASSANDRA_KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE", "default_keyspace")
CASSANDRA_USER = 'token'


class Payload(BaseModel):
    args: Dict[str, Any]

# class that implements the DataStore interface for Cassandra Datastore provider
class CassandraDataStore(DataStore):
    def __init__(self):
        self.app = None
        # no longer create session on init, since we need a session per user
        # self.client = self.create_db_client()
        pass

    def create_db_client(self, token, dbid):
        self.client = CassandraClient(token, dbid)
        return self.client

    def getSubApp(self):
        return self.app

    def setupSession(self, token, dbid):
        self.dbid = dbid
        self.client = self.create_db_client(token, dbid)
        return self.client
    def setupEndpoints(self, app):
        self.app = app
        keyspaces = self.client.get_keyspaces()

        #def create_get_keyspaces_endpoint():
        #    async def endpoint() -> List[str]:
        #        rows = await self.client.get_keyspaces_async()
        #        return rows
        #    return endpoint

        #app.add_api_route(path="/keyspaces", endpoint=create_get_keyspaces_endpoint(), methods=["GET"], operation_id=f"get_keyspaces", openapi_extra={"x-fern-sdk-method-name": "get_keyspaces", "x-fern-sdk-group-name": "manage", "summary": f"Get Keyspaces"})

        for keyspace in keyspaces:

            def create_get_tables_endpoint(keyspace):
                async def endpoint() -> List[str]:
                    rows = await self.client.get_tables_async(keyspace)
                    return rows
                return endpoint

            app.add_api_route(path=f"/{keyspace}/tables", endpoint=create_get_tables_endpoint(keyspace), methods=["GET"], operation_id=f"get_tables", openapi_extra={"x-fern-sdk-method-name": "get_tables", "x-fern-sdk-group-name": ["manage", keyspace], "summary": f"Get Tables"})

            tables = self.client.get_tables(keyspace)

            def create_select_all_endpoint(keyspace: str, table: str, response_model: BaseModel):
                async def endpoint() -> List[response_model]:
                    rows = await self.client.select_all_from_table_async(keyspace, table)
                    return rows

                return endpoint


            def create_get_columns_endpoint(keyspace, table):
                async def endpoint() -> List[Dict[str, Any]]:
                    rows = await self.client.get_columns_async(keyspace, table)
                    return rows

                return endpoint

            def create_select_by_pk_endpoint(keyspace: str, table: str, partition_keys: List[Dict[str, Any]], response_model : BaseModel):
                class PathParams:
                    def __init__(self, keys: Dict[str, Any]):
                        self.keys = keys

                    async def __call__(self, request: Request) -> Dict[str, Any]:
                        return {key['column_name']: request.path_params[key['column_name']] for key in self.keys}

                async def endpoint(args: Dict[str, str] = Depends(PathParams(partition_keys))) -> List[response_model]:
                    rows = await self.client.selectFromTableByPK(keyspace, table, partition_keys, args)
                    return [response_model(**row) for row in rows]
                return endpoint

            def create_select_by_cc_endpoint(keyspace: str, table: str, partitionKeys: List[Dict[str, Any]], clustering_columns: List[Dict[str, Any]], response_model: BaseModel):
                async def endpoint(payload: Payload) -> List[response_model]:
                    rows = await self.client.selectFromTableByPK(keyspace, table, partitionKeys + clustering_columns, payload.args)
                    return rows
                return endpoint


            def create_select_by_index_endpoint(keyspace, table, indexed_columns, vector_indexes, partition_keys, columns, response_model: BaseModel):
                async def endpoint(payload: Payload) -> List[response_model]:
                    try:
                        rows = await self.client.selectFromTableByIndex(
                            keyspace=keyspace,
                            table=table,
                            indexed_columns=indexed_columns,
                            vector_indexes=vector_indexes,
                            partition_keys=partition_keys,
                            columns=columns,
                            args=payload.args
                        )
                        return rows
                    except Exception as e:
                        message_json = {"message": str(e)}
                        raise HTTPException(status_code=500, detail=json.dumps(message_json))

                return endpoint

            def create_insert_endpoint(keyspace: str, table: str, response_model : BaseModel):
                async def endpoint(request_object: response_model) -> Response:
                    await self.client.upsert_table_from_dict_async(keyspace, table, request_object.dict())
                    content = {"success": True}
                    return Response(status_code=200, content=json.dumps(content))
                return endpoint


            for table in tables:
                model_name = ''.join(word.capitalize() for word in keyspace.split('_'))
                model_name += ''.join(word.capitalize() for word in table.split('_'))
                model_name += "Model"

                columns = self.client.get_columns(keyspace, table)
                model_fields: Dict[str, Tuple[Any, Any]] = {}
                for col in columns:
                    if col['kind'] != 'partition_key' and col['kind'] != 'clustering':
                        model_fields[col["column_name"]] = (Optional[get_pydantic_type(col["type"])], None)
                    else:
                        model_fields[col["column_name"]] = (get_pydantic_type(col["type"]), ...)

                ResponseModel = create_model(model_name, **model_fields)

                route_path=f"/{keyspace}/{table}"
                endpoint=create_insert_endpoint(keyspace, table, ResponseModel)
                app.add_api_route(path=route_path, endpoint=endpoint, methods=["POST"], operation_id=f"{keyspace}_{table}_create", openapi_extra={"x-fern-sdk-method-name": "create", "x-fern-sdk-group-name":[keyspace, table], "summary": f"Create: {table}"})


                route_path=f"/{keyspace}/{table}/columns"
                endpoint=create_get_columns_endpoint(keyspace, table)
                app.add_api_route(path=route_path, endpoint=endpoint, methods=["GET"], operation_id=f"{keyspace}_{table}_columns", openapi_extra={"x-fern-sdk-method-name": "columns", "x-fern-sdk-group-name":[keyspace, table], "summary": f"Get Columns: {table}"})

                route_path=f"/{keyspace}/{table}"
                endpoint=create_select_all_endpoint(keyspace, table, ResponseModel)
                app.add_api_route(path=route_path, endpoint=endpoint, methods=["GET"], operation_id=f"{keyspace}_{table}_list", openapi_extra={"x-fern-sdk-method-name": "list", "x-fern-sdk-group-name":[keyspace, table], "summary": f"List: {table}"})

                # filter columns that are partition keys
                partition_keys = [column for column in columns if column['kind'] == 'partition_key']
                endpoint_string = ""
                for column in partition_keys:
                    endpoint_string += "-by-" + column['column_name']
                route_path = f"/{keyspace}/{table}"
                for pk in partition_keys:
                    route_path += "/{" + pk["column_name"] + "}"
                endpoint = create_select_by_pk_endpoint(keyspace, table, partition_keys, ResponseModel)
                app.add_api_route(path=route_path, endpoint=endpoint, methods=["GET"], operation_id=f"{keyspace}_{table}_retrieve", openapi_extra={"x-fern-sdk-method-name": "retrieve", "x-fern-sdk-group-name":[keyspace, table], "summary": f"Retrieve: {table}"})

                clustering_columns = [column for column in columns if column['kind'] == 'clustering']
                cc_so_far = []
                for column in clustering_columns:
                    cc_so_far.append(column)
                    endpoint_string += "-by-" + column['column_name']
                    endpoint_path = f"/{keyspace}/{table}/clustering-column-lookup-{table}" + endpoint_string

                    # Using a function factory to ensure proper closure capture
                    def make_endpoint(keyspace=keyspace, table=table, partition_keys=partition_keys, cc_so_far=list(cc_so_far)):
                        return create_select_by_cc_endpoint(keyspace, table, partition_keys, cc_so_far, ResponseModel)

                    #app.post(endpoint_path)(make_endpoint())
                    # comment out clustering columns for now
                    #app.add_api_route(path=endpoint_path, endpoint=make_endpoint(), methods=["POST"], operation_id=f"{keyspace}_{table}_{endpoint_string}", openapi_extra={"x-fern-sdk-method-name": f"filter{endpoint_string}", "x-fern-sdk-group-name":[keyspace, table], "summary": f"Filter: {table}"})


                indexed_columns = self.client.get_indexes(keyspace, table)
                hasIndex = False
                vector_indexes = []
                # TODO - maybe support indexed collections
                for indexed_column in indexed_columns:
                    hasIndex = True
                    # see if it's a vector column
                    # first get the indexed column's details from columns
                    column_raw = [column for column in columns if column['column_name'] == indexed_column]
                    column = []
                    if len(column_raw) > 0:
                        column = column_raw[0]
                    if len(column) > 0 and 'vector' in column['type']:
                        vector_indexes.append(indexed_column)
                        # create a vector endpoint
                # remove vector columns from indexed columns
                indexed_columns = [column for column in indexed_columns if column not in vector_indexes]
                if hasIndex:
                    endpoint_path = f"/{keyspace}/{table}/index-lookup-{table}"
                    endpoint = create_select_by_index_endpoint(
                        keyspace=keyspace,
                        table=table,
                        indexed_columns=indexed_columns,
                        vector_indexes=vector_indexes,
                        partition_keys=partition_keys,
                        columns=columns,
                        response_model=ResponseModel
                    )
                    try:
                        app.add_api_route(path=endpoint_path, endpoint=endpoint, methods=["POST"], operation_id=f"{keyspace}_{table}_search", openapi_extra={"x-fern-sdk-method-name": f"search", "x-fern-sdk-group-name":[keyspace, table], "summary": f"Search: {table}"})
                    except Exception as e:
                        print(e)
                        detail = {"message": str(e)}
                        raise HTTPException(status_code=500, detail=json.dumps(detail))




        openapi_schema = app.openapi()
        for keyspace in keyspaces:
            tables = self.client.get_tables(keyspace)
            for table in tables:
                columns = self.client.get_columns(keyspace, table)
                # filter columns that are partition keys
                partition_keys = [column for column in columns if column['kind'] == 'partition_key']
                endpoint_string = ""
                pk_path = ""
                parameters = []
                properties = {}
                for column in partition_keys:
                    endpoint_string += "-by-" + column['column_name']
                    properties[column['column_name']] = get_openapi_type(column['type'])
                    properties[column['column_name']]['description'] = column['column_name']
                    pk_path += "/{" + column['column_name'] + "}"
                    # TODO: add examples based on column comments
                    parameters.append({
                        "in": "path",
                        "name": column['column_name'],
                        "required": True,
                        "schema": get_openapi_type(column['type']),
                    })
                openapi_schema['paths'][f"/{keyspace}/{table}" + pk_path]["get"]["operationId"] = f"{keyspace}_{table}_retrieve"
                openapi_schema['paths'][f"/{keyspace}/{table}" + pk_path]["get"]["description"] = f"retrieve {keyspace} {table}"
                openapi_schema['paths'][f"/{keyspace}/{table}" + pk_path]["get"]["parameters"] = parameters
                #body = {
                #    "name": "args",
                #    "required": True,
                #    "content" : {
                #        "application/json": {
                #            "schema": {
                #                "type": "object",
                #                "properties": {
                #                    "args": {
                #                        "type": "object",
                #                        "properties": properties
                #                    }
                #                }
                #            }
                #        }
                #    },
                #    "description": "The partition key columns for keyspace " + keyspace+" and table " + table + " are " + str(partition_keys),
                #}
                #post_operation["requestBody"] = body
                clustering_columns = [column for column in columns if column['kind'] == 'clustering']
                cc_so_far = []
                for column in clustering_columns:
                    cc_so_far.append(column)
                    endpoint_string += "-by-" + column['column_name']
                    properties[column['column_name']] = get_openapi_type(column['type'])
                    properties[column['column_name']]['description'] = column['column_name']
                    # disabling cc query for now
                    #post_operation = openapi_schema['paths'][f"/{keyspace}/{table}/clustering-column-lookup-{table}" + endpoint_string]["post"]
                    body = {
                        "required": True,
                        "content" : {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "args": {
                                            "type": "object",
                                            "properties": deepcopy(properties)
                                        }
                                    }
                                }
                            }
                        },
                        "description": "The partition key columns for keyspace " + keyspace+" and table " + table + " are " +
                                       str(partition_keys) + " and the required clustering columns for this endpoint are " + str(cc_so_far),
                    }
                    #post_operation["requestBody"] = body

                indexed_columns = self.client.get_indexes(keyspace, table)
                if len(indexed_columns) > 0:
                    properties = {}
                    indexed_column_details = []
                    for indexed_column in indexed_columns:
                        # TODO: maybe support indexed collections
                        column_raw = [column for column in columns if column['column_name'] == indexed_column]
                        if len(column_raw)>0:
                            column = column_raw[0]
                            indexed_column_details.append(column)
                            properties[column['column_name']] = get_openapi_type(column['type'])
                            properties[column['column_name']]['description'] = column['column_name']
                    for column in partition_keys:
                        properties[column['column_name']] = get_openapi_type(column['type'])
                        properties[column['column_name']]['description'] = column['column_name']
                        properties[column['column_name']]['nullable'] = True
                    post_operation = openapi_schema['paths'][f"/{keyspace}/{table}/index-lookup-{table}"]["post"]
                    body = {
                        "required": True,
                        "content" : {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "args": {
                                            "type": "object",
                                            "properties": properties
                                        }
                                    }
                                }
                            }
                        },
                        "description": "The indexed columns for keyspace " + keyspace+" and table " + table + " are " + str(indexed_column_details) + " and the partition key columns for keyspace " + keyspace+" and table " + table + " are " + str(partition_keys),
                    }
                    post_operation["requestBody"] = body


        openapi_schema['servers']= [{ "url": "https://www.astraplugin.com" }, { "url": "http://localhost:3333" }]
        if "components" in openapi_schema:
            openapi_schema['components']['securitySchemes'] = {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer"
                }
            }
        # add the endpoints to the openapi schema
        self.app.openapi_schema = openapi_schema


def get_astra_bundle_url(dbid, token):
    # Define the URL
    url = f"https://api.astra.datastax.com/v2/databases/{dbid}/secureBundleURL"

    # Define the headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Define the payload (if any)
    payload = {}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload)).json()

    # Print the response
    if 'errors' in response:
        # Handle the errors
        errors = response['errors']
        if errors[0]['message']:
            if errors[0]['message'] == 'JWT not valid':
                logger.warning(
                    "Please use the word `token` and your AstraDB token as CASSANDRA_USER and CASSANDRA_PASSWORD respectively instead of client and secret (starting with `ASTRACS:` to allow dynamic astra keyspace creation")
        return False
    else:
        return response['downloadURL']

def make_keyspace(databaseID, token):
    # Define the URL
    url = f"https://api.astra.datastax.com/v2/databases/{databaseID}/keyspaces/{CASSANDRA_KEYSPACE}"

    # Define the headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Define the payload (if any)
    payload = {}

    # Make the POST request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    except Exception as e:
        logger.debug(f"Failed to create keyspace {CASSANDRA_KEYSPACE} in database {databaseID}: {e}")
        logger.debug(f"Should be because it was hibernated, this should have woken it up. Sleeping 10.")
        time.sleep(10)
        return


    # Print the response
    if 'errors' in response:
        # Handle the errors
        errors = response['errors']
        if errors[0]['message']:
            if errors[0]['message'] == 'JWT not valid':
                logger.warning(
                    "Please use the word `token` and your AstraDB token as CASSANDRA_USER and CASSANDRA_PASSWORD respectively instead of client and secret (starting with `ASTRACS:` to allow dynamic astra keyspace creation")
    return


class VectorRetryPolicy(RetryPolicy):
    def on_read_timeout(self, query, consistency, required_responses,
                        received_responses, data_retrieved, retry_num):
        if retry_num < 3:
            logger.info(f"retrying timeout {retry_num}")
            logger.info(f"query: {query}")
            return RetryPolicy.RETRY, consistency  # return a tuple
        else:
            return RetryPolicy.RETHROW, consistency

    def on_request_error(self, query, consistency, error, retry_num):
        if retry_num < 3:
            logger.info(f"retrying error {retry_num}")
            logger.info(f"query: {query}")
            return RetryPolicy.RETRY, consistency  # return a tuple
        else:
            return RetryPolicy.RETHROW, consistency


    def on_unavailable(self, query, consistency, required_replicas, alive_replicas, retry_num):
        return RetryPolicy.RETHROW, consistency  # return a tuple

    def on_write_timeout(self, query, consistency, write_type,
                         required_responses, received_responses, retry_num):
        return RetryPolicy.RETHROW, consistency  # return a tuple




class CassandraClient():
    def __init__(self, token, dbid) -> None:
        super().__init__()
        self.dbid = dbid
        self.cluster =  None
        try:
            self.connect(token,dbid)
        except NoHostAvailable as e:
            logger.warning(f"No host in the cluster could be contacted: {e}")
            # sleep and retry
            time.sleep(5)
            self.connect(token,dbid)
        except Exception as e:
            logger.warning(f"Exception connecting to cluster: {e}")
            raise e
        # TODO: potentially re-enable document table creation for vector search enabled databases
        #self.create_table(token)

    def connect(self, token, dbid):
        if dbid is not None:
            # connect to Astra
            url = get_astra_bundle_url(dbid, token)
            if url:
                # Download the secure connect bundle and extract it
                r = requests.get(url)
                bundlepath = f'/tmp/{dbid}.zip'
                with open(bundlepath, 'wb') as f:
                    f.write(r.content)
                # Connect to the cluster
                cloud_config = {
                    'secure_connect_bundle': bundlepath
                }
                auth_provider = PlainTextAuthProvider(CASSANDRA_USER, token)
                # TODO - support unhibernating things
                try:
                    self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
                except Exception as e:
                    make_keyspace(dbid, token)
                    logger.warning(f"DB {dbid} is Hibernated, will attempt to wake it up")
                    return self.connect(token,dbid)

                self.session = self.cluster.connect()
            else:
                #time.sleep(5)
                #return self.connect(token, dbid)
                #print("Failed to get secure bundle URL for token and db")
                raise HTTPException(status_code=400, detail="Failed to establish database connection, please check your astradb token")

    def execute(self, ddl):
        try:
            statement = SimpleStatement(
                ddl
                , consistency_level=ConsistencyLevel.QUORUM
            )
            self.session.execute(statement)
        except Exception as e:
            logger.warning(f"Exception creating table or index: {e}")
            if isinstance(e, AlreadyExists):
                raise HTTPException(status_code=409, detail=f"Failed to create table or index {e}")
            raise HTTPException(status_code=400, detail=f"Failed to create table or index {e}")

    def __del__(self):
        # close the connection when the client is destroyed
        if self.cluster:
            self.cluster.shutdown()


    async def select_all_from_table_async(self, keyspace, table) -> List[Dict[str, Any]]:
        return self.select_all_from_table(keyspace, table)

    def select_all_from_table(self, keyspace, table) -> List[Dict[str, Any]]:
        queryString = f"""SELECT * FROM {keyspace}.{table} limit 10"""
        statement = self.session.prepare(queryString)
        statement.consistency_level = ConsistencyLevel.QUORUM
        self.session.row_factory = dict_factory
        rows = self.session.execute(statement)
        json_rows = [dict(row) for row in rows]
        self.session.row_factory = named_tuple_factory
        return json_rows

    async def selectFromTableByPK(self, keyspace, table, partitionKeys, args) -> List[Dict[str, Any]]:
        queryString = f"""SELECT * FROM {keyspace}.{table} WHERE """
        partitionKeyValues = []
        for column in partitionKeys:
            #TODO support other types (single quotes are for strings)
            queryString += f"{column['column_name']} = ? AND "
            partitionKeyValues.append(args[column['column_name']])
        # remove the last AND
        queryString = queryString[:-4]
        statement = self.session.prepare(queryString)
        statement.consistency_level = ConsistencyLevel.QUORUM
        preparedStatement = statement.bind(partitionKeyValues)
        self.session.row_factory = dict_factory
        rows = self.session.execute(preparedStatement)
        json_rows = [dict(row) for row in rows]
        self.session.row_factory = named_tuple_factory
        return json_rows

    async def upsert_table_from_dict_async(self, keyspace_name: str, table_name : str, obj : Dict):
        return self.upsert_table_from_dict(keyspace_name, table_name, obj)

    def upsert_table_from_dict(self, keyspace_name: str, table_name : str, obj : Dict):
        logger.info(f"going to upsert keyspace {keyspace_name} and table {table_name} using {obj}")
        fields = ', '.join(obj.keys())
        placeholders = ', '.join(['?' for _ in range(len(obj.keys()))])

        values_list = []

        for field in obj.keys():
            value = obj.get(field)
            if value is None:
                formatted_value = UNSET_VALUE
            else:
                formatted_value = value
            values_list.append(formatted_value)

        query_string = f"""insert into {keyspace_name}.{table_name}(
                {fields}
            ) VALUES (
                {placeholders}
            );"""

        statement = self.session.prepare(query_string)
        statement.consistency_level = ConsistencyLevel.QUORUM
        try:
            response = self.session.execute(
                statement,
                tuple(values_list)
            )
        except Exception as e:
            logger.error(f"failed to upsert {table_name}: {obj}")
            raise e

    async def get_tables_async(self, keyspace):
        return self.get_tables(keyspace)

    async def get_keyspaces_async(self):
        return self.get_keyspaces()

    def get_keyspaces(self) -> List[str]:
        queryString = "SELECT DISTINCT keyspace_name FROM system_schema.tables"
        statement = self.session.prepare(queryString)
        statement.consistency_level = ConsistencyLevel.QUORUM
        rows = self.session.execute(statement)
        keyspaces = [row.keyspace_name for row in rows]
        keyspaces.remove("system_auth")
        keyspaces.remove("system_schema")
        keyspaces.remove("system")
        keyspaces.remove("data_endpoint_auth")
        keyspaces.remove("system_traces")
        keyspaces.remove("datastax_sla")
        return keyspaces


    async def get_columns_async(self, keyspace, table) -> List[Dict[str, Any]]:
        return self.get_columns(keyspace, table)

    def get_tables(self, keyspace) -> List[str]:
        queryString = f"""SELECT table_name FROM system_schema.tables WHERE keyspace_name='{keyspace}'"""
        statement = self.session.prepare(queryString)
        statement.consistency_level = ConsistencyLevel.QUORUM
        rows = self.session.execute(statement)
        tables = [row.table_name for row in rows]
        return tables

    def get_indexes(self, keyspace, table):
        queryString = f"""
        SELECT options FROM system_schema.indexes 
        WHERE keyspace_name='{keyspace}' 
        and table_name = '{table}'
        and kind = 'CUSTOM' ALLOW FILTERING;
        """
        statement = self.session.prepare(queryString)
        statement.consistency_level = ConsistencyLevel.QUORUM
        self.session.row_factory = dict_factory
        rows = self.session.execute(statement)
        indexes = [row['options'] for row in rows]
        indexed_columns = []
        for index in indexes:
            options = dict(index)
            # TODO - extract whether it's dot vs cosine for vector types
            # and extract vector type
            if 'StorageAttachedIndex' in options['class_name']:
                indexed_columns.append(options['target'])
        self.session.row_factory = named_tuple_factory
        return indexed_columns

    def get_columns(self, keyspace, table) -> List[Dict[str, Any]]:
        queryString = f"""select column_name, kind, type, position from system_schema."columns" WHERE keyspace_name = '{keyspace}' and table_name = '{table}';"""
        statement = self.session.prepare(queryString)
        statement.consistency_level = ConsistencyLevel.QUORUM
        self.session.row_factory = dict_factory
        rows = self.session.execute(statement)
        json_rows = [dict(row) for row in rows]
        self.session.row_factory = named_tuple_factory
        return json_rows

    async def selectFromTableByIndex(self, keyspace, table, indexed_columns, vector_indexes, partition_keys, columns, args) -> List[Dict[str, Any]]:
        queryString = f"SELECT "
        bind_values = []
        for column in columns:
            if column["column_name"] in vector_indexes and column["column_name"] in args:
                # This will work for all vector tables as long as they use openapi ada-002 to make their embeddings.
                # TODO - support other vector types
                # check if column type is vector of dimension 384 and assume that means e5 embedding. IRL we should encode the embedding algo in the index name
                #if '384' in column['type']:
                #    embeddings.append(get_e5_embeddings([args[column['column_name']]]))
                # otherwise default to davinci-002
                #else:
                # TODO maybe optionally support getting embeddings
                #embeddings.append(get_embeddings([args[column['column_name']]]))
                # TODO maybe support scores one day?
                #queryString += f"similarity_cosine(?, {column['column_name']}) as {column['column_name']}_score, "
                # TODO maybe support optionally not sending back vector values
                queryString += f"{column['column_name']}, "
            else:
                queryString += f"{column['column_name']}, "
        queryString = queryString[:-2]

        has_pk_args = False
        for column in partition_keys:
            if column['column_name'] in args:
                has_pk_args = True

        if len(indexed_columns) > 0 or has_pk_args:
            queryString += f""" FROM {keyspace}.{table} WHERE """
        else:
            queryString += f""" FROM {keyspace}.{table} """

        for column in indexed_columns:
            if args[column]:
                # queryString += f"{column} = '{args[column]}' AND "
                queryString += f"{column} = ? AND "
                bind_values.append(args[column])
        # remove the last AND
        if len(indexed_columns) > 0 and not has_pk_args:
            queryString = queryString[:-4]

        if has_pk_args:
            for column in partition_keys:
                if column['column_name'] in args:
                    queryString += f"{column['column_name']} = ? AND "
                    bind_values.append(args[column['column_name']])
        # remove the last AND
        if has_pk_args:
            queryString = queryString[:-4]

        if len(vector_indexes) > 0:
            queryString += f"ORDER BY "
        for column in vector_indexes:
            if column in args:
                queryString += f"""
                {column} ann of ?
                """
                bind_values.append(args[column])
        # TODO make limit configurable
        queryString += f"LIMIT 5"

        statement = self.session.prepare(queryString)
        statement.retry_policy = VectorRetryPolicy()
        statement.consistency_level = ConsistencyLevel.LOCAL_ONE
        boundStatement = statement.bind(bind_values)
        self.session.row_factory = dict_factory
        rows = self.session.execute(boundStatement, timeout=100)
        json_rows = [dict(row) for row in rows]
        #json_rows = [{k: v for k, v in row.items() if not k in vector_indexes} for row in json_rows]
        self.session.row_factory = named_tuple_factory
        return json_rows
