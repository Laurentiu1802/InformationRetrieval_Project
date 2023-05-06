import numpy as np  #librarie pt a lucra cu array
import os           # modul pentru care detine functii pentru a interactiona cu SO in cazul in care lucram cu fisiere
import glob         #modul folosit pentru a cauta fisiere care se potrivesc unui pattern specific
import xml.etree.ElementTree as et #librarie care permite sa navigam prin fisierele xml
from collections import Counter
import json #pentru a converti lista de dictionare in stringuri JSON



def split_words(words_list):

    words=[]
    single_words_list=[]
    for index in range(len(words_list)):
        words.append(words_list[index].split())
    
    for index2 in words:
        for index3 in index2:
            single_words_list.append(index3)
                
    return single_words_list

def sort_dictionary(a_dictionary):
    myKeys=list(a_dictionary.keys())
    myKeys.sort()
    sorted_dict={i: a_dictionary[i] for i in myKeys}
    return sorted_dict
 
def words_frequency(words_list):
    words=Counter(words_list)
    return words

def extract_attribute(attrib_list):
    attribute_list=[]
    for sublist in attrib_list:
        extracted_words=[]
        for s in sublist:
            word=s.split(':')[1]
            extracted_words.append(word)
        attribute_list.append(extracted_words)
    return attribute_list

def get_directory(file_path):
    firedir=os.path.basename(os.path.dirname(file_path))
    return firedir


def write_output_into_txt_file(global_words_list,documents_list,attribute_list,directory_name):
    try:
        with open("d:/School/Sem2/Regasirea informatiei/output.txt","w") as file:
            document_index=0
            for global_word in global_words_list:
                file.write('@attribute '+ global_word + "\n")
            file.write("@data \n")
            for each_doc in documents_list:
                json_str=json.dumps(each_doc)
                file.write( "D" + str(document_index) + " # " + json_str + " # " +  str(attribute_list[document_index]) +' '+ directory_name + "\n")
                document_index+=1
    except Exception as e:
        print("Error: ", e)



