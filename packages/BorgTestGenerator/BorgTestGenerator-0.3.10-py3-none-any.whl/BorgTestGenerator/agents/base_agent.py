#coding: utf-8
from ..assistant import Assistant
from ..parsers.code_blocks_parsing import codeBlocksParser

from os import path, rename
import shutil

from typing import Optional
from typing import Union

class Agent(object):
    def __init__(self, 
                     assistant_id: Optional[str] = None, 
                     agent_name: str = "Agent",
                     agent_model: str = "gpt-4o",
                     agent_act_as: str = "",
                     agent_instructions: str = "",
                     tool_code_interpreter: bool = True, 
                     tool_file_search: bool = True):
        """
        Initializes a new instance of the BaseAgent class.

        Args:
            assistant_id (Optional[str], optional): The ID of the assistant. Defaults to None.
            agent_name (str, optional): The name of the agent. Defaults to "Agent".
            agent_model (str, optional): The model used by the agent. Defaults to "gpt-4o".
            agent_act_as (str, optional): The role the agent acts as. Defaults to "".
            agent_instructions (str, optional): The instructions for the agent. Defaults to "".
            tool_code_interpreter (bool, optional): Whether the agent can interpret code. Defaults to True.
            tool_file_search (bool, optional): Whether the agent can search for files. Defaults to True.
        """
        self.agent_model = agent_model
        self.agent_name = agent_name
        self.agent_act_as = agent_act_as
        self.agent_instructions = agent_instructions

        self.tool_code_interpreter = tool_code_interpreter
        self.tool_file_search = tool_file_search

        # 0. Définir l'assistant
        self.define_assistant(assistant_id)

    def define_assistant(self, assistant_id: Optional[str] = None) -> object:
        """
        Defines the assistant for the base agent.

        Args:
            assistant_id (str|None): The ID of the assistant to be defined. If None, a new assistant will be created.

        Returns:
            object: The base agent object.

        """
        # self.assistant_id = assistant_id    
        if assistant_id == None:
            self.assistant = Assistant(assistant_id)
            self.assistant.create_assistant(self.agent_name, 
                                            self.agent_instructions, 
                                            self.agent_model, 
                                            tool_code_interpreter = self.tool_code_interpreter, 
                                            tool_file_search = self.tool_file_search)
            self.assistant.load_assistant(self.assistant.get_assistant_id())
        else:
            self.assistant = Assistant(assistant_id)
            self.assistant.load_assistant()
        return self
    
    def search_and_retreive_assistant(self) -> object:
        """
        Searches for an assistant based on the agent's name, model, and instructions.
        If an assistant is found, it is defined as the agent's assistant.
        If no assistant is found, a new assistant is created and defined as the agent's assistant.

        Returns:
            The updated agent object.
        """
        self.assistant = Assistant(assistant_id=None)
        assistant = self.assistant.exact_search_assistant(
                                                            self.agent_name,
                                                            self.agent_model,
                                                            self.agent_instructions
                                                            )
        if assistant:
            self.define_assistant(assistant.id)
        else:
            self.define_assistant(None)
            self.define_assistant(self.assistant.create_assistant(self.agent_name, self.agent_instructions, self.agent_model, tool_code_interpreter=self.tool_code_interpreter).get_assistant_id())
        return self

    def upload_files(self, 
                         vector_store_name: str,
                         files_to_upload: list[str]) -> object:
        """
        Uploads the specified files to the vector store.

        Args:
            vector_store_name (str): The name of the vector store.
            files_to_upload (list[str]): A list of file paths to upload.

        Returns:
            object: The current instance of the class.

        Raises:
            FileNotFoundError: If any of the files in `files_to_upload` do not exist.

        """
        missing_files = [f for f in files_to_upload if not path.exists(f)]
        if missing_files:
            raise FileNotFoundError(f"Les fichiers suivants sont manquants : {missing_files}")
        
        print(f"Téléchargement des fichiers : {files_to_upload} vers {vector_store_name}")
        try:
            self.assistant.upload_files(files_to_upload, f"{vector_store_name}")
            print("Fichiers téléchargés avec succès.")
        except Exception as e:
            print(f"Erreur lors du téléchargement des fichiers : {e}")

        # 4. Mettre à jour l'assistant avec le vector store
        try:
            self.assistant.update_assistant_with_vector_store()
            print("Assistant mis à jour avec le vector store.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'assistant avec le vector store : {e}")
        return self


    def create_new_thread(self) -> object:
        """
        Creates a new thread and returns the current object.

        This method prints a message indicating the creation of a new thread
        and then calls the `create_thread` method of the assistant object.

        Returns:
            object: The current object.
        """
        print("Création d'un nouveau thread")
        self.assistant.create_thread()
        return self

    def create_new_user_message(self, 
                                    message_from_user: str) -> object:
        """
        Creates a new user message and sends it to the assistant.

        Args:
            message_from_user (str): The message from the user.

        Returns:
            object: The current instance of the base agent.
        """
        print("Création d'un message utilisateur")
        self.assistant.create_message("user", message_from_user)
        return self

    def run(self) -> object:
        """
        Executes the run method.

        This method is responsible for executing the main logic of the agent.

        Returns:
            object: The current instance of the agent.
        """
        print("Exécution du run")
        self.assistant.create_run()
        return self

    def print_assistant_result(self) -> object:
        """
        Prints the messages from the assistant.

        Returns:
            object: The current instance of the class.
        """
        print(self.assistant.get_assistant_messages())
        return self
    
    def get_assistant_result(self) -> str:
        """
        Retrieves the result from the assistant.

        Returns:
            A string representing the result from the assistant.
        """
        return self.assistant.get_assistant_messages()

    def save_assistant_response_to_file(self, 
                                        file_path: str,
                                        remove_block_delimiters: bool = True,
                                        language: Optional[Union[str, bytes, list]] = None,
                                        force_overwrite: bool = False,
                                        backup_if_exists: bool = True) -> tuple[bool, str]:
        """
        Saves the assistant's response to a file.

        Args:
            file_path (str): The path to the file where the assistant's response will be saved.
            remove_block_delimiters (bool, optional): Whether to remove block delimiters from the response. Defaults to True.
            language (str|bytes|list|None, optional): The language of the response. Defaults to None.
            force_overwrite (bool, optional): Whether to force overwrite the file if it already exists. Defaults to False.
            backup_if_exists (bool, optional): Whether to create a backup of the file if it already exists. Defaults to True.

        Returns:
            tuple[bool, str]: A tuple containing a boolean indicating whether the file was saved successfully and the file path.

        Raises:
            FileExistsError: If the file already exists and force_overwrite is set to False.
        """
        def backup_file(file_path: str, 
                        remove_existing_file: bool = False) -> object:
            """
            Backup a file by either renaming (moving) it or copying it to a backup file.

            Args:
                file_path (str): The path of the file to be backed up.
                remove_existing_file (bool, optional): Whether to remove the existing file before backing it up. 
                                                       If set to True, the file will be renamed (moved) to the backup file. 
                                                       If set to False, the file will be copied to the backup file. 
                                                       Defaults to False.

            Returns:
                object: The current instance of the object.

            """

            def find_available_backup_filename(file_path: str) -> str:
                """
                Finds an available backup filename for the given file path.

                Args:
                    file_path (str): The path of the file for which a backup filename is needed.

                Returns:
                    str: The available backup filename.

                """
                backup_file_path = f"{file_path}.bak"
                if path.exists(backup_file_path):
                    i = 1
                    while True:
                        backup_file_path = f"{file_path}.bak.{i}"
                        if not path.exists(backup_file_path):
                            break
                        i += 1
                return backup_file_path
            
            backup_file_path = find_available_backup_filename(file_path)
            
            if path.exists(file_path):
                if remove_existing_file:
                    # rename (move) the file to the backup file
                    rename(file_path, backup_file_path)
                else:
                    # copy the file to the backup file
                    shutil.copy(file_path, backup_file_path)
            return self

        
        def write_file(file_path: str, 
                       data: Union[str, bytes], 
                       force_overwrite: bool = False) -> None:
            """
            Write data to a file.

            Args:
                file_path (str): The path of the file to write.
                data (str|bytes): The data to write to the file.
                force_overwrite (bool, optional): Whether to overwrite the file if it already exists. 
                                                  Defaults to False.

            Raises:
                FileExistsError: If the file already exists and force_overwrite is False.

            """
            file_exists = path.exists(file_path)

            if ( ( file_exists == True ) and ( force_overwrite == True ) ) or ( file_exists == False ):
                if type(data) == bytes:
                    with open(file_path, 'wb') as output_file:
                        output_file.write(data)

                elif type(data) == str:
                    with open(file_path, 'w') as output_file:
                        output_file.write(data)
            else:
                raise FileExistsError

        data = self.assistant.get_assistant_messages()
        if remove_block_delimiters:
            parsed_data = codeBlocksParser(data, language=language)
            final_blocks = [ block["code"] for block in parsed_data['code_blocks'] ]
            final_data = '\n'.join(final_blocks)
        else:
            final_data = data

        if backup_if_exists:
            backup_file(file_path, remove_existing_file=force_overwrite)
        
        file_saved_with_success = None
        try:
            write_file(file_path, final_data, force_overwrite)
            file_saved_with_success = True
        except FileExistsError:
            file_saved_with_success = False
        finally:
            return file_saved_with_success, file_path
