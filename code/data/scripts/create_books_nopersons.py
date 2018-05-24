'''
1. Reads the list of books
2. Reads the list of persons
3. Finds books - persons and outputs it
'''
import csv

def read_books():
    to_return = {}

    with open("../ner_entities/books.csv") as f:
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
    books = read_books()
    books_persons = read_books_persons()

    books_no_persons = {}
    for book, abbvs in books.items():
        if book not in books_persons:
            books_no_persons[book] = abbvs
    
    with open("../ner_entities/books_nopersons.csv", "w+") as f:
        for book, abbvs in books_no_persons.items():
            f.write(",".join([book] + abbvs))
            f.write("\n")

if __name__ == "__main__":
    main()