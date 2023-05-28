import numpy as np  #librarie pt a lucra cu array
import os           # modul pentru care detine functii pentru a interactiona cu SO in cazul in care lucram cu fisiere
import glob         #modul folosit pentru a cauta fisiere care se potrivesc unui pattern specific
import xml.etree.ElementTree as et #librarie care permite sa navigam prin fisierele xml
from collections import Counter
import json #pentru a converti lista de dictionare in stringuri JSON
from scipy.spatial.distance import euclidean
import math


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

def get_xml_filenames(folder_path):
        xml_filenames = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".xml"):
                xml_filenames.append(file_name)
        return xml_filenames


def write_output_into_txt_file(global_words_list,documents_list,attribute_list,directory_name):
    try:
        with open("d:/School/Sem2/Regasirea informatiei/output.txt","w") as file:
            document_index=0
            for global_word in global_words_list:
                file.write('@attribute '+ global_word + "\n")
            file.write("@data \n")
            for each_doc in documents_list:
                json_str=json.dumps(each_doc)
                file.write( "D" + str(document_index) + " # " + json_str + " # " +  str(attribute_list[document_index]) +' '+ str(directory_name[document_index]) + "\n")
                document_index+=1
    except Exception as e:
        print("Error: ", e)


    
def normalize_nominal_data(data):
    all_keys = set()
    for d in data:
        all_keys.update(d.keys())

    normalized_data = []
    for d in data:
        max_freq = np.max(list(d.values()))  # Calculăm valoarea maximă pentru dictionarul curent
        freq_values = np.array([d.get(key, 0) / max_freq for key in all_keys])
        normalized_dict = {key: value for key, value in zip(all_keys, freq_values)}
        normalized_data.append(normalized_dict)

    return normalized_data

def attribute_frequency(lista_dictionare):  
    key = set()
    for dictionar in lista_dictionare:
       key.update(dictionar.keys())

   
    rezultate = {}
    for cheie in key:
        aparitii = sum(1 for dictionar in lista_dictionare if cheie not in dictionar)
        rezultat=math.log10(len(lista_dictionare)/(len(lista_dictionare)-aparitii))
        rezultate[cheie] = rezultat
        #print(rezultat)

    return rezultate  

def build_word_frequency_dict(word_list, global_word_vector):
    word_frequency = {}

    for word in word_list:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1

    word_dict = {}
    for word in word_frequency:
        if word in global_word_vector:
            word_index = global_word_vector.index(word)
            word_dict[word_index] = word_frequency[word]

    return word_dict

def calculate_sqrt_sum_of_squares(dict_list):
    sqrt_sum_list = []

    for d in dict_list:
        sum_of_squares = sum(value ** 2 for value in d.values())
        sqrt_sum = math.sqrt(sum_of_squares)
        sqrt_sum_list.append(sqrt_sum)

    return sqrt_sum_list

def list_to_dictionary(value_list):
    dictionary = {}

    if len(value_list) == 1:
         for i, value in enumerate(value_list):
            key = "Q"
            dictionary[key] = value
    else:
        for i, value in enumerate(value_list):
            key = f"D{i}"
            dictionary[key] = value

    return dictionary

def calculate_norm_times_similarity(norm_list,sim_list,query_norm):
    result=[]
    q_norm=query_norm.values()
    q_norm2=list(q_norm)
    for key in norm_list:
        if key in sim_list:
            result.append(sim_list[key]/(norm_list[key]*q_norm2[0]))
    return result

def calculate_similarity(list_of_dicts1, list_of_dicts2):
    result_list = []

    single_dict = list_of_dicts2[0]  # Obține singurul dicționar din lista

    for d1 in list_of_dicts1:
        result = 0
        for key in d1:
            value1 = d1[key]
            value2 = single_dict.get(key, 0)  

            result += value1 * value2

        result_list.append(result)

    return result_list