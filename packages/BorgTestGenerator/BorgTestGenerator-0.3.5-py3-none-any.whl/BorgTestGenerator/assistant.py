#!/usr/bin/env python3
#coding: utf-8

from openai import OpenAI
from os import getenv, path, makedirs
import json
import tempfile
from typing import Optional
from typing import Union
class Assistant(object):
    def __init__(self, assistant_id: Optional[str] = None):
        """
        Initializes an instance of the Assistant class.

        Parameters:
        - assistant_id (str|None): The ID of the assistant or None if not specified.

        """
        self.client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.assistant_id = assistant_id

    def load_assistant(self, assistant_id: Optional[str] = None) -> object:
        """
        Loads the assistant with the specified assistant_id.

        Args:
            assistant_id (str, optional): The ID of the assistant to load. Defaults to None.

        Returns:
            object: The loaded assistant object.

        """
        if assistant_id:
            self.assistant_id = assistant_id
            self.assistant = self.client.beta.assistants.retrieve(f"{self.assistant_id}")
        return self
    
    def create_assistant(self, 
                             name: str, 
                             instructions: str, 
                             model: str = "gpt-4o", 
                             tool_code_interpreter: bool = False, 
                             tool_file_search: bool = True) -> object:
        """
        Create a new assistant with the specified name, instructions, and tools.

        Args:
            name (str): The name of the assistant.
            instructions (str): The instructions for the assistant.
            model (str, optional): The model to use for the assistant. Defaults to "gpt-4o".
            tool_code_interpreter (bool, optional): Whether to include the code interpreter tool. Defaults to False.
            tool_file_search (bool, optional): Whether to include the file search tool. Defaults to True.

        Returns:
            object: The created assistant object.

        """
        tools_ = []
        if tool_code_interpreter:
            tools_.append({"type": "code_interpreter"})
        if tool_file_search:
            tools_.append({"type": "file_search"})

        self.assistant = self.client.beta.assistants.create(
            name=f"{name}",
            instructions=f"{instructions}",
            tools=tools_,
            model=f"{model}"
        )
        return self
    
    def get_assistant_id(self) -> str:
        """
        Returns the ID of the assistant.

        Returns:
            str: The ID of the assistant.
        """
        return self.assistant.id
    
    def get_assistant_name(self) -> str:
        """
        Returns the name of the assistant.

        Returns:
            str: The name of the assistant.
        """
        return self.assistant.name
    
    def get_assistant_model(self) -> str:
        """
        Returns the model used by the assistant.

        Returns:
            str: The model used by the assistant.
        """
        return self.assistant.model
    
    def get_assistant_instructions(self) -> str:
        """
        Returns the instructions provided by the assistant.

        Returns:
            str: The instructions provided by the assistant.
        """
        return self.assistant.instructions
    
    def get_thread_id(self) -> str:
        """
        Returns the ID of the thread associated with this instance.

        Returns:
            str: The ID of the thread.
        """
        return self.thread.id
    
    def list_assistants(self) -> list:
        """
        Retrieves a list of assistants with the specified arguments.

        Returns:
            A list of all assistants retrieved.
        """
        args = {
            'after': None,
            'limit': 100,
            'order': 'asc',
            'timeout': 30
        }

        all_assistants = []
        while True:
            # Retrieves the list of assistants with the specified arguments
            response = self.client.beta.assistants.list(**args)
            assistants = response.data

            if not assistants:
                break

            all_assistants.extend(assistants)

            # Updates the 'after' argument to retrieve the next page
            args['after'] = assistants[-1].id

        return all_assistants
    
    def save_assistants_list(self, file_name: str) -> object:
        """
        Saves the list of assistants to a JSON file.

        Args:
            file_name (str): The name of the file to save the list of assistants to.

        Returns:
            object: The current instance of the Assistant class.

        """
        with open(file_name, 'w') as file:
            json.dump(self.list_assistants(), file)
        return self
    
    def print_assistants_list(self) -> object:
        """
        Prints the list of assistants.

        Returns:
            object: The current instance of the class.
        """
        all_assistants = self.list_assistants()
        for assistant in all_assistants:
            print(f"ID: {assistant.id}, Nom: {assistant.name}")
        return self
    
    def exact_search_assistant(self, 
                               name: str, 
                               model: str, 
                               instructions: str) -> object:
        """
        Searches for an assistant with the exact specified name, model, and instructions.

        Args:
            name (str): The name of the assistant to search for.
            model (str): The model of the assistant to search for.
            instructions (str): The instructions of the assistant to search for.

        Returns:
            object: The assistant object if found, None otherwise.
        """
        assistants = self.list_assistants()
        for assistant in assistants:
            if assistant.name == name and assistant.model == model and assistant.instructions == instructions:
                return assistant
        return None

    def delete_assistant(self, assistant_id: str) -> object:
        """
        Deletes an assistant with the specified ID.

        Args:
            assistant_id (str): The ID of the assistant to delete.

        Returns:
            object: The current instance of the class.
        """
        self.client.beta.assistants.delete(assistant_id)
        return self

    def create_thread(self) -> object:
        """
        Creates a new thread using the client's beta API.

        Returns:
            object: The newly created thread object.
        """
        self.thread = self.client.beta.threads.create()
        return self

    def create_message(self, 
                       role: str, 
                       content: str) -> object:
        """
        Creates a message and adds it to the thread.

        Args:
            role (str): The role of the message.
            content (str): The content of the message.

        Returns:
            object: The created message object.
        """
        self.message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=f"{role}",
            content=f"{content}"
        )
        return self

    def create_run(self) -> object:
        """
        Creates a run for the assistant and polls for its completion.

        Returns:
            object: The created run object.
        """
        self.run = self.client.beta.threads.runs.create_and_poll(
            assistant_id=self.assistant.id,
            thread_id=self.thread.id
        )
        return self

    def upload_files(self, 
                     files_to_upload: Union[list[str], str],
                     vector_store_name: str) -> object:
        """
        Uploads files to OpenAI and adds them to a vector store.

        Args:
            files_to_upload (Union[list[str], str]): A list of file paths or a single file path to upload.
            vector_store_name (str): The name of the vector store to add the files to.

        Returns:
            object: The current instance of the class.

        Raises:
            None

        """
        if type(files_to_upload) == str:
            files_to_upload = [files_to_upload]

        # Create a vector store called "Financial Statements"
        self.vector_store = self.client.beta.vector_stores.create(name=vector_store_name)

        # Ready the files for upload to OpenAI
        self.file_paths = files_to_upload
        self.file_streams = [open(path, "rb") for path in self.file_paths]

        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        self.file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store.id, files=self.file_streams
        )

        print(self.file_batch.status)
        print(self.file_batch.file_counts)
        return self

    def update_assistant_with_vector_store(self) -> object:
        """
        Updates the assistant with the specified vector store.

        Returns:
            object: The updated assistant object.
        """
        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}},
        )
        return self

    def get_assistant_messages(self) -> Union[list, str, None]:
        """
        Retrieves the messages from the assistant.

        Returns:
            list|str|None: The messages from the assistant if the run status is 'completed',
                            otherwise the run status itself.
        """
        if self.run.status == 'completed': 
            self.messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return self.messages.data[0].content[0].text.value
        else:
            return self.run.status


class AssistantBackupManager(object):
    def __init__(self, backup_file="assistants_list.json", init_refresh=True):
        """
        Initializes an instance of the AssistantManager class.

        Args:
            backup_file (str): The name of the backup file to store the assistants list. Defaults to "assistants_list.json".
            init_refresh (bool): Whether to refresh the assistants list during initialization. Defaults to True.
        """
        self.Assistant_Client = Assistant(assistant_id=None)
        self.assistants_list = []
        self.assistant_backup_file = f"{backup_file}"
        self.backup_folder = "/tmp/assistants_backup"
        if init_refresh:
            self.refresh_assistants_list()

    def refresh_assistants_list(self) -> object:
        """
        Refreshes the list of assistants by retrieving the latest data from the Assistant Client.

        Returns:
            object: The updated instance of the class.
        """
        self.assistants_list = []
        self.assistants_list = self.Assitant_Client.list_assistants()
        return self
    
    def delete_assistants_from_list(self) -> object:
        """
        Deletes all assistants from the assistants_list.

        Returns:
            object: The updated instance of the class.
        """
        for assistant in self.assistants_list.data:
            self.Assitant_Client.delete_assistant(assistant.id)
        self.assistants_list = []
        return self

    def save_assistant(self, 
                       backup_folder: str, 
                       assistant_id: str,
                       file_name: str) -> object:
        """
        Save the assistant object to a JSON file.

        Args:
            backup_folder (str): The folder path where the JSON file will be saved.
            assistant_id (str): The ID of the assistant object to be saved.
            file_name (str): The name of the JSON file.

        Returns:
            object: The current instance of the class.

        Raises:
            Exception: If there is an error while converting the assistant object to JSON or writing to the file.

        """
        def assistant_to_json(assistant_object: object) -> str:
            # Function to convert the assistant object to JSON (if you need, you can import libraries to do this)
            try: 
                json_assistant_data_ = {
                    "id": str(assistant_object.id),
                    "created_at": int(assistant_object.created_at),
                    "description": assistant_object.description,
                    "instructions": assistant_object.instructions,
                    "metadata": assistant_object.metadata,
                    "model": assistant_object.model,
                    "name": assistant_object.name,
                    "object": f"{assistant_object.object}",
                    "tools": assistant_object.to_dict()["tools"],
                    "response_format": assistant_object.response_format,
                    "temperature": assistant_object.temperature,
                    "tool_resources": assistant_object.tool_resources.to_dict(),
                    "top_p": assistant_object.top_p
                }
            except Exception as e:
                print(f"Error: {e}")
                exit(1)

            try:
                json_assistant_data = json.dumps(json_assistant_data_,
                                                    indent=4,
                                                    sort_keys=False)
            except Exception as e:
                print(f"Error: {e}")
                exit(1)        

            return json_assistant_data
        
        client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        assistant_object = client.beta.assistants.retrieve(assistant_id)
        assistant_object_data = assistant_to_json(assistant_object)
        
        # Save the assistant object to a JSON file
        with open(f"{backup_folder}/{file_name}", 'w') as file:
            file.write(assistant_object_data)
            file.close()
        
        return self
    
    def delete_assistant(self, assistant_id: str) -> object:
        """
        Deletes an assistant with the specified ID.

        Args:
            assistant_id (str): The ID of the assistant to delete.

        Returns:
            object: The current instance of the Assistant class.

        """
        self.Assitant_Client.delete_assistant(assistant_id)
        return self
        
    def backup(self, 
               backup_root_folder: str = "/tmp/assistants_backup") -> object:
        """
        Backs up the current state of the assistants by saving each individual assistant to a backup folder.

        Args:
            backup_root_folder (str, optional): The root folder where the backup will be stored. Defaults to "/tmp/assistants_backup".

        Returns:
            object: The current instance of the Assistant class.

        """
        def filename_formatify(name: str) -> str:
            """
            Formats the given filename according to the specified rules.

            Args:
                name (str): The original filename.

            Returns:
                str: The formatted filename.

            Rules:
            - First:
                - Replace spaces by underscores.
                - Replace dashes by underscores.
            - Second:
                - Delete/remove/ignore (not replace) all other special characters (except underscores and dots).
            - Third:
                - Check: filename can contain only letters, numbers, underscores, and dots.
                - Check: letters can be in upper or lower case.
            """
            import re

            # STEP 1
            name = re.sub(r"\s+", "_", name)
            name = re.sub(r"-", "_", name)

            # STEP 2 & 3
            name = re.sub(r"[^a-zA-Z0-9_.]", "", name)

            return name

        def make_backup_root_folder() -> None:
            """
            Creates the backup root folder if it doesn't exist.

            This function checks if the backup root folder exists. If it doesn't, it creates the folder.

            Parameters:
                None

            Returns:
                None
            """
            # check if the backup root folder exists
            if not path.exists(backup_root_folder):
                makedirs(backup_root_folder)
        
        make_backup_root_folder()

        # genreate name for the new backup folder ( with a random name )
        backup_folder = tempfile.mkdtemp(dir=backup_root_folder)
        
        # refresh the list of assistants
        self.refresh_assistants_list()

        # save each individual assistant to the backup folder.
        for assistant in self.assistants_list:
            file_name = filename_formatify(f"{assistant.name}_{assistant.id}.json")
            self.save_assistant(
                backup_folder,
                assistant.id,
                file_name
            )
            self.delete_assistant(assistant.id)
        # recresh assistants list again
        self.refresh_assistants_list()
        return self


"""
from assistant import AssistantBackupManager
bck = AssistantBackupManager()
bck.backup()
"""