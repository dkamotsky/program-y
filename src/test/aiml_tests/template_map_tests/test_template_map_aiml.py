import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = os.path.dirname(__file__)
        self.configuration.brain_configuration.files.map_files._files=os.path.dirname(__file__)+ os.sep + "maps"
        self.configuration.brain_configuration.files.map_files._extension=".txt"

class TemplateMapAIMLTests(unittest.TestCase):

    def setUp(self):
        TemplateMapAIMLTests.test_client = BasicTestClient()

    def test_name_map_topic(self):
        response = TemplateMapAIMLTests.test_client.bot.ask_question("test",  "NAME MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK VAL1")

    def test_multi_word_name_map_topic(self):
        response = TemplateMapAIMLTests.test_client.bot.ask_question("test",  "MULTI WORD NAME MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK VAL1")
