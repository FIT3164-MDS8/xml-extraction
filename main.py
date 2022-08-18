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


def read_text(root):
    """ A function that converts an object to return a string.

    Args:
        root (xml.etree.ElementTree): the root node of the tree/subtree

    Returns:
        str: _description_
    """

    return "".join(root.itertext())


def read_tag(root, tagname, outputFileName=""):
    """ A function that take the root node and search for the tag (tagname) and return the texts as string.

    Args:
        root (xml.etree.ElementTree): the root node of the xml tree
        tagname (str): the tag name to search in the tree
        outputFileName (str, optional): use only for checking process. Defaults to "".

    Returns:
        str: all the texts for the specific tag
    """
    # q = open("output//"+outputFileName + ".txt", "a", encoding="utf-8")
    temp_str = ""

    for tags in root.iter(tagname):
        # q.write(read_text(tags) + "\n")
        temp_str += read_text(tags) + "\n"

    return temp_str


def read_section(root):
    """ A function that get all the child node of body with tag 'sec' and append text in it to a list of spilted words.
    All texts in tag 'sec' will be separated to 5 different section using hash.

    Args:
        root (xml.etree.ElementTree): the root node of the xml tree

    Returns:
        [[str]...]: A nested list with 5 inner list filled with texts in 1 parent list
    """
    sc_arr = [[], [], [], [], []]
    id = 0
    no_of_sec = count_body_sec(root)

    for tags in root.findall("body/sec"):

        raw_word_array = word_tokenize(read_text(tags))
        sc_arr[id % 5].extend([w.casefold() for w in raw_word_array])
        id += 1

    return sc_arr


def check_sec_type(root, sec_type_name):
    """ A function that return True when stated sec-type exists else False.

    Args:
        root (xml.etree.ElementTree): the root node of the xml tree
        sec_type_name (str): section type name, i.e. [intro, materials|methods, results, conclusions]

    Returns:
        boolean: return True if tag's attribute sec-type exist else return False
    """
    for tags in root.findall(".//body//sec[@sec-type='" + sec_type_name +
                             "']"):
        return True
    return False


def count_body_sec(root):
    """ A function that count the number of ('sec') nodes in xml tree ('article/body').

    Args:
        root (xml.etree.ElementTree): the root node of the xml tree

    Returns:
        int: the count of sections in the body of xml tree
    """

    c = 0
    # for tags in root.findall(".//body//sec"):
    for tags in root.findall("body/sec"):
        # print(tags.tag, tags.attrib, end = "\t")
        c += 1
    return c


def count_abstract(root):
    """ A function that count the number of ('abstract') nodes in xml tree.

    Args:
        root (xml.etree.ElementTree): the root node of the xml tree

    Returns:
        int: the count of abstract in the xml tree
    """
    c = 0
    for tags in root.iter("abstract"):
        c += 1
    return c


def read_abstract(root):
    """ A function that search for <abstract> tag in the xml file and return a list of the processed words.

    Args:
        root (xml.etree.ElementTree): the root node of the xml tree

    Returns:
        [str]: a list of pre-processed words
    """
    temp = ""
    for tags in root.iter("abstract"):
        temp += read_text(tags) + " "

    raw_word_array = word_tokenize(temp)

    return [w.casefold() for w in raw_word_array]


def read_keyword(root):
    """
    A function that search for keywords from the article title of the document

    Args:
        root (xml.etree.ElementTree): the root node of the xml tree

    Returns:
        [str...]: a list of keywords
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
        tpl_arr ([str...]): the list of tuples with the format of (word, Part of speech tag)
        tags ([str...]): a list that define part of the requirements.

    Returns:
        [str...]: the list of of words that met the requirements.
    """
    ret_arr = []
    for tmp in tpl_arr:
        if tmp[1][:2] in tags and tmp[0] not in ret_arr and len(tmp[0]) > 2:
            ret_arr.append(tmp[0])
    return ret_arr


def get_tags_text(tagname):
    """ A DEPRECATED function that loops through all the document

    Args:
        tagname (str): the tag to search for in the xml file
    """
    file_list = os.listdir()
    for docName in file_list:
        if os.path.isfile(docName):
            tree = ET.parse(docName, etree.XMLParser(recover=True))
            root = tree.getroot()
            read_tag(root, tagname, docName.split(".")[2])
        else:
            print("file ignore: " + docName)


def dataframe_join():
    """
    A function that loops through all the document for all the process
    Output the final DataFrame to a csv file with the initial filename with .csv instead of .xml
    """

    file_list = os.listdir()
    for docName in file_list:

        if os.path.isfile(docName):

            tree = ET.parse(docName, etree.XMLParser(recover=True))
            root = tree.getroot()

            # read keywords and convert to dataframe with column named 'word'
            kw_df = df({'word': read_keyword(root)})

            # abstarct dataframe creation with count group by words
            abs_df = df({'word': read_abstract(root)})

            abs_df = abs_df.groupby(['word']).size(
            ).reset_index(name='abstract_counts')

            # section dataframe creations with count group by words

            sec_ret_list = read_section(root)

            sec_1_df = df({'word': sec_ret_list[0]})
            sec_2_df = df({'word': sec_ret_list[1]})
            sec_3_df = df({'word': sec_ret_list[2]})
            sec_4_df = df({'word': sec_ret_list[3]})
            sec_5_df = df({'word': sec_ret_list[4]})

            sec_1_df = sec_1_df.groupby(['word']).size(
            ).reset_index(name='section_1_counts')
            sec_2_df = sec_2_df.groupby(['word']).size(
            ).reset_index(name='section_2_counts')
            sec_3_df = sec_3_df.groupby(['word']).size(
            ).reset_index(name='section_3_counts')
            sec_4_df = sec_4_df.groupby(['word']).size(
            ).reset_index(name='section_4_counts')
            sec_5_df = sec_5_df.groupby(['word']).size(
            ).reset_index(name='section_5_counts')

            # perform join operation
            kw_df = kw_df.set_index('word').join(
                abs_df.set_index('word'), lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_1_df.set_index('word'),
                               lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_2_df.set_index('word'),
                               lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_3_df.set_index('word'),
                               lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_4_df.set_index('word'),
                               lsuffix='caller', rsuffix='other')
            kw_df = kw_df.join(sec_5_df.set_index('word'),
                               lsuffix='caller', rsuffix='other')
            kw_df.to_csv("./output/" + docName[:-4] + ".csv") 

        else:
            print("file ignore: " + docName)


def main():
    os.chdir('xml-1000\\')
    
    try:
        os.mkdir('output')
    except OSError as error:
        print(error)
    
    dataframe_join()


main()
