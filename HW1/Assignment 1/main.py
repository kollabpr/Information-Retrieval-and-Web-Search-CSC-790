import pickle
import os
import json

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer as ps
stemmer = ps()

punctuation = ['?', ',', '!', '.', '-', ':', ';', '/', chr(8216), chr(8217), chr(8220), chr(8221), '(', ')']

document_ids = dict()
id = 1
with os.scandir("/Users/preetham/Desktop/Assignment/documents") as directory:
    for file in directory:
        if file.name.endswith(".txt"):
            document_ids[id] = file.name
            id=id+1
            print("file name --> ",file.name," doc id --> ", id)

def create_inverted_index():
    inverted_index = dict()
    for i in range(1,id):
        path = '/Users/preetham/Desktop/Assignment/documents/' + document_ids[i]
        with open(path, encoding="utf8") as f:
            tokens = f.read().replace("\n", " ")
        tokens = word_tokenize(tokens)
        print("Tokenizing file at: ",path)

        stop_words = list(stopwords.words("english"))
        unique_words = [word for word in tokens if word.casefold() not in stop_words]

        unique_words = [word for word in unique_words if word not in punctuation]
        
        stemmer = ps()
        stemmed_words = [stemmer.stem(word) for word in unique_words]

        for word in stemmed_words:
            if word not in list(inverted_index.keys()):
                inverted_index[word] = [1, i]
            else:
                inverted_index[word][0] += 1
                if inverted_index[word][-1] != i:
                    inverted_index[word].append(i)

    #print(inverted_index)
    with open('index.txt', 'w') as f:
        f.write(json.dumps(inverted_index))
 
    with open('inverted_dictionary', 'wb') as outfile:
        pickle.dump(inverted_index, outfile)            

def tokenize_query(phrase):
    query = word_tokenize(phrase)
    return query 

def search_word(term, invert_index):
    for key in invert_index.keys():
        if key == term: 
        # key == term[:len(key)]
            return invert_index[key][1:]
    return []

def and_operator(posting1, posting2):
    len1, len2 = len(posting1), len(posting2)
    intersection = []
    i, j = 0, 0
    while i < len1 and j < len2:
        if posting1[i] == posting2[j]:
            intersection.append(posting1[i])
            i+=1
            j+=1
        elif posting1[i] < posting2[j]:
            i+=1
        elif posting1[i] > posting2[j]:
            j+=1
    return intersection

def or_operator(posting1, posting2):
    return list(set(posting1 + posting2))

def not_operator(term, invert_index):
    posting = search_word(term, invert_index)
    return [i for i in range(1,6) if i not in posting]

def show_size():
    size = os.path.getsize('/Users/preetham/Desktop/Assignment/index.txt') 
    print('Size of file is: ', size, 'bytes')

def build_index():
    try:
        with open('inverted_dictionary', 'rb') as infile:
            inv_index = pickle.load(infile)
    except:
        print("Creating index file!")
        create_inverted_index()
        with open('inverted_dictionary', 'rb') as infile:
            inv_index = pickle.load(infile)
    return inv_index

def boolean_operations(wordbag, index):
    posting, i = [], 0
    if 'AND' not in wordbag and 'OR' not in wordbag:
        if wordbag[0] == 'NOT':
            return not_operator(stemmer.stem(wordbag[1]), index)
        else:
            return search_word(stemmer.stem(wordbag[0]), index)
    else:
        if 'OR' in wordbag:
            val = 0
        elif 'AND' in wordbag:
            val = 1
        while i < len(wordbag):
            if wordbag[i] == 'NOT':
                posting_n = not_operator(stemmer.stem(wordbag[i+1]), index)
                i+=3
            else:
                posting_n = search_word(stemmer.stem(wordbag[i]), index)
                if i == 0:
                    posting = or_operator(posting, posting_n)
                i+=2
            if val == 0:
                posting = or_operator(posting, posting_n)
            elif val == 1:
                posting = and_operator(posting, posting_n)
        return posting

def print_index():
    index = build_index()
    print(index)

def run_query():
    index = build_index()
    query = input()
    query= tokenize_query(query)
    if '(' in query:
        index_close = query.index(')')
        chunk = query[1:index_close]
        words = query[index_close+2:]
        posting_chunk = boolean_operations(chunk, index)
        posting_words = boolean_operations(words, index)
        if query[index_close+1] == 'OR':
            return or_operator(posting_chunk, posting_words)
        elif query[index_close+1] == 'AND':
            return and_operator(posting_chunk, posting_words)
    else:
        return boolean_operations(query, index)


while True:
    print(" 1. Enter Boolean Query\n 2. Display size of inverted index file\n 3. Print the inverted index\n 4. Exit")
    user_input = int(input())
    if user_input == 1:
        result = run_query()
        for i in result:
            print(document_ids[i], end = '\n')
    elif user_input == 2:
        show_size()
    elif user_input == 3:
        print_index()
    elif user_input == 4:
        exit()