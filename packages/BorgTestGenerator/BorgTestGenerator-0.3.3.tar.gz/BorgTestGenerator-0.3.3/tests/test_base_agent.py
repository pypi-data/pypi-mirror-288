import unittest
from unittest.mock import patch
from BorgTestGenerator.agents.base_agent import Agent

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent()

    # def test_define_assistant(self):
    #     assistant_id = "12345"
    #     self.agent.define_assistant(assistant_id)
    #     self.assertEqual(self.agent.assistant.get_assistant_id(), assistant_id)

    # def test_search_and_retreive_assistant(self):
    #     with patch.object(self.agent.assistant, "exact_search_assistant", return_value=None):
    #         self.agent.search_and_retreive_assistant()
    #         self.assertIsNone(self.agent.assistant.get_assistant_id())

    #     with patch.object(self.agent.assistant, "exact_search_assistant", return_value={"id": "12345"}):
    #         self.agent.search_and_retreive_assistant()
    #         self.assertEqual(self.agent.assistant.get_assistant_id(), "12345")

    # def test_upload_files(self):
    #     from os import urandom
    #     vector_store_name = "vector_store"
    #     files_to_upload = ["/tmp/file1.txt", "/tmp/file2.txt"]
    #     for file_to_generate in files_to_upload:
    #         with open(file_to_generate, "w") as f:
    #             f.write(urandom(1024).hex())
    #             f.close()
        
    #     with patch.object(self.agent.assistant, "upload_files") as mock_upload_files:
    #         self.agent.upload_files(vector_store_name, files_to_upload)
    #         mock_upload_files.assert_called_once_with(files_to_upload, vector_store_name)

    # def test_create_new_thread(self):
    #     with patch.object(self.agent.assistant, "create_thread") as mock_create_thread:
    #         self.agent.create_new_thread()
    #         mock_create_thread.assert_called_once()

    # def test_create_new_user_message(self):
    #     message_from_user = "Hello"
    #     with patch.object(self.agent.assistant, "create_message") as mock_create_message:
    #         self.agent.create_new_user_message(message_from_user)
    #         mock_create_message.assert_called_once_with("user", message_from_user)

    # def test_run(self):
    #     with patch.object(self.agent.assistant, "create_run") as mock_create_run:
    #         self.agent.run()
    #         mock_create_run.assert_called_once()

    # def test_save_assistant_response_to_file(self):
    #     file_path = "/path/to/output.txt"
    #     with patch.object(self.agent.assistant, "get_assistant_messages", return_value="Hello, world!"):
    #         result = self.agent.save_assistant_response_to_file(file_path)
    #         self.assertTrue(result[0])
    #         self.assertEqual(result[1], file_path)

if __name__ == "__main__":
    unittest.main()