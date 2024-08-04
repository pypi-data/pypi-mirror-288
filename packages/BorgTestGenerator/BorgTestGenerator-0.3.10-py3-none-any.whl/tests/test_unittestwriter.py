import unittest
from unittest.mock import patch
from BorgTestGenerator.agents.unittestwriter import UnitTestWriter

class TestUnitTestWriter(unittest.TestCase):
    def test_set_user_input(self):
        testWriter = UnitTestWriter()
        user_input = "This is a test user input."
        testWriter.set_user_input(user_input)
        self.assertEqual(testWriter.get_user_input(), user_input)

    # def test_unset_user_input(self):
    #     testWriter = UnitTestWriter()
    #     testWriter.set_user_input("This is a test user input.")
    #     testWriter.unset_user_input()
    #     self.assertEqual(testWriter.get_user_input(), "")

    # def test_add_upload(self):
    #     testWriter = UnitTestWriter()
    #     testWriter.add_upload("/path/to/file1.py")
    #     testWriter.add_upload(["/path/to/file2.py", "/path/to/file3.py"])
    #     self.assertEqual(testWriter.ls_upload(), ["/path/to/file1.py", "/path/to/file2.py", "/path/to/file3.py"])

    # def test_del_upload(self):
    #     testWriter = UnitTestWriter()
    #     testWriter.add_upload(["/path/to/file1.py", "/path/to/file2.py", "/path/to/file3.py"])
    #     testWriter.del_upload("/path/to/file2.py")
    #     self.assertEqual(testWriter.ls_upload(), ["/path/to/file1.py", "/path/to/file3.py"])

    # def test_define_vector_store_name(self):
    #     testWriter = UnitTestWriter()
    #     testWriter.define_vector_store_name("test_vector_store")
    #     self.assertEqual(testWriter.FilesToUpload.get_vector_store_name(), "test_vector_store")

    # @patch("BorgTestGenerator.agents.unittestwriter.UnitTestWriter.run_generation")
    # @patch("BorgTestGenerator.agents.unittestwriter.UnitTestWriter.save_generation")
    # def test_generate(self, mock_save_generation, mock_run_generation):
    #     testWriter = UnitTestWriter()
    #     testWriter.set_user_input("This is a test user input.")
    #     testWriter.add_upload(["/path/to/file1.py", "/path/to/file2.py"])
    #     testWriter.define_vector_store_name("test_vector_store")
    #     testWriter.generate()
    #     mock_run_generation.assert_called_once_with(message_from_user="This is a test user input.",
    #                                                 vector_store_name="test_vector_store",
    #                                                 files_to_upload=["/path/to/file1.py", "/path/to/file2.py"])
    #     mock_save_generation.assert_called_once_with(output_filepath="test_test_vector_store.py",
    #                                                  language="python",
    #                                                  force_overwrite=False,
    #                                                  backup_if_exists=True)

if __name__ == "__main__":
    unittest.main()