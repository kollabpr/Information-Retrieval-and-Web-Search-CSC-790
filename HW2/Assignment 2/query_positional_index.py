import json
import re
import argparse
from natsort import natsorted, ns

def normalize(text):
        text = re.sub("[^A-Za-z_]", " ", text)
        text = re.sub(" +"," ",text)
        text = text.lower()
        return text

def _query(index, query):
    results = set()

    print("----------------------------------------------------")
    print(query)
    print("----------------------------------------------------")
    print()

    query_tokens = re.findall(r"\w+(?:'\w+)?|[^\w\s]", normalize(query))

    for token in query_tokens:
        print(token, end="\t: ")
        x1=list(index[token])
        print()
        print(natsorted(x1, key=lambda y: y.lower()))
        print()

    if len(query_tokens) == 1:
        print()
        print(query, end="\t: ")
        x=list(index[query_tokens[0]].keys())
        print(natsorted(x, key=lambda y: y.lower()))
        return

    doc_set = set(list(index[query_tokens[0]].keys()))
    for token in set(query_tokens[1:]):
        doc_set = doc_set.intersection(set(list(index[token].keys())))

    ref_positions = index[query_tokens[0]]
    matched_positions = {}
    for doc in doc_set:
        for position in ref_positions[doc]:
            MATCH_FLAG = 1 
            for _i, token in enumerate(query_tokens[1:]):
                if position+_i+1 in index[token][doc]:
                    continue
                else:
                    MATCH_FLAG = 0
                    break
            if MATCH_FLAG == 1:
                matched_positions[doc] = position
                results.add(doc)
                break

    print()
    print(query, end="\t: ")
    print(matched_positions)
    print()
    return 

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="query parser for a given positional index")

    parser.add_argument("--index", required=True, help="positional index json")
    parser.add_argument("--queries", required=True, help="queries file")

    args = parser.parse_args()

    index = json.loads(open(args.index).read())
    queries = [i.strip("\n") for i in open(args.queries).readlines()]

    for query in queries:
        _query(index, query)