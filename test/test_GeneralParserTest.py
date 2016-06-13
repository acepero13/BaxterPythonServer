import unittest

from utils.parsers import Parser


class TestGeneralParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def testGoodXML(self):
        print "PARSE"
        xml_object = dict()
        xml_object['method'] = 'paint'
        xml_object['params'] = []
        test_str = '<?xml version="1.0" encoding="UTF-8"?><Command method="paint" id="testId"></Command>'
        res = self.parser.parse(test_str)
        self.assertDictEqual(xml_object, self.parser.parse(test_str))

    def testJSON(self):
        json_object = dict()
        json_object[u'method'] = u'test'
        json_object[u'params'] = [1, 2, 3]
        test_str = '{"params": [1, 2, 3], "method": "test"}'
        self.assertDictEqual(json_object, self.parser.parse(test_str))

    def testBadJSON(self):
        json_object = dict()
        json_object[u'method'] = u'test'
        json_object[u'params'] = [1, 2, 3]
        test_str = '<{"params": [1, 2, 3], "method": "test"}'
        self.assertNotEquals(json_object, self.parser.parse(test_str))