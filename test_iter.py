import xml.etree.ElementTree as ET
tree = ET.parse('journal.pone.0001458.xml')
for elem in tree.iter():
    print(elem.tag, elem.text)
        