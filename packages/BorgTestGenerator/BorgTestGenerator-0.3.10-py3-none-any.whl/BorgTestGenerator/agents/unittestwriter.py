#coding: utf-8

from .base_agent_writer import BaseAgentWriter, FilesListToUpload
from ..utils.files import read_text_file
import pkg_resources
import uuid
from typing import Optional
from typing import Union

class UnitTestWriter(BaseAgentWriter):
    def __init__(self, 
                 assistant_id: Optional[str] = None,
                 code_language: str = "python"):
        """
        Initializes the UnitTestWriter object.

        Args:
            assistant_id (str|None, optional): The ID of the assistant. Defaults to None.
            code_language (str, optional): The code language. Defaults to "python".
        """
        super().__init__(assistant_id)
        self.FilesToUpload = FilesListToUpload()
        self.user_input = ""
        self.code_language = code_language
        self.define_agent_presets()

    def define_agent_presets(self) -> object:
        """
        Defines the presets for the UnitTestWriter agent.

        Returns:
            object: The UnitTestWriter object with the defined presets.
        """
        self.agent_name = "UnitTestWriter"
        self.agent_model = "gpt-4o"
        self.agent_act_as = read_text_file(pkg_resources.resource_filename(__name__, "prompts/roles/linus_torvald.txt"))
        self.agent_instructions = read_text_file(pkg_resources.resource_filename(__name__, "prompts/instructions/py3_unit_tests_writer.txt"))
        self.tool_code_interpreter = True
        self.tool_file_search = True
        return self


    # #####################################
    # Gestion des instructions utilisateur
    # #####################################
    def set_user_input(self, 
                       user_input: str) -> object:
        """
        Sets the user input for the test case.

        Args:
            user_input (str): The user input to be set.

        Returns:
            object: The current instance of the class.

        """
        self.user_input = user_input
        return self

    def unset_user_input(self) -> object:
        """
        Unsets the user input by setting it to an empty string.

        Returns:
            object: The instance of the class.
        """
        self.user_input = ""
        return self

    def get_user_input(self) -> str:
        """
        Returns the user input stored in the instance variable `user_input`.

        Returns:
            str: The user input.
        """
        return self.user_input
    
    def user_input_is_empty(self) -> bool:
        """
        Checks if the user input is empty.

        Returns:
            bool: True if the user input is empty, False otherwise.
        """
        return len(self.user_input) == 0

    # #####################################
    # Gestion des fichiers à télécharger
    # #####################################
    def add_upload(self, filepath: Union[str, list[str]]) -> object:
        """
        Adds a file or a list of files to the FilesToUpload object.

        Args:
            filepath (str|list[str]): The path of the file(s) to be added.

        Returns:
            object: The current instance of the class.

        Raises:
            None

        """
        if type(filepath) == str:
            self.FilesToUpload.add_file(filepath)
        elif type(filepath) == list[str]:
            self.FilesToUpload.add_files(filepath)
        return self
    
    def del_upload(self, 
                   filepath: Union[str, list[str]]) -> object:
        """
        Removes the specified file or files from the list of files to upload.

        Args:
            filepath (str or list[str]): The path(s) of the file(s) to be removed.

        Returns:
            object: The current instance of the class.

        """
        if type(filepath) == str:
            self.FilesToUpload.remove_file(filepath)
        elif type(filepath) == list[str]:
            for file in filepath:
                self.FilesToUpload.remove_file(file)
        return self
    
    def ls_upload(self) -> list[str]:
        """
        Returns a list of files to upload.

        Returns:
            A list of file paths to upload.
        """
        return self.FilesToUpload.list_files()
    
    def define_vector_store_name(self,
                                 vector_store_name: Optional[str] = None) -> object:
        """
        Sets the name of the vector store.

        If `vector_store_name` is `None`, a unique name will be generated using UUID.
        Otherwise, the provided `vector_store_name` will be used.

        If the vector store is unnamed, a unique name will be generated.

        Returns:
            The current instance of the class.
        """
        def generate_unique_name() -> str:
            return f"{uuid.uuid4()}"
        
        if vector_store_name is None:
            self.FilesToUpload.set_vector_store_name(generate_unique_name())
        else:
            self.FilesToUpload.set_vector_store_name(vector_store_name)
        
        if self.FilesToUpload.is_unnamed():
            self.FilesToUpload.set_vector_store_name(generate_unique_name())
        
        return self
    
    def generate(self) -> object:
        """
        Generates the unit test based on the user input and files to upload.

        Raises:
            ValueError: If no user instruction is defined, no file to upload is defined, or no vector store name is defined.

        Returns:
            object: The current instance of the class.
        """
        def check_values_errors() -> None:
            if self.user_input_is_empty():
                raise ValueError("Aucune instruction utilisateur n'a été définie.")
            if  self.FilesToUpload.is_empty():
                raise ValueError("Aucun fichier à télécharger n'a été défini.")
            if self.FilesToUpload.is_unnamed():
                raise ValueError("Aucun nom de vector store n'a été défini.")

        check_values_errors()
        self.run_generation(message_from_user=self.user_input,
                            vector_store_name=self.FilesToUpload.get_vector_store_name(),
                            files_to_upload=self.FilesToUpload.list_files())
        self.save_generation(output_filepath=f"test_{self.FilesToUpload.get_vector_store_name()}.py",
                                language= self.code_language,
                                force_overwrite=False,
                                backup_if_exists=True)
        return self
        
"""
# Exemple d'utilisation
from BorgTestGenerator.agents.unittestwriter import UnitTestWriter
testWriter = UnitTestWriter(code_language="python")
testWriter.set_user_input("Écrit le code du fichier test correspondant a ce script python")
testWriter.add_upload(["/path/to/file1.py", "/path/to/file2.py"])
testWriter.define_vector_store_name("test_vector_store")
testWriter.generate()
"""