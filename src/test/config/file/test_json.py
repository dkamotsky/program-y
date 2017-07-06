import unittest
import os

from programy.config.file.json_file import JSONConfigurationFile
from programy.config.client.client import ClientConfiguration


class JsonConfigurationFileTests(unittest.TestCase):

    def test_load_from_file(self):
        client_config = ClientConfiguration()
        json = JSONConfigurationFile(client_config)
        self.assertIsNotNone(json)
        json.load_from_file(os.path.dirname(__file__)+"/test_json.json", ",")
        self.assertIsNotNone(json.json_data)
        brain = json.get_section("brain")
        self.assertIsNotNone(brain)
        files = json.get_section("files", brain)
        self.assertIsNotNone(files)
        aiml = json.get_section("aiml", files)
        self.assertIsNotNone(aiml)

        services = json.get_child_section_keys("services", brain)
        self.assertIsNotNone(services)

        depth_str = json.get_option(brain, "max_depth")
        self.assertEqual(100, depth_str)
        supress_warnings = json.get_bool_option(brain, "supress_warnings")
        self.assertFalse(supress_warnings)
        depth_int = json.get_int_option(brain, "max_depth")
        self.assertEqual(100, depth_int)

        other_depth = json.get_option(brain, "max_other_depth", 50)
        self.assertEqual(50, other_depth)
        supress_other_warnings = json.get_bool_option(brain, "supress_other_warnings", True)
        self.assertTrue(supress_other_warnings)
        other_depth_int = json.get_int_option(brain, "other_depth_int", 999)
        self.assertEqual(999, other_depth_int)

        files = json.get_section("files", aiml)
        self.assertIsNotNone(files)
        self.assertEqual(files, "/aiml")
        extension = json.get_section("extension", aiml)
        self.assertIsNotNone(extension)
        self.assertEqual(extension, ".aiml")
        directories = json.get_section("directories", aiml)
        self.assertIsNotNone(directories)
        self.assertEqual(directories, True)

    def test_load_from_text(self):
        client_config = ClientConfiguration()
        json = JSONConfigurationFile(client_config)
        self.assertIsNotNone(json)
        json.load_from_text("""
        {
            "brain": {
                "supress_warnings": false,
                "allow_system_aiml": true,
                "allow_learn_aiml": true,
                "allow_learnf_aiml": true,
        
                "files": {
                    "aiml": {
                        "files": "/aiml",
                        "extension": ".aiml",
                        "directories": true
                    },
                    "sets": {
                        "files": "/sets",
                        "extension": ".txt",
                        "directories": false
                    },
                    "maps": {
                        "files": "/maps",
                        "extension": ".txt",
                        "directories": true
                    },
                    "denormal": "denormal.txt",
                    "normal": "normal.txt",
                    "gender": "gender.txt",
                    "person": "person.txt",
                    "person2": "person2.txt",
                    "predicates": "predicates.txt",
                    "pronouns": "pronouns.txt",
                    "properties": "properties.txt",
                    "triples": "triples.txt",
                    "preprocessors": "preprocessors.txt",
                    "postprocessors": "postprocessors.txt"
                },
        
                "services": {
                    "REST": {
                        "path": "programy.utils.services.rest.GenericRESTService"
                    },
                    "Pannous": {
                        "path": "programy.utils.services.pannous.PannousService"
                    },
                    "Pandora": {
                        "path": "programy.utils.services.pandora.PandoraService"
                    },
                    "Wikipedia": {
                        "path": "programy.utils.services.wikipedia.WikipediaService"
                    }
                }
            },
            "bot": {
                "prompt": ">>>",
                "default_response": "Sorry, I don't have an answer for that!",
                "exit_response": "So long, and thanks for the fish!",
                "initial_question": "Hi, how can I help you>"
            }
        }""", ",")

