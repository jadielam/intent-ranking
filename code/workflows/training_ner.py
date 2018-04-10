'''
Trains a ner model
'''

import sys
import json

import pyner.train.train as train

def main():
    with open(sys.argv[1]) as f:
        conf = json.load(f)

    train(conf)

if __name__ == "__main__":
    main()