import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes, markdown_to_blocks

class TestSplitNodes(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.PLAIN_TEXT),
        TextNode("code block", TextType.CODE_TEXT),
        TextNode(" word", TextType.PLAIN_TEXT),
        ])
    
    def test_no_split(self):
        node = TextNode("This is text with a code block word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a code block word", TextType.PLAIN_TEXT),

        ])

    def test_split_nontext(self):
        node1 = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        node2 = TextNode("`code text`",TextType.CODE_TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.PLAIN_TEXT),
        TextNode("code block", TextType.CODE_TEXT),
        TextNode(" word", TextType.PLAIN_TEXT),
        TextNode("`code text`",TextType.CODE_TEXT)
        ])

    def test_split_nonmatching(self):
        with self.assertRaises(Exception) as context:
            node1 = TextNode("This is text with a `code block word", TextType.PLAIN_TEXT)
            node2 = TextNode("`code text`",TextType.CODE_TEXT)
            new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE_TEXT)
        self.assertEqual(str(context.exception), f"Invalid syntax, missing or extra ` symbol")

    def test_multiple_splits(self):
        node = TextNode("This is text with two `code block` word `code`", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
        TextNode("This is text with two ", TextType.PLAIN_TEXT),
        TextNode("code block", TextType.CODE_TEXT),
        TextNode(" word ", TextType.PLAIN_TEXT),
        TextNode("code", TextType.CODE_TEXT)
        ])
    
    def test_bold_split(self):
        node = TextNode("This is text with a **bold** word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.PLAIN_TEXT),
        TextNode("bold", TextType.BOLD_TEXT),
        TextNode(" word", TextType.PLAIN_TEXT),
        ])
    
    def test_italic_split(self):
        node = TextNode("This is text with a _italic_ word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.PLAIN_TEXT),
        TextNode("italic", TextType.ITALIC_TEXT),
        TextNode(" word", TextType.PLAIN_TEXT),
        ])
    
    def test_multiple_text_splits(self):
        node1 = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        node2 = TextNode("`code text`",TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.PLAIN_TEXT),
        TextNode("code block", TextType.CODE_TEXT),
        TextNode(" word", TextType.PLAIN_TEXT),
        TextNode("code text",TextType.CODE_TEXT)
        ])
    
    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_link_image_difference(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_image_link_difference(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])
    
    def test_incomplete_link(self):
        text = "[to boot dev](https:// [to boot dev(https://www.boot.dev) [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])

    def test_incomplete_image(self):
        text = "![to boot dev](https:// ![to boot (https://www.boot.dev) ![to boot dev](https://www.boot.dev)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])
    

    def test_split_link(self):
        node = TextNode("This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode(
                "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
        )
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_connected(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_no_links(self):
        node = TextNode("This is text with an link](https://i.imgur.com/zjjcJKZ.png) and another second link](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
           node
        ],
        new_nodes,
        )
    
    def test_full_text_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) hi"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
        TextNode("This is ", TextType.PLAIN_TEXT),
        TextNode("text", TextType.BOLD_TEXT),
        TextNode(" with an ", TextType.PLAIN_TEXT),
        TextNode("italic", TextType.ITALIC_TEXT),
        TextNode(" word and a ", TextType.PLAIN_TEXT),
        TextNode("code block", TextType.CODE_TEXT),
        TextNode(" and an ", TextType.PLAIN_TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.PLAIN_TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        TextNode(" hi", TextType.PLAIN_TEXT),
        ])
    
    def test_full_text_split_inv(self):
        text = "This is _text_ with an **bold** word and a `code block` and an [link](https://boot.dev) and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) hi"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
        TextNode("This is ", TextType.PLAIN_TEXT),
        TextNode("text", TextType.ITALIC_TEXT),
        TextNode(" with an ", TextType.PLAIN_TEXT),
        TextNode("bold", TextType.BOLD_TEXT),
        TextNode(" word and a ", TextType.PLAIN_TEXT),
        TextNode("code block", TextType.CODE_TEXT),
        TextNode(" and an ", TextType.PLAIN_TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        TextNode(" and a ", TextType.PLAIN_TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" hi", TextType.PLAIN_TEXT),
        ])
    
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_multiline(self):
            md = """
This is **bolded** paragraph


 This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line   


- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )