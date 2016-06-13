import unittest

from utils.json_parser import JsonParser
from utils.xml_parser import XMLParser


class TestJSONParser(unittest.TestCase):
    def setUp(self):
        self.parser = JsonParser()


    def test_validjson(self):
        json_object = dict()
        json_object[u'method'] = u'test'
        json_object[u'params'] = [1, 2, 3]
        test_str = '{"params": [1, 2, 3], "method": "test"}'
        res = self.parser.parse(test_str)
        self.assertDictEqual(json_object, res)

    def test_invalidjson(self):
        json_object = dict()
        json_object[u'method'] = u'test'
        json_object[u'params'] = [1, 2, 3]
        test_str = '#ID CLIENT'
        res = self.parser.parse(test_str)
        self.assertFalse(res)

    def test_writeJson(self):
        json_object = dict()
        json_object[u'method'] = u'test'
        json_object[u'params'] = [1, 2, 3]
        res = self.parser.writeJson(json_object)
        test_str = '{"params": [1, 2, 3], "method": "test"}'
        self.assertEquals(res, test_str)


