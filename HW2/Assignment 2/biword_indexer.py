import re, os
import json
import argparse 
from collections import OrderedDict

def normalize(text):
        text = re.sub("[^A-Za-z_]", " ", text)
        text = re.sub(" +"," ",text)
        text = text.lower()
        return text

def build_biword_index(input_dir, index_path):
    print("Building Biword index!")
    index = {}
    for file in os.listdir(input_dir):
        if file.endswith(".txt"):
            # use os to make a legible path string
            file_text = normalize(open(input_dir + "/" + file).read())
            words = re.findall(r"\w+(?:'\w+)?|[^\w\s]", file_text)

            for _i in range(len(words) - 1):
                biword_phrase = words[_i] + " " + words[_i + 1]
                if biword_phrase not in index.keys():
                    index[biword_phrase] = []
                if file not in index[biword_phrase]:
                    index[biword_phrase].append(file)
                index[biword_phrase].sort()

    o_fp = open(index_path, "w")
    o_fp.write(json.dumps(index))
    
    path=os.getcwd()
    print("Biword index created sucessfully.")
    size = os.path.getsize(path+'/biword_index.json') 
    print('Size of file is: ', size, 'bytes')
    o_fp.close() 

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="positional indexer")

	parser.add_argument("--data_dir", required=True, help="path to the directory containing the docs")
	parser.add_argument("--index_path", required=True, help="path for storing the index")

	args = parser.parse_args()
	build_biword_index(args.data_dir, args.index_path)
