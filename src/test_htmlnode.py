import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_None(self):
        first = HTMLNode("p", "hello")
        result = first.props_to_html()
        expected = ""
        self.assertEqual(expected,result)

    def test_props_to_html_empty(self):
        first = HTMLNode("p", "hello", [], {})
        result = first.props_to_html()
        expected = ""
        self.assertEqual(expected,result)

    def test_props_to_html(self):
        first = HTMLNode("p", "hello", [],{"href": "https://www.google.com", "target": "_blank",})
        result = first.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected,result)