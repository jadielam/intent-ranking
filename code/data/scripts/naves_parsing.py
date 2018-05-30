import csv

def parse_naves(filepath):
    with open(filepath) as f:
        content = f.readlines()
    
    content = [x.strip() for x in content]
    
    entries = {}

    i = -1
    state = "find_entry"
    current_entry = None
    current_text = None
    
    while True:
        i += 1
        if i >= len(content):
            break
        line = content[i]
        if len(line) == 0:
            continue

        if state == "find_entry":
            if line.isupper():
                if line == "NAVES TOPICAL BIBLE":
                    continue
                else:
                    current_entry = line.lower()
                    state = "find_text"
        elif state == "find_text":
            if line.isupper():
                continue
            if line.isdigit():
                continue
            entries[current_entry] = line
            state = "find_entry"
    
    return entries

def read_topics(filepath):
    topics = []
    with open(filepath) as f:
        reader = csv.reader(f, delimiter = ",")
    
        for line in reader:
            topic = line[0]
            topics.append(topic)
    return topics

def main():
    entries = parse_naves("../raw/naves.txt")
    topics = read_topics("../ner_entities/topics.csv")

    with open("../ner_entities/topics_annotated.csv", "w+") as f:
        for topic in topics:
            if topic in entries:
                f.write(topic + "," + entries[topic] + "\n")
            else:
                f.write(topic + "\n")

if __name__ == "__main__":
    main()