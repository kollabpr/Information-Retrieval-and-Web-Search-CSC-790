#!/usr/bin/python
import numpy as np

def get_cosine_scores(vec_dic):
	cosine_scores = {}
	doc_list = list(vec_dic.keys())
	
	for _i, doc in enumerate(doc_list):
		for _j in range(_i+1, len(doc_list)):
			cosine_scores[doc + " " + doc_list[_j]] = np.dot(vec_dic[doc], vec_dic[doc_list[_j]])/(np.linalg.norm(vec_dic[doc]) * np.linalg.norm(vec_dic[doc_list[_j]]))

	return dict(sorted(cosine_scores.items(), key=lambda item: item[1]))

if __name__=="__main__":
	import pickle
	pickle.dump(get_cosine_scores(pickle.load(open("../assets/tf_vectors.pickle", "rb"))), open("../assets/tf_similarity.pickle", "wb"))
	pickle.dump(get_cosine_scores(pickle.load(open("../assets/tfidf_vectors.pickle", "rb"))), open("../assets/tfidf_similarity.pickle", "wb"))
	pickle.dump(get_cosine_scores(pickle.load(open("../assets/wf_vectors.pickle", "rb"))), open("../assets/wf_similarity.pickle", "wb"))
	pickle.dump(get_cosine_scores(pickle.load(open("../assets/wfidf_vectors.pickle", "rb"))), open("../assets/wfidf_similarity.pickle", "wb"))
