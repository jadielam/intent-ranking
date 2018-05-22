import csv

from common import clean_entry, _lowercase

def read_persons():
    persons = []

    with open("../raw/People.csv") as f:
        reader = csv.reader(f, delimiter = ',')

        next(reader)
        for row in reader:
            name = clean_entry(row[1])
            persons.append(name)
    
    return persons
        
def main():
    persons = read_persons()
    persons = _lowercase(persons)
    with open("../entities/persons.csv", "w+") as f:
        f.write("\n".join(persons))
    
if __name__ == "__main__":
    main()
