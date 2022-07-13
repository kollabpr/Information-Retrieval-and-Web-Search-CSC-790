#!/usr/bin/python
import numpy as np
import os
import re
from tqdm import tqdm
from tf import _calculate_term_freq
import nltk
from nltk.corpus import stopwords

cachedStopwords = stopwords.words("english")
pattern = re.compile(r'\b(' + r'|'.join(cachedStopwords) + r')\b\s*')

tk = nltk.RegexpTokenizer(r"\w+")

def make_wf_vectors(docs_path, vocab):
	"""returns wf vectors for each doc
	"""
	doc2tf_maps = {}
	vectors = {}

	print()
	print("MAKING WF VECTORS")

	for doc in tqdm(os.listdir(docs_path)):
		if doc.endswith(".txt"):
			_vector = np.zeros(len(vocab))
			words = set(tk.tokenize(pattern.sub('',open(docs_path + "/" + doc).read().lower())))

			for word in words:
				if word not in list(doc2tf_maps.keys()):
					_doc2tf_map = _calculate_term_freq(word, docs_path)
					_tf = _doc2tf_map[doc]/(sum(list(_doc2tf_map.values())))
					_vector[vocab.index(word)] =  1 + np.log10(_tf) if _tf > 0 else 0
					doc2tf_maps[word] = _doc2tf_map
				else:
					_tf = doc2tf_maps[word][doc]/(sum(list(doc2tf_maps[word].values())))
					_vector[vocab.index(word)] = 1 + np.log10(_tf) if _tf > 0 else 0

			vectors[doc] = _vector

	return vectors

if __name__=="__main__":
	import pickle
	vocab = pickle.load(open("../assets/vocab.pickle", "rb"))
	pickle.dump(make_wf_vectors("../documents", vocab), open("../assets/wf_vectors.pickle", "wb"))
