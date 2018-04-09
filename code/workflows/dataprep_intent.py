'''
Prepares the input data for the NER model
Input: csv file with two columns: template, intent ranks
Output: csv file with three columns: realized template, ner annotations, intents

It needs to run the realized templates through the ner model to create ner annotations column.
'''