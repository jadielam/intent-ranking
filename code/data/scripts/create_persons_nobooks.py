'''
1. Reads the list of persons
2. Reads the list of persons and books
3. Finds books - persons and outputs it
'''
import csv

def read_persons():
    to_return = {}

    with open("../ner_entities/persons.csv") as f:
        reader = csv.reader(f, delimiter = ',')

        for row in reader:
            to_return[row[0]] = row[1:]
    
    return to_return

def read_books_persons():
    to_return = set()
    with open("../ner_entities/books_persons.csv") as f:
        reader = csv.reader(f, delimiter = ',')
        for row in reader:
            to_return.add(row[0])
    
    return to_return
    
def main():
    persons = read_persons()
    books_persons = read_books_persons()

    books_no_persons = {}
    for person, abbvs in persons.items():
        if person not in books_persons:
            books_no_persons[person] = abbvs
    
    with open("../ner_entities/persons_nobooks.csv", "w+") as f:
        for person, abbvs in books_no_persons.items():
            f.write(",".join([person] + abbvs))
            f.write("\n")

if __name__ == "__main__":
    main()