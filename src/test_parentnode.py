import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )
    def test_parent_to_html_no_tag(self):
        with self.assertRaises(ValueError) as context:
            child_node = LeafNode("span", "child")
            node = ParentNode(None, [child_node])
            node.to_html()
        self.assertEqual(str(context.exception), "Parent node has no tag")
    
    def test_parent_to_html_no_children(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode("p", None)
            node.to_html()
        self.assertEqual(str(context.exception), "Parent node has no children")
    
    def test_parent_to_html_multiple_children_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        node = ParentNode(
            "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            ParentNode("div", [child_node]),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i><div><span><b>grandchild</b></span></div></p>")