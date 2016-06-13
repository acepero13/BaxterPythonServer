import unittest

from utils.xml_parser import XMLParser


class TestXMLParser(unittest.TestCase):
    def setUp(self):
        self.parser = XMLParser()

    def testValidXML(self):
        xml_object = dict()
        xml_object['method'] = 'test'
        xml_object['params'] = ['1', '2', '3']
        test_str = '<Command method="test"> <params> <param>1</param><param>2</param><param>3</param> </params> ' \
                   ' </Command>'
        res = self.parser.parse(test_str)
        self.assertDictEqual(xml_object, res)

    def testMethodNotDefined(self):
        test_str = '<Command> <params> <param>1</param><param>2</param><param>3</param> </params> ' \
                   ' </Command>'
        with self.assertRaises(Exception) as context:
            res = self.parser.parse(test_str)
        self.assertTrue('Method not defined' in context.exception)

    def testCommanddNotDefined(self):
        test_str = '<badcommand> <params> <param>1</param><param>2</param><param>3</param> </params> ' \
                   ' </badcommand>'
        with self.assertRaises(Exception) as context:
            res = self.parser.parse(test_str)
        self.assertTrue('Command not specified' in context.exception)

    def testBadXML(self):
        test_str = '<badcommand> <params> <param>1</param><param>2</param><param>3</param> </params> ' \
                   ' <ff>'
        with self.assertRaises(Exception) as context:
            res = self.parser.parse(test_str)
        self.assertTrue('A problem has occurred parsing xml' in context.exception)





