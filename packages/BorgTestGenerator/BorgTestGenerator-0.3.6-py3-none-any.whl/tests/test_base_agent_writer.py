import unittest
from BorgTestGenerator.agents.base_agent_writer import FilesListToUpload
from BorgTestGenerator.agents.base_agent_writer import BaseAgentWriter

class TestFilesListToUpload(unittest.TestCase):
    def test_is_empty(self):
        # Test case 1: Empty list
        files_list = FilesListToUpload()
        self.assertTrue(files_list.is_empty())

        # Test case 2: Non-empty list
        files_list = FilesListToUpload(['file1.txt', 'file2.txt'])
        self.assertFalse(files_list.is_empty())

#     def test_is_unnamed(self):
#         # Test case 1: Unnamed vector store
#         files_list = FilesListToUpload(vector_store_name=None)
#         self.assertTrue(files_list.is_unnamed())

#         # Test case 2: Named vector store
#         files_list = FilesListToUpload(vector_store_name='vector_store')
#         self.assertFalse(files_list.is_unnamed())

#     def test_add_file(self):
#         files_list = FilesListToUpload()
#         files_list.add_file('file1.txt')
#         self.assertEqual(files_list, ['file1.txt'])

#     def test_add_files(self):
#         files_list = FilesListToUpload()
#         files_list.add_files(['file1.txt', 'file2.txt'])
#         self.assertEqual(files_list, ['file1.txt', 'file2.txt'])

#     def test_remove_file(self):
#         files_list = FilesListToUpload(['file1.txt', 'file2.txt'])
#         files_list.remove_file('file1.txt')
#         self.assertEqual(files_list, ['file2.txt'])

#     def test_list_files(self):
#         files_list = FilesListToUpload(['file1.txt', 'file2.txt'])
#         self.assertEqual(files_list.list_files(), ['file1.txt', 'file2.txt'])

#     def test_set_vector_store_name(self):
#         files_list = FilesListToUpload()
#         files_list.set_vector_store_name('vector_store')
#         self.assertEqual(files_list.get_vector_store_name(), 'vector_store')

#     def test_get_vector_store_name(self):
#         files_list = FilesListToUpload(vector_store_name='vector_store')
#         self.assertEqual(files_list.get_vector_store_name(), 'vector_store')

# class TestBaseAgentWriter(unittest.TestCase):
#     def test_check_and_retreive(self):
#         # Test case 1: Assistant is not set
#         agent = BaseAgentWriter()
#         agent.check_and_retreive()
#         self.assertIsNotNone(agent.assistant)

#         # Test case 2: Assistant ID is not set
#         agent = BaseAgentWriter(assistant_id=None)
#         agent.check_and_retreive()
#         self.assertIsNotNone(agent.assistant)

#         # Test case 3: Assistant is already set
#         agent = BaseAgentWriter()
#         agent.assistant = "Test Assistant"
#         agent.check_and_retreive()
#         self.assertEqual(agent.assistant, "Test Assistant")

#     def test_run_generation(self):
#         # Test case 1: No vector store name and files to upload
#         agent = BaseAgentWriter()
#         agent.run_generation("Hello, world!")
#         # Add assertions here

#         # Test case 2: With vector store name and files to upload
#         agent = BaseAgentWriter()
#         agent.run_generation("Hello, world!", vector_store_name="vector_store", files_to_upload=["file1.txt", "file2.txt"])
#         # Add assertions here

#     def test_save_generation(self):
#         # Test case 1: Output file does not exist
#         agent = BaseAgentWriter()
#         agent.save_generation("output.txt")
#         # Add assertions here

#         # Test case 2: Output file exists and force_overwrite is True
#         agent = BaseAgentWriter()
#         agent.save_generation("output.txt", force_overwrite=True)
#         # Add assertions here

#         # Test case 3: Output file exists and force_overwrite is False
#         agent = BaseAgentWriter()
#         agent.save_generation("output.txt", force_overwrite=False)
#         # Add assertions here

if __name__ == "__main__":
    unittest.main()