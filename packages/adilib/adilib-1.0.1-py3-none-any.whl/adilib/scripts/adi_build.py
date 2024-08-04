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
        description = 'Schema builder for the Application Data Interface (ADI) framework.',
    )
    parser.add_argument('schema_source_dir',
        type=str,
        help='''
        The directory containing the source files tables.tsv, fields.tsv, entities.tsv,
        properties.tsv, values.tsv, and verbalizations.txt.jinja .'
        '''
    )
    parser.add_argument(
        '--frictionless-data',
        dest='frictionless_data',
        action='store_true',
        help='Whether to attempt to create Frictionless Data artifacts. If omitted, not created.',
    )
    args = parser.parse_args()
    if not exists(args.schema_source_dir):
        raise FileNotFoundError(args.schema_source_dir)
    schema_source_dir = abspath(args.schema_source_dir)

    print('Searching for source files in: %s' % schema_source_dir)
    converter = ADISchemaConverter(schema_source_dir=schema_source_dir)
    results = converter.generate_export_formats()
    token = converter.get_domain_token()
    prefix = converter.get_domain_prefix()
    with open('tables_fields_syntax_overview.html', 'wt') as file:
        file.write(results['HTML']['main overview'])
    with open('entities_alphabetical.html', 'wt') as file:
        file.write(results['HTML']['entities'])
    with open('properties_alphabetical.html', 'wt') as file:
        file.write(results['HTML']['properties'])
    with open('values.html', 'wt') as file:
        file.write(results['HTML']['values'])
    with open('schema.owl', 'wt') as file:
        file.write(results['OWL'])
    with open('schema.sql', 'wt') as file:
        file.write(results['SQL'])
    with open('schema_with_labels.sql', 'wt') as file:
        file.write(results['SQL with labels'])
    with open('schema.yaml', 'wt') as file:
        file.write(results['YAML'])
    with open('schema.yamldef', 'wt') as file:
        file.write(results['YAML def'])
    with open('schema.d2', 'wt') as file:
        file.write(results['D2 diagram source'])
    os.system('d2 --layout elk schema.d2 schema.d2.svg')
    if args.frictionless_data:
        fd_package = token + '_fd_package/'
        if not exists(fd_package):
            mkdir(fd_package)
        for filename, contents in results['Frictionless Data'].items():
            with open(join(fd_package, filename), 'wt') as file:
                file.write(contents)
