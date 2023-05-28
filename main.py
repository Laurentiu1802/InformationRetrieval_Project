import numpy as np  #librarie pt a lucra cu array
import os           # modul pentru care detine functii pentru a interactiona cu SO in cazul in care lucram cu fisiere
import glob         #modul folosit pentru a cauta fisiere care se potrivesc unui pattern specific
import xml.etree.ElementTree as et #librarie care permite sa navigam prin fisierele xml
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize,word_tokenize
import myFunctions
import math
from scipy.spatial.distance import euclidean



ps=PorterStemmer()

#path_to_give="D:\School\Sem2\Regasirea informatiei\Reuters\Reuters_34\Testing\*.XML" 
path_to_give="D:\School\Sem2\Regasirea informatiei\Reuters\Reuters_34\Training\*.XML" 
#path_to_give="D:\School\Sem2\Regasirea informatiei\Reuters\Reuters_7083\*.XML"
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
attributes_unique=[]
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

    codes=root.find('.//metadata//codes[@class="bip:topics:1.0"]')
    code_attribute=[]
    for tag in codes:
        attr_value=tag.get('code')
        fcode.append(attr_value)
    
    documents_array.append(ftext)
    titles_array.append(ftitle)
    attributes.append(fcode)
    attributes_unique.append(fcode[0])


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
print(attributes)
#print("********************************")
#print(global_words_array)
#print("*********************************")
#print("stop words: ",stop_words_list)



print (len(global_words_array)) #cuvinte gasite


only_unique_attributes=list(set(attributes_unique))
count_list=[]
count_sum=0
for unique_attr in only_unique_attributes:
    count=attributes_unique.count(unique_attr)
    print(f'{unique_attr}:{count}')
    count_list.append(count)
    count_sum+=count

entropy = 0
entropy_total = 0
for entropy_sum in count_list:
    x = entropy_sum
    entropy = -(x / count_sum) * math.log((x / count_sum), 2) + entropy
   # entropy_total = entropy
   # print(f'{entropy_sum} : {entropy=}')
print(entropy)
   
print(count_sum)
print(only_unique_attributes)

global_word_counter=0
global_word_not_counter=0
gain=[]
for each_word in range(len(global_words_array)):
    for each_dict in documents:
        if each_word in each_dict.keys():
            global_word_counter+=1
        if each_word not in each_dict.keys():
            global_word_not_counter+=1
    gain.append(entropy-(global_word_counter/len(documents)))
    global_word_not_counter=0
    global_word_counter=0



#interrogation="A private company that provides online access to public record."
#interrogation="A major provider of Internet access to commercial services plans to add content and high-quality service."
#interrogation="Intranets are company-wide networks based on the Internet protocol."
#interrogation="Systems integrators and large corporations providing for "either clandestine side payments, discounts on the Microsoft desktop operating system."
#interrogation="The legal clash comes at a critical point as both Netscape and Microsoft are introducing new versions of their respective browsers."
#interrogation="It said Monday that more than one million users have downloaded its latest Internet Explorer version in its first week of availability."
#interrogation="Netscape and Microsoft are already well along the way to developing the next version of their browser software."
#interrogation="We think the company is extremely well positioned to take advantage of the opportunities in this nascent environment we're in, in both the consumer online Internet market as well as the Corporate Internet Services."
#interrogation="CompuServe has addressed subscriber declines by upgrading its infrastructure to improve speed and performance and is releasing a new software product."
#interrogation="New partnerships with IBM, Netscape Communications Corp, Microsoft Corp and Oracle Corp provide comprehensive intranet-hosting platforms."
#interrogation="In launching the latest version of Navigator, Mountain View, Calif.-based Netscape highlighted a new electronic mail feature that will deliver information from selected content providers directly to the user's computer ."
#interrogation="Microsoft also pointed out that its product is free, while Netscape charges most users a $49 license fee after a free 90-day trial period."
#interrogation="Microsoft officials said versions for previous versions of Windows and for Apple Computer Inc.'s Macintosh system were forthcoming."
#interrogation="Novell has been a leader since 1983 in conventional networking software but has fallen behind Netscape Communications Corp. and Microsoft Corp. in the competition for intranets, private networks which function like the Internet's Web."
#interrogation="The company said IntranetWare is compatible with existing Novell network software and will allow companies to preserve previous investments in network software. "
#interrogation="The company attributed the higher revenues to sales generated by BETA Inc and Modern Learning Press."
#interrogation="The early success is not leading the company to modify guidance for the full year yet, however."
#interrogation="The Department of Justice said it was reviewing Microsoft's acquisition of VXtreme Inc, a Silicon Valley developer of technology for sending audio and video over the Internet."
#interrogation="The technology is particularly useful to recording companies and movie studios that want to preview teasers and promotions on the Internet without compromising copyrights."
#interrogation="Microsoft is hoping its powerful brand name, an emphasis on breadth and depth of content and new "TutorAssist" technology will break through the clutter and appeal to busy parents eager to give their children an educational boost."
#interrogation="Deutsche Morgan Grenfell said on Friday it raised its rating on the shares of Bay Networks Inc to buy from accumulate."
interogation=input("What are you looking for?")
interogative_words=interogation.lower().split()
translation_table=str.maketrans('','',special_chars)
clean_interrogation=[word.translate(translation_table) for word in interogative_words if word not in stop_words_list]
cleaner_interrogation=[ps.stem(word) for word in clean_interrogation]
the_cleanest_interrogation = [word for word in cleaner_interrogation if len(word) > 2 and word.isalpha()]
print(the_cleanest_interrogation)
query=myFunctions.build_word_frequency_dict(the_cleanest_interrogation,global_words_array)




IDF=myFunctions.attribute_frequency(documents)
normalized_docs=myFunctions.normalize_nominal_data(documents)
normalized_dict=[]
for each_dict in normalized_docs:
    norm_dict_temp={k: IDF[k]* each_dict[k] for k in IDF.keys() & each_dict.keys()}
    normalized_dict.append(norm_dict_temp)

query_list=[]
query_list.append(query)
normalized_q=myFunctions.normalize_nominal_data(query_list)
normalized_query=[]

for each_q in normalized_q:
    norm_q_temp={k:IDF[k]* each_q[k] for k in IDF.keys() & each_q.keys()}
    normalized_query.append(norm_q_temp)
        
#print(normalized_dict)
#print(normalized_query)

doc_norm=myFunctions.list_to_dictionary(myFunctions.calculate_sqrt_sum_of_squares(normalized_dict))
query_norm=myFunctions.list_to_dictionary(myFunctions.calculate_sqrt_sum_of_squares(normalized_query))

similarity=myFunctions.list_to_dictionary(myFunctions.calculate_similarity(normalized_dict,normalized_query))
best_similarity=myFunctions.list_to_dictionary(myFunctions.calculate_norm_times_similarity(doc_norm,similarity,query_norm))
#print(best_similarity)

#Numele fisierelor xml
xml_filenames=[]
filenames=[]
for file_path in read_files:
    xml_filename=os.path.basename(file_path)
    inner_list=[xml_filename]
    xml_filenames.append(inner_list) #pentru a scrie in fisier
    filenames.append(xml_filename)

filenames=myFunctions.list_to_dictionary(filenames)

#print(filenames)
myFunctions.write_output_into_txt_file(global_words_array,documents ,attributes,xml_filenames)



doc_names=[item for sublist in titles_array for item in sublist]
doc_names=myFunctions.list_to_dictionary(doc_names)

most_relevant=dict(sorted(best_similarity.items(),key=lambda x:x[1],reverse=True)[:10]) #primele 10 documente relevante
for key,value in most_relevant.items():
    if key in filenames:
        print(f"Index: {key} -Titlu: {doc_names[key]} Numele documentului: {filenames[key]} -  Valoarea similaritatii: {value}")

