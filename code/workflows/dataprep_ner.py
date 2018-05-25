'''
Input: csv file with two columns: template, intents
Output: Two csv files.
- Csv file with two columns: realized templates, ner annotations
- Csv file with two columns: realized templates, incorrect ner annotations.
  The second csv file needs to be corrected manually by a human

Entities that go into first csv file:
- book (books that are not persons)
- book_abbv
- ref_number
- book_person
- person (persons that are not books)
- city
- demonyms
- lake
- sea
- island
- mountain
- topic

Entities that go into the second csv file:
- bible_verse_portion
- section_heading
- small_phrase
'''
import os
import sys
import json
import csv
import random
import string

def are_in_params(list1, params):
    for a in list1:
        if a in params:
            return True
    return False
    
def generate_random_entity_factory(entities_d, function_type):

    def generate_random_entity(entity_type):
        if entity_type == "book":
            entities = random.choice(entities_d[entity_type])
            return entities[0]
        if entity_type in entities_d:
            entities = random.choice(entities_d[entity_type])
            return random.choice(entities)
        elif entity_type == "ref_number":
            return random.randint(1, 200)
        elif entity_type == "book_abbv":
            entities = random.choice(entities_d["book"])
            return random.choice(entities)
        elif entity_type == "small_phrase":
            return random.choice(entities_d['small_phrase'])
        elif entity_type == "bible_verse_portion":
            return random.choice(entities_d['bible_verse_portion'])
        elif entity_type == "section_heading":
            return random.choice(entities_d['section_heading'])
        else:
            raise KeyError
    
    return generate_random_entity

def read_entities(filepath):
    entries = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            if len(row) > 0:
                entries.append(row)
    return entries

def read_templates(filepath):
    entries = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter = '\t')
        for row in reader:
            if len(row) > 0:
                template = row[0]
                entries.append(template)
    return entries

def write_annotated_sentences(output_path, annotated_sentences):
    with open(output_path, "w+") as f:
        f.write("\n".join(annotated_sentences))

def create_annotated_entity(entity, annotation):
    tokens = entity.split()
    annotated = []
    for idx, token in enumerate(tokens):
        if idx = 0:
            annotated.append(token + "/" + "B-" + annotation)
        else:
            annotated.append(token + "/" + "I-" + annotation)
    return " ".join(annotated)

def main():
    with open(sys.argv[1]) as f:
        conf = json.load(f)
    
    entity_files = conf['entity_files']
    templates_file = conf['templates_file']
    output_path = conf['output_path']
    nb_samples = conf['nb_samples']

    #1. Read entity files
    entities_d = {}
    for e_type, filepath in entity_files.items():
        entities_d[e_type] = read_entities(filepath)
    select_random_entity = generate_random_entity_factory(entities_d)
    
    #2. Read templates file
    templates_l = read_templates(filepath)

    #3. For n runs:
    F = string.Formatter()
    formatted_sentences1 = []
    formatted_sentences2 = []

    for _ in range(nb_samples):
        template = random.choice(templates_l)
        params = [a[1] for a in F.parse(template) if a[1] is not None]
        
        
        if are_in_params(['small_phrase', 'bible_verse_portion', 'section_heading'], params):
            replacements = {}
            for param in params:
                entity_choice = select_random_entity(param)
                replacements[param] = entity_choice
            formatted = template.format(replacements)
            formatted_sentences1.append(formatted)
        else:
            replacements = {}
            for param in params:
                entity_choice = select_random_entity(param)
                annotated_entity = create_annotated_entity(entity_choice, param)
                replacements[param] = annotated_entity
            formatted = template.format(replacements)
            formatted_sentences2.append(formatted)
            
    write_annotated_sentences(output_path1, formatted_sentences1)
    write_annotated_sentences(output_path2, formatted_sentences2)
    
if __name__ == "__main__":
    main()