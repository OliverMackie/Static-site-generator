import unittest
from blocktype import BlockType, block_to_blocktype, markdown_to_html_node
from copy_content import extract_title

class TestTextNode(unittest.TestCase):
    def test_block_to_blocktype_heading(self):
        text = "#### heading"
        type1 = block_to_blocktype(text)
        self.assertEqual(type1, BlockType.HEADING)
    
    def test_block_to_blocktype_code(self):
        text = """``` code
        block```"""
        type1 = block_to_blocktype(text)
        self.assertEqual(type1, BlockType.CODE)
    
    def test_block_to_blocktype_quote(self):
        text = """> to
>be
> or
>not
> to be"""
        type1 = block_to_blocktype(text)
        self.assertEqual(type1, BlockType.QUOTE)
    
    def test_block_to_blocktype_unordered(self):
        text = """- to
- be
- or
- not
- to be"""
        type1 = block_to_blocktype(text)
        self.assertEqual(type1, BlockType.UNORDERED_LIST)
    
    def test_block_to_blocktype_ordered(self):
        text = """1. to
2. be
3. or
4. not
5. to be"""
        type1 = block_to_blocktype(text)
        self.assertEqual(type1, BlockType.ORDERED_LIST)
    
    def test_block_to_blocktype_paragraph(self):
        text = """this is a regular
        paragraph"""
        type1 = block_to_blocktype(text)
        self.assertEqual(type1, BlockType.PARAGRAPH)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_unordered_list(self):
        md = """
- This is **bolded** paragraph
- text in a p
- tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>This is <b>bolded</b> paragraph</li><li>text in a p</li><li>tag here</li></ul><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_ordered_list_heading(self):
        md = """
1. This is **bolded** paragraph
2. text in a p
3. tag here

##### This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ol><li>This is <b>bolded</b> paragraph</li><li>text in a p</li><li>tag here</li></ol><h5>This is another paragraph with <i>italic</i> text and <code>code</code> here</h5></div>",
        )
    
    def test_blockquote(self):
        md = """
>This is **bolded** paragraph
> text in a p
>tag here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>This is <b>bolded</b> paragraph\ntext in a p\ntag here</blockquote></div>",
        )
    def test_title(self):
        text = """# header
text"""
        header = extract_title(text)
        self.assertEqual(header, "header")