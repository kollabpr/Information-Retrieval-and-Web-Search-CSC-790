#!/usr/bin/python
import numpy as np
from tqdm import tqdm

def wf_idf(docs_path, wf_vectors, vocab):
	"""returns wfidf vectors for the docs
	"""
	print("MAKING VOCAB")
	idf_vector = np.zeros(len(vocab))
	doc_count = len(list(wf_vectors.keys()))

	print()
	print("MAKING THE IDF VECTOR")
	for word in tqdm(vocab):
		_docs_containing_word = 0 
		for doc in list(wf_vectors.keys()):
			if wf_vectors[doc][vocab.index(word)] != 0:
				_docs_containing_word += 1

		idf_vector[vocab.index(word)] = np.log10(doc_count/(1 + _docs_containing_word))

	wf_idf_vectors = {}

	print()
	print("MAKING WFIDF VECTORS")
	for doc in tqdm(list(wf_vectors.keys())):
		wf_idf_vectors[doc] = wf_vectors[doc]*idf_vector
	
	return wf_idf_vectors

if __name__=="__main__":
	import pickle
	wf_vectors = pickle.load(open("../assets/wf_vectors.pickle", "rb"))
	vocab = pickle.load(open("../assets/vocab.pickle", "rb"))
	pickle.dump(wf_idf("../documents", wf_vectors, vocab), open("../assets/wfidf_vectors.pickle", "wb"))
