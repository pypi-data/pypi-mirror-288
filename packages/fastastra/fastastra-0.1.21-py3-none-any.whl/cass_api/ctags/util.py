import os
import re
import subprocess
import json

def generate_ctags(directory, output_file):
    """
    Generate ctags for the specified directory and output to the given file.
    """
    if os.path.exists(output_file):
        os.remove(output_file)
    cmd = ['ctags', '-R', '--output-format=json', '--fields=+KnlSa', '--extras=+q', '-f', output_file, directory]
    print(f"about to run command: {cmd}")
    result = subprocess.run(cmd, check=True)
    print(f"result: {result}")


def parse_json_lines_file(file_path):
    tags_info = {'tags': []}
    with open(file_path, 'r') as file:
        for line in file:
            tags_info['tags'].append(json.loads(line))
    return tags_info

def extract_table_name(file_path):
    match = re.search(r'/([^/]+)/client.py', file_path)
    if match:
        return match.group(1)
    return None

def parse_ctags(file_path):
    tags_info = parse_json_lines_file(file_path)


    client_classes_with_retrieve = set()
    for entry in tags_info['tags']:
        if "Client" in entry.get("scope", "") and entry.get("name") == "retrieve":
            client_classes_with_retrieve.add(entry["scope"])
        if "Client" in entry.get("scope", "") and entry.get("name") == "db_login":
            client_classes_with_retrieve.add(entry["scope"])

    relevant_entries = {}
    for entry in tags_info['tags']:
        if entry.get("scope") in client_classes_with_retrieve:
            table = extract_table_name(entry.get("path"))
            if relevant_entries.get(table) is None:
                relevant_entries[table] = []
            relevant_entries[table].append(entry)


    return relevant_entries


def create_ctags_prompt(tags_info):
    prompt = f"""
    You are given a custom SDK with the following ctag information::

    {tags_info}
    
    The SDK usage is similar to the following example (replace keyspace and table with values from the ctag information):
    
    ```python
    import os
    import dotenv
    from src.datastax.client import db

    dotenv.load_dotenv()

    client = db(
        token=os.getenv('ASTRA_DB_APPLICATION_TOKEN'),
    )


    try:
        client.manage.db_login(db_id=os.getenv('ASTRA_DB_ID'))
    except Exception as e:
        if hasattr(e,"status_code") and e.status_code == 409:
            pass
        else:
            print(e)
            raise e

    embedding = [0.37972306566599356, ...]

    client.default_keyspace.document_chunks.create(
        chunk_id="test",
        document_id="test",
        user_id="test",
        workspace_id="test_2",
        chunk_data="a long string",
        embedding=embedding,
    )
    chunk = client.default_keyspace.document_chunks.retrieve(user_id="test", workspace_id="test_2")
    print("chunk" + chunk")

    chunks = client.default_keyspace.document_chunks.search(args={{"embedding": embedding, "user_id": "test", "workspace_id": "test"}})
    print("ann result count: " + len(chunks)")
    ```

    """
    return prompt