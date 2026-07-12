import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_None(self):
        with self.assertRaises(ValueError) as context:
            node = LeafNode("p", None)
            node.to_html()
        self.assertEqual(str(context.exception), "Leaf node has no value")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")
    
    def test_leaf_to_html_props(self):
        node = LeafNode("a", "google", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">google</a>')

