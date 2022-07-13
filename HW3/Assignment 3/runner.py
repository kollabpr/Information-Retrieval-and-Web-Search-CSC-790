import pickle
import numpy as np
from src.tf import _make_vocab
from collections import Counter

tf_sim = pickle.load(open("assets/tf_similarity.pickle", "rb"))
tfidf_sim = pickle.load(open("assets/tfidf_similarity.pickle", "rb"))
wfidf_sim = pickle.load(open("assets/wfidf_similarity.pickle", "rb"))
_vocab = pickle.load(open("assets/vocab.pickle", "rb"))
_term_count = pickle.load(open("assets/term_count.pickle", "rb"))

k = int(input("ENTER THE VALUE OF K:"))

print()
print("THE NUMBER OF UNIQUE WORDS: " + str(len(_vocab)), end="\n\n")

print()
print("TOP 10 MOST COMMON WORDS: ")
_term_count = sorted(_term_count.items(), key=lambda x: x[1])
for i in _term_count[::-1][:10]:
    print(i[0])

print()
print("TF: TOP K SIMILAR PAIRS OF DOCS: ")
for _i in [item for item in tf_sim.items()][::-1][:k]:
	print(_i)

print()
print("TFIDF: TOP K SIMILAR PAIRS OF DOCS: ")
for _i in [item for item in tfidf_sim.items()][::-1][:k]:
	print(_i)

print()
print("WFIDF: TOP K SIMILAR PAIRS OF DOCS: ")
for _i in [item for item in wfidf_sim.items()][::-1][:k]:
	print(_i)
