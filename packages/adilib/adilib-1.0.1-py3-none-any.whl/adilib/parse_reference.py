import os
from os import listdir
from os.path import join
from os.path import split
import re

import pandas as pd
import toml

from .log_formats import colorized_logger
logger = colorized_logger(__name__)

from .schema_source_validation import ADISchemaSourceBasicChecker


class ADISchemaImporter:
    def __init__(self, schema_source_dir):
        packagename = toml.load(join(schema_source_dir, 'pyproject.toml'))['project']['name']

        tables = self.load_tables(join(schema_source_dir, packagename))
        checker = ADISchemaSourceBasicChecker()
        checker.validate(tables)
        self.report_schema_source_statistics(tables)
        self.tables = tables
        self.domain_token = split(schema_source_dir)[1]

        # self.version = open(join(schema_source_dir, 'version.txt'), 'rt').read()
        self.version = toml.load(join(schema_source_dir, 'pyproject.toml'))['project']['version']

        self.domain_prefix = open(join(schema_source_dir, 'prefix.txt'), 'rt').read()

    def load_tables(self, schema_source_dir):
        source_filenames = ['tables', 'fields', 'entities', 'properties', 'values']
        files = os.listdir(schema_source_dir)

        missing = list(set([f+'.tsv' for f in source_filenames]).difference(files))
        if missing == []:
            logger.info('Directory %s has all necessary source tables.', schema_source_dir)
        else:
            logger.error('Directory %s is missing source tables: %s', schema_source_dir, missing)
        verbalizations_file = 'verbalizations.txt.jinja'
        if verbalizations_file in files:
            logger.info(
                'Directory %s has verbalizations template file.',
                schema_source_dir,
            )
        else:
            logger.error(
                'Directory %s is missing verbalizations template file %s .',
                schema_source_dir,
                verbalizations_file,
            )

        filenames = {
            tablename : join(schema_source_dir, tablename + '.tsv')
            for tablename in source_filenames
        }
        tables = {
            tablename : pd.read_csv(filenames[tablename], sep='\t', na_filter=False)
            for tablename in source_filenames
        }
        tables['verbalizations'] = self.retrieve_verbalizations(
            join(schema_source_dir, verbalizations_file)
        )
        return tables

    def get_version_string(self):
        return self.version

    def retrieve_verbalizations(self, verbalizations_file):
        with open(verbalizations_file, 'rt') as file:
            lines = file.readlines()
        tablename = None
        verbalizations = {}
        for line in lines:
            if line.lstrip().rstrip() == '':
                tablename = None
                continue
            else:
                if not tablename:
                    tablename = line.rstrip().rstrip(':')
                else:
                    verbalizations[tablename] = line.rstrip()
        return verbalizations

    def report_schema_source_statistics(self, tables):
        logger.info(
            'Schema specifies %s tables with a total of %s fields.',
            tables['tables'].shape[0],
            tables['fields'].shape[0],
        )
        logger.info(
            'Schema refers to %s entity types, %s property types, and %s specific values.',
            tables['entities'].shape[0],
            tables['properties'].shape[0],
            tables['values'].shape[0],
        )
        reference_count_entities = len([x for x in tables['entities']['Definitional reference'] if x != ''])
        reference_count_properties = len([x for x in tables['properties']['Definitional reference'] if x != ''])
        reference_count_values = len([x for x in tables['values']['Definitional reference'] if x != ''])
        count_entities = len(tables['entities']['Definitional reference'])
        count_properties = len(tables['properties']['Definitional reference'])
        count_values = len(tables['values']['Definitional reference'])
        logger.info(
            '%s entities (%s%%) are associated with an external ontology CRID reference.',
            reference_count_entities,
            round(100 * reference_count_entities / count_entities),
        )
        logger.info(
            '%s properties (%s%%) are associated with an external ontology CRID reference.',
            reference_count_properties,
            round(100 * reference_count_properties / count_properties),
        )
        logger.info(
            '%s values (%s%%) are associated with an external ontology CRID reference.',
            reference_count_values,
            round(100 * reference_count_values / count_values),
        )
        logger.info(
            'Overall external ontology coverage is about %s%%.',
            round(100 * 
                sum([
                    reference_count_entities,
                    reference_count_properties,
                    reference_count_values,
                ]) /
                sum([
                    count_entities,
                    count_properties,
                    count_values,
                ])
            )
        )

    def get_tables(self):
        return self.tables

    def get_domain_token(self):
        return self.domain_token

    def get_domain_prefix(self):
        return self.domain_prefix

    def get_importable_ontology_urls(self):
        return self.importable_ontology_urls
