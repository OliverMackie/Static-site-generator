from enum import Enum
from textnode import markdown_to_blocks, TextType, text_to_textnodes, text_node_to_html_node, TextNode
from parentnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_blocktype(text):
    if text[0] == "#":
        for i in range(1,6):
            if text[i] == " ":
                return BlockType.HEADING
            elif text[i] != "#":
                break
    elif text[0] == "`":
        if text[:3] == "```":
            if text[-1:-4:-1] == "```":
                return BlockType.CODE
    elif text[0] == ">":
        for i in range(1, len(text)):
            if (text[i] == "\n") and (text[i+1] != ">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif text[0:2] == "- ":
        for i in range(1, len(text)):
            if (text[i] == "\n") and (text[i+1:i+3] != "- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif text[0].isdigit():
        first_dot = True
        for i in range(1,len(text)):
            if text[i].isdigit() and first_dot:
                continue
            elif text[i:i+2] == ". " and first_dot:
                first_dot = False
                continue
            elif first_dot:
                return BlockType.PARAGRAPH
            elif text[i] == "\n":
                first_dot = True
                continue  
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

type_tag_dict = {BlockType.PARAGRAPH: "p", BlockType.UNORDERED_LIST: "ul", BlockType.ORDERED_LIST: "ol", BlockType.QUOTE: "blockquote"}

def markdown_to_html_node(text):
    parents = []
    children = []
    blocks = markdown_to_blocks(text)
    for block in blocks:
        blocktype = block_to_blocktype(block)
        if blocktype == BlockType.QUOTE:
            tag = type_tag_dict[blocktype]
            block = block.replace("> ", "")
            block = block.replace(">", "")
            children = block_to_children(block)
        if blocktype == BlockType.UNORDERED_LIST:
            tag = type_tag_dict[blocktype]
            block = block.replace("- ", "")
            lines = block.split("\n")
            for line in lines:
                line_children = block_to_children(line)
                node = ParentNode("li", line_children)
                children.append(node)
        if blocktype == BlockType.ORDERED_LIST:
            tag = type_tag_dict[blocktype]
            lines = block.split("\n")
            for line in lines:
                curr_line = line.split(". ", 1)
                line_children = block_to_children(curr_line[1])
                node = ParentNode("li", line_children)
                children.append(node)
        if blocktype == BlockType.HEADING:
            text = block.split(" ", 1)
            children = block_to_children(text[1])
            tag = f"h{len(text[0])}"
        if blocktype == BlockType.CODE:
            tag = "pre"
            text = block.replace("```", "")
            text = text.lstrip("\n")
            node = TextNode(text, TextType.CODE_TEXT)
            node = text_node_to_html_node(node)
            children.append(node)
        if blocktype == BlockType.PARAGRAPH:
            tag = "p"
            block = block.replace("\n", " ")
            children = block_to_children(block)
        parents.append(ParentNode(tag, children))
        children = []
    return ParentNode("div", parents)

def block_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children