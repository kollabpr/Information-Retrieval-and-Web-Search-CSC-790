#!/usr/bin/python
import numpy as np
from tqdm import tqdm

def tf_idf(docs_path, tf_vectors, vocab):
	"""returns tfidf vectors for the docs
	"""
	print("MAKING VOCAB")
	idf_vector = np.zeros(len(vocab))
	doc_count = len(list(tf_vectors.keys()))

	print()
	print("MAKING THE IDF VECTOR")
	for word in vocab:
		_docs_containing_word = 0 
		for doc in list(tf_vectors.keys()):
			if tf_vectors[doc][vocab.index(word)] != 0:
				_docs_containing_word += 1

		idf_vector[vocab.index(word)] = np.log10(doc_count/(1 + _docs_containing_word))

	tf_idf_vectors = {}

	print()
	print("MAKING THE TFIDF VECTORS")
	for doc in tqdm(list(tf_vectors.keys())):
		tf_idf_vectors[doc] = tf_vectors[doc]*idf_vector
	
	return tf_idf_vectors

if __name__=="__main__":
	import pickle
	tf_vectors = pickle.load(open("../assets/tf_vectors.pickle", "rb"))
	vocab = pickle.load(open("../assets/vocab.pickle", "rb"))
	pickle.dump(tf_idf("../documents", tf_vectors, vocab), open("../assets/tfidf_vectors.pickle", "wb"))