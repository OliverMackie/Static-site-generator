from textnode import TextNode, TextType
from parentnode import ParentNode
from leafnode import LeafNode
from copy_content import copy_content
import os
from copy_content import generate_page, generate_page_recursive

def main():
    copy_content(
    os.path.expanduser("~/workspace/boot.dev/static-site-generator/public"),
    os.path.expanduser("~/workspace/boot.dev/static-site-generator/static"),
)
    generate_page_recursive(
    os.path.expanduser("~/workspace/boot.dev/static-site-generator/content"),
    os.path.expanduser("~/workspace/boot.dev/static-site-generator/template.html"),
    os.path.expanduser("~/workspace/boot.dev/static-site-generator/public")
)

main()