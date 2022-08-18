# importing element tree under the alias of ET
import xml.etree.ElementTree as ET
from lxml import etree

# import os
import os

# import nltk
# must first download required package of nltk to run with no errors
# nltk.download(packageName: or leave blank to UI)
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# import pandas.DataFrame
from pandas import DataFrame as df

# def recc_read_root(r, root_tag=""):
#     f = open("output.txt", "a")

#     arr = p["abstract", "body", "title"]

#     if root_tag == "":
#         for c in r:
#             recc_read_root(c, r.tag)
#     elif len(r) > 0:
#         f.write(root_tag + "; " + r.tag + " : ")
#         if r.text != None:
#             f.write(r.text + "\n")
#         for c in r:
#             recc_read_root(c, root_tag + "; " + r.tag)
#     else:
#         f.write(root_tag + "; " + r.tag + " : ")
#         if r.text != None:
#             f.write(r.text + "\n")
#         print(root_tag + "; " + r.tag, end=" : ")
#         print(r.text)

# recc_read_root(root)


def read_text(root):
    return "".join(root.itertext())


def read_tag(root, tagname, outputFileName=""):

    # q = open("output//"+outputFileName + ".txt", "a", encoding="utf-8")
    temp_str = ""

    for tags in root.iter(tagname):
        # print(read_text(tags))
        # q.write(read_text(tags) + "\n")
        temp_str += read_text(tags) + "\n"

    return temp_str


def read_section(root):

    sc_arr = [[], [], [], [], []]
    id = 0
    no_of_sec = count_body_sec(root)

    for tags in root.findall("body/sec"):

        raw_word_array = word_tokenize(read_text(tags))
        sc_arr[id%5].extend([w.casefold() for w in raw_word_array])
        id += 1

    return sc_arr


def check_sec_type(root, sec_type_name):
    for tags in root.findall(".//body//sec[@sec-type='" + sec_type_name +
                             "']"):
        return True
    return False


def count_body_sec(root):
    c = 0
    # for tags in root.findall(".//body//sec"):
    for tags in root.findall("body/sec"):
        # print(tags.tag, tags.attrib, end = "\t")
        c += 1
    return c


def count_abstract(root):
    c = 0
    # for tags in root.findall(".//body//sec"):
    for tags in root.iter("abstract"):
        # print(tags.tag, tags.attrib, end = "\t")
        c += 1
    return c


def read_abstract(root):
    # for tags in root.findall(".//body//sec"):
    temp = ""
    for tags in root.iter("abstract"):
        temp += read_text(tags) + " "

    raw_word_array = word_tokenize(temp)

    return [w.casefold() for w in raw_word_array]


def read_keyword(root):
    """
    A function that search for keywords from the article title of the document

    Args:
        root (???): the root of the xml tree

    Returns:
        _type_: _description_
    """
    stop_words = set(stopwords.words("english"))
    raw_title = read_tag(root, "title-group")
    raw_word_array = word_tokenize(raw_title)
    return filter_POS_tag(nltk.pos_tag([w.casefold() for w in raw_word_array]),
                          ["NN"])


def filter_POS_tag(tpl_arr, tags):
    """
    A function that loops the list of tuples with the format of (word, Part of speech tag)
    and append the word that fulfill the requirements

    Args:
        tpl_arr (list[strings]): the list of tuples with the format of (word, Part of speech tag)
        tags (list[strings]): a list that define part of the requirements.

    Returns:
        list: the list of of words that met the requirements.
    """
    ret_arr = []
    for tmp in tpl_arr:
        if tmp[1][:2] in tags and tmp[0] not in ret_arr and len(tmp[0]) > 2:
            ret_arr.append(tmp[0])
    return ret_arr


# Code sample to get all title text in documents
# def get_title():

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


def test_loop_doc():
    """
    A function that loops through all the document in the specific directory
    """

    file_list = os.listdir()
    for docName in file_list:
        if os.path.isfile(docName):
            tree = ET.parse(docName, etree.XMLParser(recover=True))
            root = tree.getroot()

            # print(docName, end=":\t")
            # print(read_abstract(root))

            # read keywords and append to dataframe with column named 'word'
            kw_df = df({'word': read_keyword(root)})

            # abstarct dataframe
            abs_df = df({'word': read_abstract(root)})
            abs_df = abs_df.groupby(['word']).size().reset_index(name='abstract_counts')

            # section dataframe

            # print(count_body_sec(root))
            
            sec_ret_list = read_section(root)

            sec_1_df = df({'word': sec_ret_list[0]})
            sec_2_df = df({'word': sec_ret_list[1]})
            sec_3_df = df({'word': sec_ret_list[2]})
            sec_4_df = df({'word': sec_ret_list[3]})
            sec_5_df = df({'word': sec_ret_list[4]})
            sec_1_df = sec_1_df.groupby(['word']).size().reset_index(name='section_1_counts')
            sec_2_df = sec_2_df.groupby(['word']).size().reset_index(name='section_2_counts')
            sec_3_df = sec_3_df.groupby(['word']).size().reset_index(name='section_3_counts')
            sec_4_df = sec_4_df.groupby(['word']).size().reset_index(name='section_4_counts')
            sec_5_df = sec_5_df.groupby(['word']).size().reset_index(name='section_5_counts')


            # perform join
            kw_df = kw_df.set_index('word').join(abs_df.set_index('word'), lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_1_df.set_index('word'), lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_2_df.set_index('word'), lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_3_df.set_index('word'), lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_4_df.set_index('word'), lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_5_df.set_index('word'), lsuffix='caller', rsuffix='other')
            kw_df.to_csv("./output/" + docName[:-4] + ".csv") # , index=False)

            # abs_df.groupby(['word'])['word'].count()

            # print(count_abstract(root))

            # print(count_body_sec(root), end=":\t")
            # print(check_sec_type(root, "intro"), end= "\t")
            # print(check_sec_type(root, "materials|methods"), end= "\t")
            # print(check_sec_type(root, "results"), end= "\t")
            # print(check_sec_type(root, "conclusions"))

            # read_section(root)

            # print(len(read_keyword(root)))
            # print(read_keyword(root))

        else:
            print("file ignore: " + docName)


def main():
    os.chdir('xml-1000\\')
    # get_tags_text("title-group")
    # get_tags_text("body")
    test_loop_doc()


main()