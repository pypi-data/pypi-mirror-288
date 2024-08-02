# This is a version of the main.py file found in ../../../server/main.py for testing the plugin locally.
# Use the command `poetry run dev` to run this.
import json
from typing import Optional, Dict, List

import dotenv
import uvicorn
import yaml
from astra_assistants.astra_assistants_manager import AssistantManager
from astra_assistants.tools.structured_code import StructuredProgram, StructuredCodeGenerator, StructuredCodeEditor
from astra_assistants.tools.tool_interface import ToolInterface
from fastapi import FastAPI, HTTPException, Body, Response, Depends, Request, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
from loguru import logger
import requests
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from pydantic import BaseModel, Field

from cass_api.assistant.ddl_tool import MakeDDLTool
from cass_api.assistant.util import RequestBody, SimpleCache, MigrateBody, process_thread, TablesBody
from cass_api.ctags.util import parse_ctags, create_ctags_prompt
from cass_api.fern.util import generate_sdk
from datastore.providers.cassandra_datastore import CassandraDataStore
from starlette.responses import FileResponse

dotenv.load_dotenv()

#datastores = Dict[str, CassandraDataStore]
datastores = {}
ctags_by_token = {}

class OptionalHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=param)

optional_bearer_scheme = OptionalHTTPBearer()

async def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_bearer_scheme)):
    if credentials is None:
        return None
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Missing token")
    token = credentials.credentials
    return token

app = FastAPI()

@app.get("/custom-swagger-ui", include_in_schema=False)
async def custom_swagger_ui_html():
    return FileResponse('cass_api/static/custom_swagger_ui.html')

@app.get("/styles.css", include_in_schema=False)
async def styles():
    return FileResponse('cass_api/static/styles.css')

@app.get("/script.js", include_in_schema=False)
async def script():
    return FileResponse('cass_api/static/script.js')


@app.get("/manage.html", include_in_schema=False)
async def manage_html():
    return FileResponse('cass_api/static/manage.html')


@app.get("/openapi_2.json", include_in_schema=False)
async def get_openapi_json(token: Optional[str] = Depends(verify_token)):
    main_schema = app.openapi()
    # TODO potentially re-enable this for vector enabled databases
    #main_schema['components']['schemas']['DeleteRequest']['properties']['ids']['title'] = "DocumentIDs"
    main_schema['paths'] = {path: info for path, info in main_schema['paths'].items() if "/.well-known" not in path}
    if token is None or token not in datastores:
        return Response(content=json.dumps(main_schema))
    datastore = get_datastore_from_cache(token)
    subApp = datastore.getSubApp()
    openapi_schema = subApp.openapi()
    openapi_schema['title'] = "AstraDB Plugin",
    openapi_schema['description'] = "Used for interacting with the user's AstraDB data (AstraDB is an Apache Cassandra based database as a service that contains data organized into keyspaces, tables, and columns) to find answers to questions and retrieve relevant information."
    if 'components' in openapi_schema:
        openapi_schema['components']['schemas'] = openapi_schema['components']['schemas'] | main_schema['components']['schemas']
    for path in main_schema['paths']:
        if "/.well-known" not in path and path not in openapi_schema['paths']:
            openapi_schema['paths'][path] = main_schema['paths'][path]
    return Response(content=json.dumps(openapi_schema))


@app.post(
    "/get_databases",
)
async def get_databases_async(token: str = Depends(verify_token)):
    return get_databases(token)


def get_databases(token: str = Depends(verify_token)):
    # Define the URL
    url = "https://api.astra.datastax.com/v2/databases"

    # Define the headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Make the GET request
    response = requests.get(url, headers=headers).json()

    # Print the response
    if 'errors' in response:
        # Handle the errors
        errors = response['errors']
        if errors[0]['message']:
            if errors[0]['message'] == 'JWT not valid':
                logger.warning(
                    "Please use the word `token` and your AstraDB token as CASSANDRA_USER and CASSANDRA_PASSWORD respectively instead of client and secret (starting with `ASTRACS:` to allow dynamic astra keyspace creation")
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        # return only the [].id's
        return [db['id'] for db in response]

class LoginPayload(BaseModel):
    db_id: str

@app.post(
    "/db_login",
    operation_id="auth.db_login",
    openapi_extra={"x-fern-sdk-method-name": "db_login", "x-fern-sdk-group-name": "manage"}
)
async def db_login_async(payload: LoginPayload = Body(...), token: str = Depends(verify_token)) -> Response:
    return db_login(payload, token)

def db_login(payload: LoginPayload = Body(...), token: str = Depends(verify_token)) -> Response:
    global datastores
    datastore = datastores.get(token)
    if datastore is None:
        datastore = CassandraDataStore()
    if datastore.getSubApp():
        subApp = FastAPI()
        datastore.setupEndpoints(subApp)
        datastores[token] = datastore

        content = {"msg": f"Already logged in to {payload.db_id}. Refreshed schema."}
        app.mount(f"",subApp)
        return Response(status_code=409, content=json.dumps(content))
    if payload.db_id == "":
        return Response(status_code=400, content='{"msg": "db_id is required in payload."}')
    datastore.setupSession(token, payload.db_id)
    subApp = FastAPI()
    datastore.setupEndpoints(subApp)
    datastores[token] = datastore
    app.mount(f"",subApp)
    content = {"msg":f"Successfully logged in to {payload.db_id}."}
    return Response(status_code=200, content=json.dumps(content))

PORT = 3333

#origins = [
#    f"http://localhost:{PORT}",
#    "https://chat.openai.com",
#]
#
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins,
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)


@app.get("/.well-known/ai-plugin.json")
async def get_manifest():
    file_path = "./local_server/ai-plugin.json"
    simple_headers = {}
    simple_headers["Access-Control-Allow-Private-Network"] = "true"
    return FileResponse(file_path, media_type="text/json", headers=simple_headers)


@app.get("/.well-known/logo.png")
async def get_logo():
    file_path = "./local_server/logo.png"
    return FileResponse(file_path, media_type="text/json")

def get_datastore_from_cache(token) -> CassandraDataStore:
    global datastores
    if token in datastores:
        return datastores[token]
    raise HTTPException(status_code=404, detail="Must login to a database ('/db_login') before calling this endpoint")

@app.get("/.well-known/openapi.yaml")
async def get_openapi_yaml(token: Optional[str] = Depends(verify_token)):
    main_schema = app.openapi()
    # TODO potentially re-enable this for vector enabled databases
    #main_schema['components']['schemas']['DeleteRequest']['properties']['ids']['title'] = "DocumentIDs"
    main_schema['paths'] = {path: info for path, info in main_schema['paths'].items() if "/.well-known" not in path}
    if token is None:
        openapi_yaml = yaml.safe_dump(main_schema)
        return Response(content=openapi_yaml)
    if token not in datastores:
        openapi_yaml = yaml.safe_dump(main_schema)
        return Response(content=openapi_yaml)
    datastore = get_datastore_from_cache(token)
    subApp = datastore.getSubApp()
    openapi_schema = subApp.openapi()
    openapi_schema['title'] = "AstraDB Plugin",
    openapi_schema['description'] = "Used for interacting with the user's AstraDB data (AstraDB is an Apache Cassandra based database as a service that contains data organized into keyspaces, tables, and columns) to find answers to questions and retrieve relevant information."
    openapi_schema['components']['schemas'] = openapi_schema['components']['schemas'] | main_schema['components']['schemas']
    for path in main_schema['paths']:
        if "/.well-known" not in path and path not in openapi_schema['paths']:
            openapi_schema['paths'][path] = main_schema['paths'][path]
    openapi_yaml = yaml.safe_dump(openapi_schema)
    return Response(content=openapi_yaml)

thread_cache = SimpleCache()
ddl_list = []
make_ddl_tool = MakeDDLTool(ddl_list)
instructions="""
The user will give you some sort of object (pydantic, zod, pojo, json, go struct, json schema, etc.) your job is to help them design the appropriate cassandra cql table .

Follow these rules:
 - If timestamps are numeric in sample data use bigint, not timestamp.
 - In your explanation call out primary key / partition key and clustering column when applicable and share valid access patterns.
 - Remember that you must pass partition key when you want to select by clustering column.
 - Do not break down objects into separate components. For nested objects initially just use a TEXT field and suggest it's stored as a json string. Cassandra does not support json types.
 - Do not include WITH clauses in your DDL.
 - The field names should match the object keys as much as possible.
 
Use the make_dll tool to create the DLL statement you include and analyze in your response.

Except for METADATA which is a MAP.
"""
data_modeling_manager = AssistantManager(
    instructions=instructions,
    #model="gpt-3.5-turbo",
    model="openai/gpt-4o-mini",
    #model="groq/llama3-8b-8192",
    name="data modeler",
    tools=[make_ddl_tool]
)

@app.post(
    "/manage/{keyspace_name}/{table_name}/design",
    operation_id="design",
    openapi_extra={"x-fern-ignore": True}
    #openapi_extra={"x-fern-sdk-method-name": "design", "x-fern-sdk-group-name": "manage"}
)
async def design(keyspace_name: str = Path(...), table_name: str = Path(...), query: RequestBody = Body(...), token: str = Depends(verify_token)):
    client = data_modeling_manager.get_client()

    thread = None
    thread_id = thread_cache.get(f"{keyspace_name}-{table_name}")
    if thread_id is None:
        thread = data_modeling_manager.thread
        thread_cache.set(f"{keyspace_name}-{table_name}", thread.id)
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id=thread_id)

    content = query.content + f"\nNote: use keyspace_name: {keyspace_name} and table_name:{table_name}"
    result: ToolOutput = await data_modeling_manager.run_thread(
        content=content,
        tool=make_ddl_tool,
        thread=thread
    )
    if result['error'] is not None:
        return design(keyspace_name, table_name, result['error'], token)
    ddl = result['output'].to_string(keyspace_name, table_name)
    response = {
        "diagnosis": result['text'],
        "thread_id": thread.id,
        "design_id": result['design_id'],
        "ddl": ddl,
    }

    return response

@app.post(
    "/manage/{keyspace_name}/{table_name}/migrate",
    operation_id="migrate",
    openapi_extra={"x-fern-ignore": True}
    #openapi_extra={"x-fern-sdk-method-name": "design", "x-fern-sdk-group-name": "migrate"}
)
async def migrate(keyspace_name: str = Path(...), table_name: str = Path(...), query: MigrateBody = Body(...), token: str = Depends(verify_token)):
    global datastores
    if token is None:
        raise HTTPException(status_code=401, detail="Missing token header")
    datastore = get_datastore_from_cache(token)
    design_id = query.design_id
    ddl_cache = data_modeling_manager.tools[0].ddl_cache
    for cached in ddl_cache:
        if str(cached['design_id']) == design_id:
            ddl = cached['output'].to_string()
            datastore.client.execute(ddl)
            output = {"msg":f"Created {keyspace_name}.{table_name} using {query} and {ddl}."}

            await db_login(LoginPayload(db_id=datastore.dbid), token)
            response = await get_openapi_yaml(token)
            generate_sdk(response.body.decode("utf-8"), f'{datastore.dbid}.tags')
            return output


programs: List[Dict[str, StructuredProgram]] = []
code_generator = StructuredCodeGenerator(programs)
code_editor = StructuredCodeEditor(programs)


class TrueOrFalsePayload(BaseModel):
    answer: bool = Field(..., description="true or false")

    def to_string(self):
        return "True" if self.answer else "False"

class TrueOrFalseTool(ToolInterface):
    def call(self, result: TrueOrFalsePayload):
        return {"output": result}


true_or_false_tool = TrueOrFalseTool()
tools = [code_generator, code_editor, true_or_false_tool]

code_manager = AssistantManager(
    instructions="use the structured code tool to generate code to help the user.",
    tools=tools,
    model="openai/gpt-4o",
)

@app.get(
    "/manage/ctags",
    operation_id="ctags",
    #openapi_extra={"x-fern-sdk-method-name": "code", "x-fern-sdk-group-name": "manage"}
    openapi_extra={"x-fern-ignore": True}
)
async def get_ctag_tools(token: str = Depends(verify_token)):
    dbid = datastores[token].dbid
    tags_info = parse_ctags(f"./tenant_ctags/{dbid}.tags")
    ctags_prompt = create_ctags_prompt(tags_info)
    ctags_by_token[token] = {"prompt": ctags_prompt, "tags_info": tags_info}
    tables = list(tags_info.keys())
    tables.remove("manage")
    return {"tables": tables}

@app.post(
    "/manage/ctags",
    operation_id="ctags",
    #openapi_extra={"x-fern-sdk-method-name": "code", "x-fern-sdk-group-name": "manage"}
    openapi_extra={"x-fern-ignore": True}
)
async def enable_ctag_tools(payload: TablesBody = Body(...), token: str = Depends(verify_token)):
    tables = payload.tables
    tables.append("manage")
    dbid = datastores[token].dbid
    tags_info = parse_ctags(f"./tenant_ctags/{dbid}.tags")
    tags_info = {table: tags_info[table] for table in tables}
    ctags_prompt = create_ctags_prompt(tags_info)
    code_manager.additional_instructions = ctags_prompt
    return {"success": True}


@app.post(
    "/manage/code",
    operation_id="code",
    #openapi_extra={"x-fern-sdk-method-name": "code", "x-fern-sdk-group-name": "manage"}
    openapi_extra={"x-fern-ignore": True}
)
async def genreate_code(query: RequestBody = Body(...), token: str = Depends(verify_token)):
    output: ToolOutput = await code_manager.run_thread(
        content=query.content,
        tool=code_generator
    )
    result = code_generator.program_cache
    for program in result:
        program['as_string'] = program['output'].to_string()
        program['as_string_no_line_numbers'] = program['output'].to_string(False)
    return result

@app.post(
    "/manage/code/{program_id}",
    operation_id="edit",
    #openapi_extra={"x-fern-sdk-method-name": "code", "x-fern-sdk-group-name": "manage"}
    openapi_extra={"x-fern-ignore": True}
)
async def edit_code(program_id: str = Path(...), query: RequestBody = Body(...), token: str = Depends(verify_token)):
    program_string = None
    for program_obj in code_editor.program_cache:
        if program_obj['program_id'] == program_id:
            program_string = program_obj['output'].to_string()
            break
    if program_string is None:
        return {"error": f"Program id {program_id} not found"}
    output: ToolOutput = await code_manager.run_thread(
        content=f"## Context:\nMake an edit for the program and describe your changes\nprogram_id: {program_id}\nprogram:\n{program_string}\nperform the following changes to the program using the edit tool: {query.content}",
        tool=code_editor
    )
    result = code_editor.program_cache
    for program in result:
        program['as_string'] = program['output'].to_string()
        program['as_string_no_line_numbers'] = program['output'].to_string(False)
        program['text'] = output['text']

    tf_result: ToolOutput = await code_manager.run_thread(
        content=f"This is the output of the edit \n{result[0]['as_string']}\nIs this what you wanted?",
        tool=true_or_false_tool
    )
    print(f"was it what I wanted? {tf_result['output'].answer}")
    #if not tf_result['output'].answer:
    if False:
        print(f"because: {tf_result['text']}")
        print(f"this is not what I wanted, trying again")
        return await edit_code(program_id, query, token)

    return result



def start():
    #uvicorn.run("cass_api.main:app", host="localhost", port=PORT, reload=True, log_level="debug", reload_excludes=["fern_config/*", "tenant_ctags/*"])
    uvicorn.run("cass_api.main:app", host="localhost", port=PORT)

if __name__ == "__main__":
    start()