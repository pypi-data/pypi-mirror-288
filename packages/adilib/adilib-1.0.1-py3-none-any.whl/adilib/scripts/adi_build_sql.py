#!/usr/bin/env python3
import argparse
import os
from os import mkdir
from os.path import abspath
from os.path import exists
from os.path import join

import adilib
from adilib import ADISchemaConverter

def main_program():
    parser = argparse.ArgumentParser(
        description = 'SQL schema builder for the Application Data Interface (ADI) framework.',
    )
    parser.add_argument('schema_source_dir',
        type=str,
        help='''
        The directory containing the source files tables.tsv, fields.tsv, entities.tsv,
        properties.tsv, values.tsv, and verbalizations.txt.jinja .'
        '''
    )
    parser.add_argument('--unique-rows',
        dest='unique_rows',
        action='store_true',
    )
    args = parser.parse_args()
    if not exists(args.schema_source_dir):
        raise FileNotFoundError(args.schema_source_dir)
    schema_source_dir = abspath(args.schema_source_dir)

    unique_rows = True if args.unique_rows else False
    print('Searching for source files in: %s' % schema_source_dir)
    if unique_rows:
        print('Adding uniqueness constraint to all rows.')
    converter = ADISchemaConverter(schema_source_dir=schema_source_dir, unique_rows=unique_rows)
    results = converter.generate_sql()
    with open('schema.sql', 'wt') as file:
        file.write(results['SQL'])
    with open('schema_with_labels.sql', 'wt') as file:
        file.write(results['SQL with labels'])
