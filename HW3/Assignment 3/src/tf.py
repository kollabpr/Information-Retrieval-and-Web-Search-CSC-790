#!/usr/bin/python
import numpy as np
import os
import re
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
cachedStopwords = stopwords.words("english")
pattern = re.compile(r'\b(' + r'|'.join(cachedStopwords) + r')\b\s*')
tk = nltk.RegexpTokenizer(r"\w+")

def _calculate_term_freq(term, docs_path):
	"""returns map of file:count for a given term
	"""
	doc2tf_map = {}
	for doc in os.listdir(docs_path):
		if doc.endswith(".txt"):
			count = 0
			for word in tk.tokenize(pattern.sub('',open(docs_path + "/" + doc).read().lower())):
				if word == term:
					count += 1
			doc2tf_map[doc] = count

	return doc2tf_map

def _make_vocab(docs_path):
	vocab = []
	for doc in tqdm(os.listdir(docs_path)):
		if doc.endswith(".txt"):
			for word in set(tk.tokenize(pattern.sub('',open(docs_path + "/" + doc).read().lower()))):
				if word not in vocab:
					vocab.append(word)
	return vocab

def make_tf_vectors(docs_path, vocab):
	"""returns tf vectors for each doc
	"""
	doc2tf_maps = {}
	vectors = {}

	print()
	print("MAKING TF VECTORS")

	for doc in tqdm(os.listdir(docs_path)):
		if doc.endswith(".txt"):
			_vector = np.zeros(len(vocab))
			words = set(tk.tokenize(pattern.sub('',open(docs_path + "/" + doc).read().lower())))

			for word in words:
				if word not in list(doc2tf_maps.keys()):
					_doc2tf_map = _calculate_term_freq(word, docs_path)
					_vector[vocab.index(word)] = _doc2tf_map[doc]/(sum(list(_doc2tf_map.values())))
					doc2tf_maps[word] = _doc2tf_map
				else:
					_vector[vocab.index(word)] = doc2tf_maps[word][doc]/(sum(list(doc2tf_maps[word].values())))

			vectors[doc] = _vector

	return vectors

if __name__=="__main__":
	import pickle
	print("MAKING VOCAB")
	vocab = _make_vocab("../documents")
	pickle.dump(vocab, open("../assets/vocab.pickle", "wb"))
	pickle.dump(make_tf_vectors("../documents", vocab), open("../assets/tf_vectors.pickle", "wb"))
