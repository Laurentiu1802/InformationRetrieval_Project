import numpy as np  #librarie pt a lucra cu array
import os           # modul pentru care detine functii pentru a interactiona cu SO in cazul in care lucram cu fisiere
import glob         #modul folosit pentru a cauta fisiere care se potrivesc unui pattern specific
import xml.etree.ElementTree as et #librarie care permite sa navigam prin fisierele xml
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize,word_tokenize
import myFunctions

ps=PorterStemmer()

path_to_give="D:\School\Sem2\Regasirea informatiei\Reuters\Reuters_34\Testing\*.XML" #D:\School\Sem2\Regasirea informatiei\Reuters\Reuters_7083
read_files=glob.glob(path_to_give) #se citesc fisirele xml din folderul Testing
read_stop_words=open("D:\School\Sem2\Regasirea informatiei\stopwords.txt","r") 

stop_words_into_list=read_stop_words.read()
stop_words_list=stop_words_into_list.split("\n")

dir_name=myFunctions.get_directory(path_to_give) #numele fisierului din care afisam

global_words_array=[]
documents_array=[]
titles_array=[]
word_frequency=[]
word_list=[]
word_list_temp=[]
attributes=[]
for filename in read_files: #iteram prin fiecare fisier
    ftitle=[] #listele in care inregistram valorile
    ftext=[]
    fcode=[]
    tree=et.parse(filename) #se analizeaza fisierul xml in obiectul 'tree' 
    root=tree.getroot()     #accesam radacina fisierului analizat

    for title in root.iter('title'):  #folosind root iteram in fisier si salvam valorile in liste
        ftitle.append(title.text.lower())

    for itext in root.iter('p'):
        ftext.append(itext.text.lower())

    codes=root.findall('.//code')
    code_attribute=[]
    for tag in codes:
        attr_value=tag.get('code')
        fcode.append(attr_value)

    documents_array.append(ftext)
    titles_array.append(ftitle)
    attributes.append(fcode)


# topics=myFunctions.extract_attribute(attributes) #clasele

#desfacem propozitiile
for words in documents_array: # <-----------------------------------------aici schimbam inputul
    word_list_temp.append(myFunctions.split_words(words))

#scoatem caracterele speciale
special_chars = "!@#$%^&*()_+-={}[]|\:;\"'<>,.?/ "
word_frequency =[[word.translate(str.maketrans('','',special_chars)) for word in words if word not in stop_words_list]for words in word_list_temp]

#aplicam Porter_Stemmer pe fiecare cuvant din fiecare document
for each_document in range(len(word_frequency)):
    for each_word in range(len(word_frequency[each_document])):
        word_frequency[each_document][each_word]=ps.stem(word_frequency[each_document][each_word])

#frecventa cuvintelor
word_dictionary=[]
for x in range(len(word_frequency)):
    word_dictionary.append(Counter(word_frequency[x]))

#adauga lista cuvinte si frecventa sa intr-o lista
dictionary=[]
for index in range(len(word_dictionary)):
    dicty={element: count for element, count in word_dictionary[index].items()}
    dictionary.append(dicty)

#adaugam fiecare cuvant in lista globala de cuvinte
for x in range(len(dictionary)):
    for word in dictionary[x]:
        if word not in global_words_array  and word.isalpha() and len(word)>2 :
            global_words_array.append(word)

#aducem documentele la aceeasi dimensiune
#for x in range(len(dictionary)):
#    for words in global_words_array:
#        if words not in dictionary[x]:
#            dictionary[x][words]=0

#sortam documentele
documents=[]
for x in range(len(dictionary)):
    documents.append(myFunctions.sort_dictionary(dictionary[x]))
global_words_array.sort()

#vectori rari
for d in documents:
    updated_dict={}
    for word,freq in d.items():
        if word in global_words_array:
            updated_dict[global_words_array.index(word)]=freq # se creeaza din nou perechea key-value cu indexul cuvantului din 
       # else:                                                   #lista de cuvinte globale si ii se atribuie valoarea din fosta lista de frecvente
        #    updated_dict[word]=freq                               
    d.clear()
    d.update(updated_dict)

#print(attributes)  
print(documents)
#print("********************************")
#print(global_words_array)
#print("*********************************")
#print("stop words: ",stop_words_list)

myFunctions.write_output_into_txt_file(global_words_array,documents ,attributes,dir_name)

print (len(global_words_array)) #cuvinte gasite