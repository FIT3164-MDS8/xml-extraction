# from bs4 import BeautifulSoup

# # Reading the data inside the xml
# # file to a variable under the name
# # data
# with open('test.xml', 'r') as f:
#     data = f.read()

# # Passing the stored data inside
# # the beautifulsoup parser, storing
# # the returned object
# Bs_data = BeautifulSoup(data, "xml")
 
# # print(Bs_data)

# # # Finding all instances of tag
# # # `unique`
# b_unique = Bs_data.find_all('contrib')
 
# print(b_unique)
 
# # # Using find() to extract attributes
# # # of the first instance of the tag
# # b_name = Bs_data.find('child', {'name':'Frank'})
 
# # print(b_name)
 
# # # Extracting the data stored in a
# # # specific attribute of the
# # # `child` tag
# # value = b_name.get('test')
 
# # print(value)


# importing element tree
# under the alias of ET
import xml.etree.ElementTree as ET
 
# Passing the path of the
# xml document to enable the
# parsing process

# tree = ET.parse('test.xml')
# tree = ET.parse('journal.pbio.1000147.xml')
tree = ET.parse('journal.pbio.1000231.xml')

# getting the parent tag of
# the xml document
root = tree.getroot()

# for child in root:
#     print(child.tag, child.text, len(child))

# printing the root (parent) tag
# of the xml document, along with
# its memory location
# print(len(root))
 
# printing the attributes of the
# first tag from the parent
# print(root[0].attrib)
 
# printing the text contained within
# first subtag of the 5th tag from
# the parent
# print(root[5][0].text)

# def recc_read_root(r):
#     if len(r) > 0:
#         for c in r:
#             recc_read_root(c)
#     else:
#         print(r.tag, end= " : ")
#         print(r.text)


    

def recc_read_root(r, root_tag = ""):
    f = open("output.txt", "a")

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
        # print(root_tag + "; " + r.tag, end= " : ")
        # print(r.text)

recc_read_root(root)