'''
Prepares the input data for the NER model
Input: csv file with two columns: template, intent ranks
Output: csv file with three columns: realized template, ner annotations, intents

It needs to run the realized templates through the ner model to create ner annotations column.
'''

import os
import sys
import json
import csv
import random
import string

import pyner.test.tag_sentence_factory as tag_sentence_factory

def read_template_file(filepath):
    entries = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter = '\t')
        for row in reader:
            if len(row) > 0:
                template = row[0]
                intents = row[1]
                entries.append((template, intents))
    return entries

def read_entities(filepath):
    entries = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter = '\t')
        for row in reader:
            if len(row) > 0:
                entries.append(row)
    return entries

def write_output_file(output_path, entries):
    pass

def main():
    with open(sys.argv[1]) as f:
        conf = json.load(f)
    
    entity_files = conf['entity_files']
    templates_file = conf['templates_file']
    output_path = conf['output_path']
    nb_samples = conf['nb_samples']
    tagger_conf_file = conf['tagger_conf_file']

    with open(tagger_conf_file) as f:
        tagger_conf = json.load(f)
    tag_sentence = tag_sentence_factory(conf)
    
    #1. Read entity files
    entities_d = {}
    for e_type, filepath in entity_files.items():
        entities_d[e_type] = read_entities(filepath)

    #2. Read templates file
    templates_l = read_template_file(templates_file)

    #3. Create output entries
    F = string.Formatter()
    output_entries = []
    for _ in range(nb_samples):
        template, intents = random.choice(templates_l)
        params = [a[1] for a in F.parse(template) if a[1] is not None]
        
        replacements = {}
        for param in params:
            entities = entities_d[param]
            line_choice = random.choice(entities)
            entity_choice = random.choice(line_choice)
            replacements[param] = entity_choice

        formatted = template.format(replacements)
        tagged_sequence = tag_sentence(formatted)
        tagged_sequence = " ".join(tagged_sequence)
        output_entries.append((formatted, tagged_sequence, intents))
    
    write_output_file(output_path, output_entries)

if __name__ == "__main__":
    main()