#!/usr/bin/env python
# coding: utf-8
#By: Kollabathula Preetham
# In[2]:


import numpy as np
import re
import math
import os
import glob, os
import pickle
from os.path import exists
from pathlib import Path

BASE = os.getcwd()
print(BASE)
PNAME = "pickle.pkl"
PPATH = BASE + "/" + PNAME

docspath=BASE+"/documents"
l = os.listdir(docspath) # dir is your directory path
number_files = len(l)

pickle_file_exists = exists(PPATH)
if pickle_file_exists:
    print("Output from Pickle File")
    file_to_read = open("pickle.pkl", "rb")
    loaded_dictionary = pickle.load(file_to_read)
    document_Matrix = loaded_dictionary['document_Matrix']
    termDocuemnt_Matrix = loaded_dictionary['termDocument_Matrix']
    doc_Prob = loaded_dictionary['doc_Prob']
    Indices = loaded_dictionary['Indices']
    for i in range(len(Indices)): 
        print("RSV " + "{"+document_Matrix[Indices[i],0]+"}"+" = "+str(doc_Prob[Indices[i]])+"    "+document_Matrix[Indices[i],2])

else:
    numberOfSearchesToShow = 10

    with open("query.txt",'r')as f:
        a = f.read()
    query= []
    for term in a.split():
        t = re.sub(r"[^a-zA-Z0-9]","",term)
        query.append(t)
    print(query)


    # In[ ]:
    ALLDOCS="all_docs.txt"
    ALL_DOCS_PATH=BASE+"/"+ALLDOCS

    def create_file(line,file,dir):
        print("Appending to all_docs.txt")
        with open (dir,"r") as f:
            text = f.read()
        with open("all_docs.txt","a") as txt:
            regex = re.compile(r'\d+')
            ab = [int(x) for x in regex.findall(file)]
            ab = ab[0]-1
            ab = "file" +"_"+ str(ab) +"_0"
            txt.write(line+file +"\n"+ text + "\n")

    alldocs_file_exists = exists(ALL_DOCS_PATH)
    print(alldocs_file_exists)

    if not alldocs_file_exists: 
        total_files = 0
        docx=BASE+"/documents"
        for file in os.listdir(docx):
            if file.endswith(".txt"):
                total_files += 1
                file_path = f"{docx}/{file}"
                print(file_path)
                with open ("file_label.txt", "r") as l:
                    num =Path(file_path).stem
                    for line in l :
                        matched = re.search(r'^([^,])+', line) # find results      
                        #print("num is: "+num+" matched[0]: "+matched[0])
                        if num == matched[0]:
                            create_file(line,file,file_path)
        #print(total_files)


    # In[5]:


    #reading the file and storing the documetns
    file = open("all_docs.txt")
    documentMatrix = np.full((number_files,3), dtype=object, fill_value = "empty")
    documentCount = 0
    index = 0
    for line in file:
        if documentCount>=number_files:
            break
        if line in ['\n','\r\n']:
            documentCount = documentCount + 1
            index = 0
        else:
            index = index + 1    
        if index == 1:
            documentMatrix[documentCount,2] = line
        elif index == 2:
            documentMatrix[documentCount,0] = line
        elif index == 3:
            documentMatrix[documentCount,1] = line
    documentMatrix


    # In[6]:



    ##cleaning text code
    for i in range(documentMatrix.shape[0]):
        for j in range(documentMatrix.shape[1]):
    #         documentMatrix[i,j] = re.sub(r'[^\w\s_]+', '', documentMatrix[i,j]).strip()
            documentMatrix[i,j] = documentMatrix[i,j].lower()
    documentMatrix = documentMatrix.astype(str)
    #print(documentMatrix)
    documentMatrix2 = np.full((number_files), dtype=object, fill_value = "empty")
    for i in range(len(documentMatrix)):
        documentMatrix2[i] = documentMatrix[i,1] + " " + documentMatrix[i, 2]
    documentMatrix2 = documentMatrix2.astype(str)
    #print(documentMatrix2)
    documents = list(documentMatrix2)
    documentMatrix2 = None
    #print(len(documents))


    # In[7]:


    #collect all words in the all documents
    bagOfWords = []
    for line in documents:
        for word in line.split():
            word = re.sub(r"[^a-zA-Z0-9]","",word)
            word = word.lower()
            if word not in bagOfWords:
                bagOfWords.append(word)

    #instantiate term document matrix of appropriate size with zeros
    termDocumentMatrix = np.zeros((len(documents), len(bagOfWords)), dtype = 'int8')
    #print(len(bagOfWords))


    # In[8]:


    ##populate term document matrix
    for i in range(len(documents)):
        docWordList = documents[i].split();
        
        for t in range(len(docWordList)):
            docWordList[t] = re.sub(r"[^a-zA-Z0-9]","",docWordList[t])
            docWordList[t] = docWordList[t].lower()

        
        for j in range(len(bagOfWords)):
            if bagOfWords[j] in docWordList:
                termDocumentMatrix[i,j] = 1

    #print(termDocumentMatrix[1])


    # In[ ]:


    #calculate dft of each term and calculate its weight "w"
    n = len(documents)
    dft = np.zeros((len(bagOfWords)))
    weight = np.zeros((len(bagOfWords)))

    for i in range(len(bagOfWords)):
        for j in range(len(documents)):
            if termDocumentMatrix[j,i] == 1:
                dft[i] = dft[i] +1 
        weight[i] = math.log(n/dft[i], 2)


    # In[ ]:


    #calculating the retrieval status value of each doc
    docProb = np.zeros((len(documents)))
    for q in query:
        termIndex = bagOfWords.index(q)
        for d in range(len(termDocumentMatrix)):
            if termDocumentMatrix[d, termIndex] == 1:
                docProb[d] = docProb[d] + weight[termIndex]


    # In[ ]:


    #displaying the results
    indices = docProb.argsort()[-numberOfSearchesToShow:][::-1]
    print("\n")
    for i in range(len(indices)):
        print("RSV " + "{"+documentMatrix[indices[i],0]+"}"+" = "+str(docProb[indices[i]])+"    "+documentMatrix[indices[i],2])
    #     print("Content:     " + documentMatrix[indices[i],2])
    #     print("RSV:         " + str(docProb[indices[i]]))
    #    print("Terms found: ", end='')
    #    for j in range(len(termDocumentMatrix[indices[i]])):
    #        if termDocumentMatrix[indices[i], j] == 1 and bagOfWords[j] in query:
    #            print(bagOfWords[j] + ", ", end = '')
        print("\n")


    # In[ ]:
    print("Pickle File Created")
    dic = {
        'document_Matrix' : documentMatrix,
        'weight':weight,
        'termDocument_Matrix':termDocumentMatrix,
        'doc_Prob':docProb,
        'Indices':indices

    }
    pickle.dump(dic,open(PPATH,'wb'))

    

