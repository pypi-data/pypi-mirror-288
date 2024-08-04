#coding: utf-8

from typing import Any, Union, Optional

from ....assistant import Assistant
from ....parsers.code_blocks_parsing import codeBlocksParser

from os import path, rename
import shutil


# ######## ######## ######## ######## ########
# Base pour creer des Agents de l'essaim
# ######## ######## ######## ######## ########


# class SwarmAgent(object):
#     def __init__(self,
#                  assistant_id: Optional[str] = None,
#                  agent_name: str = "SwarmAgent",
#                  agent_model: str = "gpt-4o",
#                  agent_act_as: str = "",
#                  agent_instructions: str = "",
#                  tool_code_interpreter: bool = False,
#                  tool_file_search: bool = False):
#         self.agent_model = agent_model
#         self.agent_name = agent_name
#         self.agent_act_as = agent_act_as
#         self.agent_instructions = agent_instructions

#         self.tool_code_interpreter = tool_code_interpreter
#         self.tool_file_search = tool_file_search

#         # Définir l'assistant
#         self.define_assistant(assistant_id)

#     def define_assistant(self, assistant_id: Optional[str] = None) -> object
#         """
#         Defines the assistant for the base agent.

#         Args:
#             assistant_id (str|None): The ID of the assistant to be defined. If None, a new assistant will be created.

#         Returns:
#             object: The base agent object.

#         """
#         if assistant_id == None:
#             self.assistant = Assistant(assistant_id)
#             self.assistant.create_assistant(self.agent_name, 
#                                             self.agent_instructions, 
#                                             self.agent_model, 
#                                             tool_code_interpreter = self.tool_code_interpreter, 
#                                             tool_file_search = self.tool_file_search)
#             self.assistant.load_assistant(self.assistant.get_assistant_id())
#         else:
#             self.assistant = Assistant(assistant_id)
#             self.assistant.load_assistant()
#         return self

#     def create_new_user_message(self, 
#                                     message_from_user: str) -> object:
#         """
#         Creates a new user message and sends it to the assistant.

#         Args:
#             message_from_user (str): The message from the user.

#         Returns:
#             object: The current instance of the base agent.
#         """
#         print("Création d'un message utilisateur")
#         self.assistant.create_message("user", message_from_user)
#         return self

                 
