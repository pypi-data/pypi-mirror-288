#coding: utf-8

from .base_agent import Agent
import os
from typing import Optional
from typing import Union

class FilesListToUpload(list):
    def __init__(self, 
                 files: Optional[list[str]] = [],
                 vector_store_name: Optional[str] = None):
        """
        Initializes a BaseAgentWriter object.

        Args:
            files (list[str], optional): A list of file paths. Defaults to an empty list.
            vector_store_name (str|None, optional): The name of the vector store. Defaults to None.
        """
        super().__init__(files)
        self.vector_store_name = vector_store_name
    
    def is_empty(self) -> bool:
        """
        Checks if the agent is empty.

        Returns:
            bool: True if the agent is empty, False otherwise.
        """
        return len(self) == 0

    def is_unnamed(self) -> bool:
        """
        Checks if the agent is unnamed.

        Returns:
            bool: True if the agent is unnamed, False otherwise.
        """
        return (type(self.vector_store_name) == None) or (len(f"{self.vector_store_name}") == 0)

    def add_file(self, filepath: str) -> None:
        """
        Adds a file to the agent's list of files.

        Args:
            filepath (str): The path of the file to be added.

        Returns:
            None
        """
        self.append(filepath)

    def add_files(self, files: list[str]) -> None:
        """
        Adds a list of files to the agent.

        Args:
            files (list[str]): A list of file paths to be added.

        Returns:
            None
        """
        for file in files:
            self.add_file(file)

    def remove_file(self, filepath: str) -> None:
        """
        Removes a file from the specified filepath.

        Args:
            filepath (str): The path of the file to be removed.

        Returns:
            None
        """
        self.remove(filepath)

    def list_files(self) -> list[str]:
        """
        Returns a list of files.

        Returns:
            A list of file names.
        """
        return self
    
    def set_vector_store_name(self, vector_store_name: str) -> None:
        """
        Sets the name of the vector store.

        Args:
            vector_store_name (str): The name of the vector store.

        Returns:
            None
        """
        self.vector_store_name = vector_store_name
        
    def get_vector_store_name(self) -> str:
        """
        Returns the name of the vector store.

        Returns:
            str: The name of the vector store.
        """
        return self.vector_store_name
    


class BaseAgentWriter(Agent):
    def __init__(self, assistant_id: Optional[str] = None):
        """
        Initializes a new instance of the BaseAgentWriter class.

        Args:
            assistant_id (str|None): The ID of the assistant. Defaults to None.
        """
        super().__init__(assistant_id)

    def check_and_retreive(self) -> Agent:
        """
        Checks if the assistant is available and retrieves it if necessary.

        If the assistant is not set or the assistant ID is not set, this method
        searches and retrieves the assistant.

        Returns:
            The current instance of the Agent class.
        """
        if (type(self.assistant) == None) or (self.assistant.assistant_id == None):
            self.search_and_retreive_assistant()
        return self

    def run_generation(self, 
                       message_from_user: str,
                       vector_store_name: Optional[str] = None, 
                       files_to_upload: Optional[list[str]] = None) -> Agent:
        """
        Runs the generation process for the agent.

        Args:
            message_from_user (str): The message provided by the user.
            vector_store_name (str|None, optional): The name of the vector store. Defaults to None.
            files_to_upload (list[str]|None, optional): The list of files to upload. Defaults to None.

        Returns:
            Agent: The updated agent object.

        Raises:
            FileNotFoundError: If a file is not found.
            Exception: If an unexpected error occurs.
        """
        try:
            print("Début de la génération...")
            if (type(vector_store_name)!=None):
                self.upload_files(vector_store_name, files_to_upload)
            self.create_new_thread()
            self.create_new_user_message(f"{message_from_user}")
            self.run()
            self.print_assistant_result()
            print("Génération terminée avec succès.")
        except FileNotFoundError as fnf_error:
            print(f"Erreur : {fnf_error}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")
        return self

    def save_generation(self, 
                            output_filepath: str,
                            language: Optional[Union[str, bytes, list]] = ["python"],
                            force_overwrite: bool = False,
                            backup_if_exists: bool = True) -> Agent:
        """
        Saves the generated response of the assistant to a file.

        Args:
            output_filepath (str): The path of the output file to save the response to.
            language (str|bytes|list|None, optional): The language of the response. Defaults to ["python"].
            force_overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to False.
            backup_if_exists (bool, optional): Whether to create a backup of the existing file if it already exists. Defaults to True.

        Returns:
            Agent: The current instance of the Agent class.

        """
        if os.path.exists(output_filepath):
            if force_overwrite:
                os.remove(output_filepath)
            else:
                print(f"Le fichier {output_filepath} existe déjà !")
                return self
            
        print("Sauvegarde de la réponse de l'assistant...")
        success_, saved_filepath = self.save_assistant_response_to_file(output_filepath, 
                                                remove_block_delimiters=True, 
                                                language=language, 
                                                force_overwrite=force_overwrite, 
                                                backup_if_exists=backup_if_exists)
        if success_:
            print(f"Réponse de l'assistant sauvegardée dans le fichier : {saved_filepath}")
        else:
            print("Erreur lors de la sauvegarde de la réponse de l'assistant dans le fichier : {saved_filepath}")
        return self


