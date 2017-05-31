import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

"""
A set of scratch tests to provide a unit test framework for testing adhoc grammars
Nothing in here should ever be taken as meaningful tests, they come and go like the wind
( or my novel deadlines..... lol )
"""

class ScratchTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ScratchTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__), ".aiml", False)

class ScratchAIMLTests(unittest.TestCase):

    def setUp (self):
        ScratchAIMLTests.test_client = ScratchTestsClient()

    def test_response(self):
        response = ScratchAIMLTests.test_client.bot.ask_question("testif", "SCRATCH TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'OK')

