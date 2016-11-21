import unittest
import subprocess
import os, sys
import json

http_suitcase = 'http://pkit.wopr.c2x.io:8000/suitcases/rolly'
http_parts = 'http://pkit.wopr.c2x.io:8000/robots/hey-you/parts'
file_suitcase = '../test/suitcase.json'
file_parts = '../test/parts.json'

class TestExecutableInterface(unittest.TestCase):

    def setUp(self):
        os.chdir('src')

    def tearDown(self):
        os.chdir('..')

    def test_output_format(self):
        command = [sys.executable, 'pack_bot.py',
            http_suitcase,
            http_parts]
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        # output = subprocess.check_output(command)
        result = json.loads(output)
        self.assertIn('value',result, "pack_bot.py failed to output json field 'value'")
        self.assertIn('part_ids',result, "pack_bot.py failed to output json field 'part_ids'")

    def test_regress_against_files(self):
        command = [sys.executable, 'pack_bot.py', file_suitcase, file_parts]
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        # output = subprocess.check_output(command)
        result = json.loads(output)
        expected_result = {
                "part_ids": [
                    "part-1",
                    "part-2",
                    "part-3",
                    "part-4",
                    "part-5",
                    "part-6",
                    "part-8",
                    "part-9",
                    "part-10",
                    "part-11",
                    "part-12",
                    "part-13",
                    "part-14",
                    "part-15",
                    "part-16",
                    "part-17",
                    "part-18",
                    "part-19",
                    "part-22",
                    "part-23",
                    "part-24",
                    "part-25",
                    "part-26",
                    "part-27",
                    "part-28",
                    "part-29",
                    "part-30",
                    "part-32",
                    "part-33",
                    "part-34",
                    "part-36",
                    "part-37",
                    "part-38",
                    "part-39",
                    "part-40",
                    "part-42",
                    "part-44"],
                "value": 1163
            }
        self.assertDictEqual(result,expected_result, "pack_bot.py failed to produce valid json known regression files")

