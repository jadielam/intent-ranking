import csv
import sys

from common import _lowercase, clean_entry
'''
Creates books entries from:
-books.csv
-books_other.csv
-BooksAliases.csv

The output will be a file with n lines, one per book.
The first entry in the line is the official name of the book.
The rest of the entries are other names used to refer to it.
'''

def read_books():
    to_return = {}

    with open("../raw/books.csv") as f:
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            name = row[0]
            to_return[name] = row[1:]
    return to_return

def read_books_aliases():
    to_return = {}

    with open("../raw/BookAliases.csv") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        for row in reader:
            bid = int(clean_entry(row[0]))
            s = clean_entry(row[1])

            to_return[bid] = [s]

    return to_return

def read_books_other():
    to_return = {}

    with open("../raw/books_other.csv") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        for row in reader:
            bid = int(clean_entry(row[0]))
            bname = clean_entry(row[1])
            s1 = clean_entry(row[4])
            s2 = clean_entry(row[5])

            to_return[bid] = [bname, s1, s2]

    return to_return


def main():
    # 1. Read books_other.csv, and use the official name as the name there.
    books_other = read_books_other()
    books_other = _lowercase(books_other)

    # 2. Read BooksAliases.csv, and add the unofficial names to the list
    books_aliases = read_books_aliases()
    books_aliases = _lowercase(books_aliases)

    # 3. Read books.csv and add unofficial names to the list.
    books = read_books()
    books = _lowercase(books)

    # Updating books_other with books_aliases
    for bid, names_l in books_aliases.items():
        for name in names_l:
            books_other[bid].append(name)

    final_books = {}
    for bid, names_l in books_other.items():
        final_books[names_l[0]] = set(names_l)

    # Updating final_books with books
    for official_name, other_names in books.items():
        if official_name in final_books:
            for name in other_names:
                final_books[official_name].add(name)

    # Write final books
    with open("../ner_entities/books.csv", "w+") as f:
        for bname, bnames in final_books.items():
            f.write(bname)
            for name in bnames:
                f.write("," + name)
            f.write("\n")

if __name__ == "__main__":
    main()