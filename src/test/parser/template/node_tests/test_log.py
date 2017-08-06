import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.log import TemplateLogNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.exceptions import ParserException

from test.parser.template.base import TemplateTestsBaseClass

class TemplateLogNodeTests(TemplateTestsBaseClass):

    def test_init(self):
        log = TemplateLogNode()

        log.level = "debug"
        self.assertEqual("debug", log.level)
        self.assertEqual("", log.resolve(None, None))

        log.level = "warning"
        self.assertEqual("warning", log.level)
        self.assertEqual("", log.resolve(None, None))

        log.level = "error"
        self.assertEqual("error", log.level)
        self.assertEqual("", log.resolve(None, None))

        log.level = "info"
        self.assertEqual("info", log.level)
        self.assertEqual("", log.resolve(None, None))

        log.level = "exception"
        self.assertEqual("exception", log.level)
        self.assertEqual("", log.resolve(None, None))

    def test_set_attrib(self):
        log = TemplateLogNode()

        log.set_attrib('level', 'debug')
        self.assertEqual("debug", log.level)

        log.set_attrib('level', 'warning')
        self.assertEqual("warning", log.level)

        log.set_attrib('level', 'error')
        self.assertEqual("error", log.level)

        log.set_attrib('level', 'info')
        self.assertEqual("info", log.level)

        with self.assertRaises(ParserException):
            log.set_attrib('unknown', 'info')

        with self.assertRaises(ParserException):
            log.set_attrib('level', 'unknown')


    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        log = TemplateLogNode()
        self.assertIsNotNone(log)
        log.append(TemplateWordNode("Log Test"))

        root.append(log)
        self.assertEqual(1, len(root.children))

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

    def test_to_xml_default(self):

        root = TemplateNode()
        log = TemplateLogNode()

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="debug">Log Test</log></template>', xml_str)

    def test_to_xml_debug(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = "debug"

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="debug">Log Test</log></template>', xml_str)

    def test_to_xml_error(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = "error"

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="error">Log Test</log></template>', xml_str)

    def test_to_xml_info(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = "info"

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="info">Log Test</log></template>', xml_str)

    def test_to_xml_warning(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = "warning"

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="warning">Log Test</log></template>', xml_str)

    def test_to_xml_unknown(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = None

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log>Log Test</log></template>', xml_str)
