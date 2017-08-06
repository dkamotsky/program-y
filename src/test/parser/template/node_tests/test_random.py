import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.rand import TemplateRandomNode
from programy.parser.template.nodes.word import TemplateWordNode

from test.parser.template.base import TemplateTestsBaseClass


class TemplateRandomNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        random = TemplateRandomNode()
        random.append(TemplateWordNode("Test1"))
        random.append(TemplateWordNode("Test2"))
        random.append(TemplateWordNode("Test3"))
        self.assertEqual(len(random.children), 3)

        root.append(random)

        resolved = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1", "Test2", "Test3"])

    def test_to_xml(self):
        root = TemplateNode()
        random = TemplateRandomNode()
        root.append(random)
        random.append(TemplateWordNode("Test1"))
        random.append(TemplateWordNode("Test2"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><random><li>Test1</li><li>Test2</li></random></template>", xml_str)

