'''
Input: csv file with two columns: template, intents
Output: csv file with one column: realized templates, ner annotations
'''
import os
import sys
import json
import csv
import random
import string

def read_entities(filepath):
    entries = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter = '\t')
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

    #2. Read templates file
    templates_l = read_templates(filepath)

    #3. For n runs:
    F = string.Formatter()
    formatted_sentences = []
    for _ in range(nb_samples):
        template = random.choice(templates_l)
        params = [a[1] for a in F.parse(template) if a[1] is not None]
        
        replacements = {}
        for param in params:
            entities = entities_d[param]
            line_choice = random.choice(entities)
            entity_choice = random.choice(line_choice)
            annotated_entity = create_annotated_entity(entity_choice, param)
            replacements[param] = annotated_entity
        
        formatted = template.format(replacements)
        formatted_sentences.append(formatted)

    write_annotated_sentences(output_path, formatted_sentences)
    
if __name__ == "__main__":
    main()