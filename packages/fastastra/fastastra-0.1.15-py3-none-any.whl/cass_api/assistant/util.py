import asyncio
from typing import List

from astra_assistants.astra_assistants_event_handler import AstraEventHandler
from fastapi import HTTPException
from pydantic import BaseModel


class RequestBody(BaseModel):
    content: str

class TablesBody(BaseModel):
    tables: List[str]

class TableModel(BaseModel):
    partition_key: List[BaseModel]



class MigrateBody(BaseModel):
    design_id: str

class SimpleCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def clear(self):
        self.cache.clear()


async def process_thread(client, content, thread, assistant_manager):
    assistant = assistant_manager.get_assistant()
    tool = assistant_manager.get_tool()
    event_handler = AstraEventHandler(client)
    event_handler.register_tool(tool)
    try:
        client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=content
        )
        with client.beta.threads.runs.create_and_stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=event_handler,
            tool_choice=tool.tool_choice_object(),
        ) as stream:
            for part in stream:
                pass
        text = ""
        with event_handler.stream as stream:
            for part in stream.text_deltas:
                text += part

        # TODO: fix this hack for concurrency etc.
        ddl = tool.ddl_cache[len(tool.ddl_cache)-1]

        response = {
            "diagnosis": text,
            "thread_id": thread.id,
            "design_id": ddl['design_id'],
            "ddl": ddl['ddl_statement'],
        }
        print(response)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
