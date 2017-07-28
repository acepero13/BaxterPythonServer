from unittest import TestCase

from src.libs.sentimentanalysis.command_parser import CommandParser


class TestCommandParser(TestCase):
    def test_parse_with_right_xml(self):
        xml = '<messages><message type="voice_recognition" id="#MessageID: 1">Hello world this is a test</message></messages>'
        commandParser = CommandParser()
        commandParser.parse(xml)
        res = commandParser.getMessage()
        self.assertEqual("Hello world this is a test", res)