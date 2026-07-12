import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        first_node = TextNode("Test Text", TextType("plain"))
        second_node = TextNode("Test Text", TextType.PLAIN_TEXT)
        self.assertEqual(first_node, second_node)

    def test_ineq(self):
        first = TextNode("Dummy Text", TextType("bold"), "www.youtube.com")
        second = TextNode("Stupid Text", TextType("bold"), "www.youtube.com")
        self.assertNotEqual(first, second)

    def test_eq_url(self):
        first_node = TextNode("Test Text", TextType("plain"), "www.youtube.com")
        second_node = TextNode("Test Text", TextType.PLAIN_TEXT, "www.youtube.com")
        self.assertEqual(first_node, second_node)

    def test_ineq_url(self):
        first_node = TextNode("Test Text", TextType("plain"), "www.youtube.com")
        second_node = TextNode("Test Text", TextType.PLAIN_TEXT, "www.yo.utube.com")
        self.assertNotEqual(first_node, second_node)
    
    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")
    
    def test_code_text(self):
        node = TextNode("This is a code node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://youtube.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": node.url})
    
    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": node.url, "alt": node.text})

    def test_error(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("This is a image node", "wrong")
            html_node = text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Invalid text type")

if __name__ == "__main__":
    unittest.main()