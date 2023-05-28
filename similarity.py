# Lista de dictionare
import math
import numpy as np

def attribute_frequency(lista_dictionare):  
# Determinarea tuturor cheilor din dictionare
    chei = set()
    for dictionar in lista_dictionare:
       chei.update(dictionar.keys())

    # Numărarea aparițiilor cheilor lipsă în dictionare
    rezultate = {}
    for cheie in chei:
        aparitii = sum(1 for dictionar in lista_dictionare if cheie not in dictionar)
        rezultat=math.log10(len(lista_dictionare)/(len(lista_dictionare)-aparitii))
        rezultate[cheie] = rezultat
        #print(rezultat)

    return rezultate

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

def calculate_sqrt_sum_of_squares(dict_list):
    sqrt_sum_list = []

    for d in dict_list:
        sum_of_squares = sum(value ** 2 for value in d.values())
        sqrt_sum = math.sqrt(sum_of_squares)
        sqrt_sum_list.append(sqrt_sum)

    return sqrt_sum_list

lista_dictionare = [
    {0: 1, 1: 1, 2: 2,3:1,6:1},
    {0:1, 4: 1,6:1},
    {1:1,2: 1, 3: 1, 5:1,6:1},
]
normalized_dict=[]

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


x=attribute_frequency(lista_dictionare)
y=normalize_nominal_data(lista_dictionare)

for each_dict in y:
    norm_dict_temp={k: x[k]* each_dict[k] for k in x.keys() & each_dict.keys()}
    normalized_dict.append(norm_dict_temp)
print(normalized_dict)

normalized_q=[]
query=[{2:1,3:1,4:1}]
q=normalize_nominal_data(query)
for each_q in q:
    norm_q_temp={k:x[k]* each_q[k] for k in x.keys() & each_q.keys()}
    normalized_q.append(norm_q_temp)
print("*****")
print(normalized_q)

norma=calculate_sqrt_sum_of_squares(normalized_dict)
#print(norma)

query_norm=calculate_sqrt_sum_of_squares(normalized_q)
#print(query_norm)

norma2=list_to_dictionary(calculate_sqrt_sum_of_squares(normalized_dict))
querynorm2=list_to_dictionary(calculate_sqrt_sum_of_squares(normalized_q))
#print(norma2)
#print(querynorm2)

similarity=list_to_dictionary(calculate_similarity(normalized_dict,normalized_q))
print(similarity)
#print(normalized_dict)

def calculate_norm_times_similarity(norm_list,sim_list,query_norm):
    result=[]
    q_norm=query_norm.values()
    q_norm2=list(q_norm)
    for key in norm_list:
        if key in sim_list:
            result.append(sim_list[key]/(norm_list[key]*q_norm2[0]))
    return result

the_best_similarity=list_to_dictionary(calculate_norm_times_similarity(norma2,similarity,querynorm2))
#print(the_best_similarity)