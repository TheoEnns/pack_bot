import unittest
from src import pb_get_json
from pack_sources import *

class TestImportingInputSources(unittest.TestCase):

    def setUp(self):
        pass

    def test_http_fetch_json(self):
        """
        Simple check to verify I can reach servers; does not verify content of output
        """
        data = pb_get_json.http_fetch_json(http_suitcase)
        self.assertIsNotNone(data)
        data = pb_get_json.http_fetch_json(http_parts)
        self.assertIsNotNone(data)

    def test_verify_sample_file_loading(self):
        """
        Verify test file loading is functioning
        """
        result = pb_get_json.grab_dict_from(file_suitcase)
        self.assertEqual( result['volume'], 1584)
        result = pb_get_json.grab_dict_from(file_parts)
        self.assertEqual( len(result), 44)
        self.assertEqual( result[0]['id'], 'part-1')

if __name__ == '__main__':
    unittest.main()
