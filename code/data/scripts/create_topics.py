import csv

from common import _lowercase, clean_entry

def read_topics():
    topics = set()

    with open("../raw/Topics.csv") as f:
        reader = csv.reader(f, delimiter = ',', quotechar = '\"')
        for row in reader:
            topic = clean_entry(row[1])
            cidx = topic.find(",")
            if cidx != -1:
                topic = topic[cidx + 2 :] + " " + topic[:cidx]
            
            topics.add(topic.lower())
        return topics

def read_entities_to_set(filename):
    to_return = set()
    with open(filename) as f:
        reader = csv.reader(f, delimiter = ',')
        for row in reader:
            for entry in row:
                to_return.add(entry)
    
    return to_return

def main():
    #1. read topics
    topics = read_topics()

    #2. read these entities: books, cities, demonyms, islands, lakes, measurements, mountains, nations, persons, rivers, seas
    entities = [read_entities_to_set("../ner_entities/" + a + ".csv") for a in ["books", "cities", "demonyms", "islands", "lakes", "measurements", "mountains", "nations", "persons", "rivers", "seas"]]
    
    new_topics = set()
    #3. For each entry in topics, if entry is not in any of the
    # sets for those entities, add topic to list of topics
    for candidate in topics:
        add = True
        for entity_set in entities:
            if candidate in entity_set:
                add = False
                break

        if candidate[:3] == "the":
            for entity_set in entities:
                if candidate[4:] in entity_set:
                    add = False
                    break
        if add:
            new_topics.add(candidate)

    new_topics_l = list(new_topics)
    new_topics_l.sort()

    #4. Print list of topics.
    with open("../ner_entities/topics.csv", "w+") as f:
        f.write("\n".join(new_topics_l))

if __name__ == "__main__":
    main()
