from enum import Enum
from leafnode import LeafNode
import re

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return(self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(node):
        if node.text_type == TextType.PLAIN_TEXT:
            return LeafNode(None, node.text)
        elif node.text_type == TextType.BOLD_TEXT:
            return LeafNode("b", node.text)
        elif node.text_type == TextType.ITALIC_TEXT:
            return LeafNode("i", node.text)
        elif node.text_type == TextType.CODE_TEXT:
            return LeafNode("code", node.text)
        elif node.text_type == TextType.LINK:
            return LeafNode("a", node.text, {"href":node.url})
        elif node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src":node.url, "alt":node.text})
        else:
            raise ValueError("Invalid text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if delimiter in ["**", "_", "`"]:
        for node in old_nodes:
            if node.text_type != TextType.PLAIN_TEXT:
                new_nodes.append(node)
            elif node.text != None:
                split_list = node.text.split(delimiter)
                if len(split_list) % 2 == 0:
                    raise Exception(f"Invalid syntax, missing or extra {delimiter} symbol")
                for i in range(0,len(split_list)):
                    if (i % 2 == 0) and (split_list[i] != ""):
                        new_nodes.append(TextNode(split_list[i], TextType.PLAIN_TEXT))
                    elif split_list[i] != "":
                        new_nodes.append(TextNode(split_list[i], text_type))
    else:
        raise Exception(f"Invalid inline delimiter {delimiter}")
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes):
    i = 0
    store = []
    nodes = []
    for node in old_nodes:
        old_text = node.text
        links = extract_markdown_links(old_text)
        if len(links) == 0:
            nodes.append(TextNode(old_text, node.text_type, node.url))
        for link in links:
            texts = old_text.split(f"[{link[0]}]({link[1]})", 1)
            old_text = texts[1]
            store.append(texts[0])
            if link == links[-1]:
                store.append(texts[1])
        for text in store:
            if text != "" and text != None:    
                nodes.append(TextNode(text, node.text_type, node.url))
            if i < len(links):
                nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                i += 1
        store = []
    return nodes

def split_nodes_image(old_nodes):
        i = 0
        store = []
        nodes = []
        for node in old_nodes:
            old_text = node.text
            images = extract_markdown_images(old_text)
            if len(images) == 0:
                nodes.append(TextNode(node.text, node.text_type, node.url))
            for image in images:
                texts = old_text.split(f"![{image[0]}]({image[1]})", 1)
                old_text = texts[1]
                store.append(texts[0])
                if image == images[-1]:
                    store.append(texts[1])
            for text in store:
                if text != "" and text != None:    
                    nodes.append(TextNode(text, node.text_type, node.url))
                if i < len(images):
                    nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                    i += 1
            store = []
        return nodes

delim_to_texttype = {"**": TextType.BOLD_TEXT, "_": TextType.ITALIC_TEXT, "`": TextType.CODE_TEXT}

def text_to_textnodes(text):
    node = TextNode(text, TextType.PLAIN_TEXT)
    nodes = [node]
    for delim in ["**", "_", "`"]:
        nodes = split_nodes_delimiter(nodes, delim, delim_to_texttype[delim])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(text):
    final_blocks = []
    blocks = text.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        final_blocks.append(block.strip())
    return final_blocks