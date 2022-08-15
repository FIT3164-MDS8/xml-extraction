# importing element tree under the alias of ET
import xml.etree.ElementTree as ET
from lxml import etree

# import os
import os


def recc_read_root(r, root_tag=""):
    f = open("output.txt", "a")

    arr = p["abstract", "body", "title"]

    if root_tag == "":
        for c in r:
            recc_read_root(c, r.tag)
    elif len(r) > 0:
        f.write(root_tag + "; " + r.tag + " : ")
        if r.text != None:
            f.write(r.text + "\n")
        for c in r:
            recc_read_root(c, root_tag + "; " + r.tag)
    else:
        f.write(root_tag + "; " + r.tag + " : ")
        if r.text != None:
            f.write(r.text + "\n")
        print(root_tag + "; " + r.tag, end=" : ")
        print(r.text)

# recc_read_root(root)


def read_text(root):
    return "".join(root.itertext())


def read_tag(root, tagname, outputFileName):

    q = open("output//"+outputFileName + ".txt", "a", encoding="utf-8")

    for tags in root.iter(tagname):
        # print(read_text(tags))
        q.write(read_text(tags) + "\n")

# Code sample to get all title text in documents
# def get_title():

#     # print(os.getcwd())
#     # print(os.getcwd())
#     os.chdir('xml-1000\\')

#     # List ALL files in "xml-1000" directory
#     file_list = os.listdir()
#     # print(file_list)

#     for docName in file_list:
        
#         if os.path.isfile(docName):

#             # Passing the path of the xml document to enable the parsing process
#             tree = ET.parse(docName, etree.XMLParser(recover=True))

#             # getting the parent tag of the xml document
#             root = tree.getroot()

#             read_tag(root, "title", docName.split(".")[2])
        
#         else:
#             print("file ignore: " + docName)
#             # fstr = "journal.pone.0001458.xml"
#             # tree = ET.parse("xml-1000//" + docName)
#             # print(str.split(".")[2])


def get_tags_text(tagname):
    
    file_list = os.listdir()
    for docName in file_list:      
        if os.path.isfile(docName):
            tree = ET.parse(docName, etree.XMLParser(recover=True))
            root = tree.getroot()
            read_tag(root, tagname, docName.split(".")[2])
        else:
            print("file ignore: " + docName)


def main():
    os.chdir('xml-1000\\')
    get_tags_text("article-title")
    get_tags_text("title")

main()