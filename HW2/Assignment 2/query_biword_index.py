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
    query_tokens = re.findall(r"\w+(?:'\w+)?|[^\w\s]", normalize(query))
    print("----------------------------------------------------")
    print(query)
    print("----------------------------------------------------")
    print()
    try:
        init_phrase = query_tokens[0] + " " + query_tokens[1]
        results = set(index[init_phrase])  
        print(init_phrase, end="\t: ")
        print()
        #print(list(results))
        x2=list(results)
        print(natsorted(x2, key=lambda y: y.lower()))
    except:
        print(init_phrase, end="\t: ")
        print()
        print([])
        return

    for _i in range(1, len(query_tokens) - 1):
        try:
            phrase = query_tokens[_i] + " " + query_tokens[_i + 1]
            results = results.intersection(set(index[phrase]))
            print(phrase, end="\t: ")
            print()
            x=list(index[phrase])
            print(natsorted(x, key=lambda y: y.lower()))
            
        except:
            break
    y1=list(results)        
    print()
    print("common\t: ", end="")
    print(natsorted(y1, key=lambda y: y.lower()))
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