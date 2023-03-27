# InformationRetrieval_Project
My first project in python for accessing and retrieve information from documents

main.py represents the main code , and myFunction.py represents the functions I made and used
to simplify some things for me. Still needs optimization.

  The first part represents extraction of the attributes . At this step I read the xml files from
my directory and extract the text from title tags , p (paragraphs) tags and code tags ( which refers
to the topics of the documents so I can classify them later). In this phase I store the text extracted
from documents in lists , I split each word from each sentence in every list, remove the special 
characters (!@#$%^&*()_+-={}[]|\:;\"'<>,.?/ ) and creating a dictionay which contains the words 
frequency in the document. Next, knowing each list of words (which represents the words from documents)
has the single appearance of a word , I add the word in a global list which contains each unique word from
all the documents processed. The idea is of comparing the frequency list of each document and this global list, knowing
that every single word has the same position in every list, only the frequency making the difference.
