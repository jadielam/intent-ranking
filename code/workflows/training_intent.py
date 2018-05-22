import sys
import json

def main():
    with open(sys.argv[1]) as f:
        conf = json.load(f)
    
    #1. 

if __name__ == "__main__":
    main()