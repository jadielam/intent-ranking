import csv

def read_persons():
    persons = set()

    with open("../entities/persons.csv") as f:
        reader = csv.reader(f, delimiter = ",")

        for row in reader:
            persons.add(row[0])
    
    return persons

def read_books():
    books = set()
    with open("../entities/books.csv") as f:
        reader = csv.reader(f, delimiter = ",")

        for row in reader:
            books.add(row[0])

    return books
    
def main():
    #1. read persons
    persons = read_persons()

    #2. read books
    books = read_books()

    #3. Find the intersection
    persons_books = set.intersection(persons, books)

    #4. Output the intersection
    with open("../entities/books_persons.csv", "w+") as f:
        f.write("\n".join(persons_books))

if __name__ == "__main__":
    main()