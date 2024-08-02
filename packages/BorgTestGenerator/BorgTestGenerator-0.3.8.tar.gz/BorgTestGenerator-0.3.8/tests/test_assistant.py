import unittest
from unittest.mock import patch
from BorgTestGenerator.assistant import Assistant
from BorgTestGenerator.assistant import AssistantBackupManager


class TestAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = Assistant()

        name = "Test Assistant"
        instructions = "This is a test assistant."
        model = "gpt-4o"
        tool_code_interpreter = True
        tool_file_search = False

        self.assistant.create_assistant(name, instructions, model, tool_code_interpreter, tool_file_search)

        self.assertEqual(self.assistant.get_assistant_name(), name)
        self.assertEqual(self.assistant.get_assistant_instructions(), instructions)
        self.assertEqual(self.assistant.get_assistant_model(), model)

    # def test_load_assistant(self):
    #     assistant_id = "12345"
    #     self.assistant.load_assistant(assistant_id)
    #     self.assertEqual(self.assistant.assistant_id, assistant_id)

    # def test_create_assistant(self):
    #     name = "Test Assistant"
    #     instructions = "This is a test assistant."
    #     model = "gpt-4o"
    #     tool_code_interpreter = True
    #     tool_file_search = False

    #     self.assistant.create_assistant(name, instructions, model, tool_code_interpreter, tool_file_search)

    #     self.assertEqual(self.assistant.get_assistant_name(), name)
    #     self.assertEqual(self.assistant.get_assistant_instructions(), instructions)
    #     self.assertEqual(self.assistant.get_assistant_model(), model)

    # def test_get_assistant_id(self):
    #     assistant_id = "12345"
    #     self.assistant.assistant_id = assistant_id
    #     self.assertEqual(self.assistant.get_assistant_id(), assistant_id)

    # def test_get_assistant_name(self):
    #     name = "Test Assistant"
    #     self.assistant.assistant.name = name
    #     self.assertEqual(self.assistant.get_assistant_name(), name)

    # def test_get_assistant_model(self):
    #     model = "gpt-4o"
    #     self.assistant.assistant.model = model
    #     self.assertEqual(self.assistant.get_assistant_model(), model)

    # def test_get_assistant_instructions(self):
    #     instructions = "This is a test assistant."
    #     self.assistant.assistant.instructions = instructions
    #     self.assertEqual(self.assistant.get_assistant_instructions(), instructions)

    # def test_get_thread_id(self):
    #     thread_id = "12345"
    #     self.assistant.thread.id = thread_id
    #     self.assertEqual(self.assistant.get_thread_id(), thread_id)

    # def test_list_assistants(self):
    #     assistants = [
    #         {"id": "1", "name": "Assistant 1"},
    #         {"id": "2", "name": "Assistant 2"},
    #         {"id": "3", "name": "Assistant 3"}
    #     ]
    #     with patch.object(self.assistant, "list_assistants", return_value=assistants):
    #         self.assertEqual(self.assistant.list_assistants(), assistants)

    # def test_save_assistants_list(self):
    #     file_name = "assistants.json"
    #     assistants = [
    #         {"id": "1", "name": "Assistant 1"},
    #         {"id": "2", "name": "Assistant 2"},
    #         {"id": "3", "name": "Assistant 3"}
    #     ]
    #     with patch.object(self.assistant, "list_assistants", return_value=assistants):
    #         self.assistant.save_assistants_list(file_name)
    #         # TODO: Assert that the file is saved correctly

    # def test_print_assistants_list(self):
    #     assistants = [
    #         {"id": "1", "name": "Assistant 1"},
    #         {"id": "2", "name": "Assistant 2"},
    #         {"id": "3", "name": "Assistant 3"}
    #     ]
    #     with patch.object(self.assistant, "list_assistants", return_value=assistants):
    #         # TODO: Capture the printed output and assert that it matches the expected output
    #         self.assistant.print_assistants_list()

    # def test_exact_search_assistant(self):
    #     name = "Test Assistant"
    #     model = "gpt-4o"
    #     instructions = "This is a test assistant."
    #     assistants = [
    #         {"id": "1", "name": "Assistant 1", "model": "gpt-4o", "instructions": "This is a test assistant."},
    #         {"id": "2", "name": "Assistant 2", "model": "gpt-3o", "instructions": "This is another test assistant."},
    #         {"id": "3", "name": "Assistant 3", "model": "gpt-4o", "instructions": "This is a test assistant."}
    #     ]
    #     with patch.object(self.assistant, "list_assistants", return_value=assistants):
    #         self.assertEqual(self.assistant.exact_search_assistant(name, model, instructions), assistants[0])

    # def test_delete_assistant(self):
    #     assistant_id = "12345"
    #     with patch.object(self.assistant, "delete_assistant") as mock_delete_assistant:
    #         self.assistant.delete_assistant(assistant_id)
    #         mock_delete_assistant.assert_called_with(assistant_id)


# class TestAssistantBackupManager(unittest.TestCase):
#     def setUp(self):
#         self.backup_manager = AssistantBackupManager(backup_file="test_assistants_list.json", init_refresh=False)

#     def test_refresh_assistants_list(self):
#         with patch.object(self.backup_manager.Assitant_Client, "list_assistants", return_value=[{"id": "1", "name": "Assistant 1"}]):
#             self.backup_manager.refresh_assistants_list()
#             self.assertEqual(len(self.backup_manager.assistants_list), 1)
#             self.assertEqual(self.backup_manager.assistants_list[0]["name"], "Assistant 1")

#     def test_delete_assistants_from_list(self):
#         self.backup_manager.assistants_list = [{"id": "1", "name": "Assistant 1"}, {"id": "2", "name": "Assistant 2"}]
#         with patch.object(self.backup_manager.Assitant_Client, "delete_assistant") as mock_delete_assistant:
#             self.backup_manager.delete_assistants_from_list()
#             self.assertEqual(len(self.backup_manager.assistants_list), 0)
#             self.assertEqual(mock_delete_assistant.call_count, 2)

#     def test_save_assistant(self):
#         assistant_id = "1"
#         file_name = "assistant_1.json"
#         with patch.object(self.backup_manager.Assitant_Client.client.beta.assistants, "retrieve", return_value={"id": "1", "name": "Assistant 1"}):
#             self.backup_manager.save_assistant("/tmp/backup", assistant_id, file_name)
#             # TODO: Assert that the file is saved correctly

#     def test_delete_assistant(self):
#         assistant_id = "1"
#         with patch.object(self.backup_manager.Assitant_Client, "delete_assistant") as mock_delete_assistant:
#             self.backup_manager.delete_assistant(assistant_id)
#             mock_delete_assistant.assert_called_with(assistant_id)

#     def test_backup(self):
#         with patch.object(self.backup_manager, "refresh_assistants_list"):
#             with patch.object(self.backup_manager, "save_assistant"):
#                 with patch.object(self.backup_manager, "delete_assistant"):
#                     self.backup_manager.backup(backup_root_folder="/tmp/backup")
#                     # TODO: Assert that the backup is performed correctly

if __name__ == "__main__":
    unittest.main()