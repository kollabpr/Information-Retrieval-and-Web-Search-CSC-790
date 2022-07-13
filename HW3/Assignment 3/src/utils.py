#!/usr/bin/python
import os
import re
from tqdm import tqdm
from nltk.corpus import stopwords
import nltk

cachedStopwords = stopwords.words("english")
pattern = re.compile(r'\b(' + r'|'.join(cachedStopwords) + r')\b\s*')

tk = nltk.RegexpTokenizer(r"\w+")

def count_terms_across_docs(docs_path):
	term_count = {}
	for doc in tqdm(os.listdir(docs_path)):
		if doc.endswith(".txt"):
			for word in tk.tokenize(pattern.sub('', open(docs_path + "/" + doc).read().lower())):

				if word not in list(term_count.keys()):
					term_count[word] = 1
				else:
					term_count[word] += 1
	return term_count

if __name__=="__main__":
	import pickle
	print("COUNTING TERMS")
	term_count = count_terms_across_docs("../documents")
	pickle.dump(term_count, open("../assets/term_count.pickle", "wb"))
