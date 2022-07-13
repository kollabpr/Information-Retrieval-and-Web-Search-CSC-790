import re, os
import json
import argparse
from collections import OrderedDict

def normalize(text):
        text = re.sub("[^A-Za-z_]", " ", text)
        text = re.sub(" +"," ",text)
        text = text.lower()
        return text

def build_positional_index(input_dir, index_path):
    print("Buliding positional index!")
    index = {}
    for file in os.listdir(input_dir):
        if file.endswith(".txt"):
            # use os to make a legible path string
            file_text = normalize(open(input_dir + "/" + file).read())
            words = re.findall(r"\w+(?:'\w+)?|[^\w\s]", file_text)

            for _i, word in enumerate(words):
                if word not in index.keys():
                    index[word] = {}
                    index[word][file] = []
                    index[word][file].append(_i)
                else:
                    if file not in index[word].keys():
                        index[word][file] = []
                    index[word][file].append(_i)

                index[word] = OrderedDict(sorted(index[word].items()))
    index = OrderedDict(sorted(index.items()))
    o_fp = open(index_path, "w")
    o_fp.write(json.dumps(index))

    path=os.getcwd()
    print("Positional index created sucessfully.")
    size = os.path.getsize(path+'/positional_index.json') 
    print('Size of file is: ', size, 'bytes')
    o_fp.close() 
   

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="positional indexer")

	parser.add_argument("--data_dir", required=True, help="path to the directory containing the docs")
	parser.add_argument("--index_path", required=True, help="path for storing the index")

	args = parser.parse_args()
	build_positional_index(args.data_dir, args.index_path)
