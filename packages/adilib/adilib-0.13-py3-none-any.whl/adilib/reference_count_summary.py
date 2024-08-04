import re
from urllib.request import urlopen
import json
import time
import os
from os.path import exists

import pandas as pd

from .log_formats import colorized_logger
logger = colorized_logger(__name__)


def extract_registry_symbol(crid, crid_pattern):
    if crid == '':
        return ''
    match = re.match(crid_pattern, crid)
    if match:
        return match.groups(1)[0]
    else:
        logger.error('Malformed CRID: %s', crid)
    return None


class OntologyReferenceSummaryGenerator:
    def __init__(self, tables, crid_pattern):
        summary_df = self.get_summary_data_frame(tables, crid_pattern)
        self.doc_ontology_summary = self.generate_summary_doc(summary_df)

    def get_doc_ontology_summary(self):
        return self.doc_ontology_summary

    def generate_summary_doc(self, summary_df):
        records = self.recordize(summary_df)
        for i in range(len(records)):
            count = records[i]['reference_count']
            records[i]['reference_placeholders'] = list(' ' * count)
        percent_coverage = round((
            sum(summary_df[summary_df['registry_symbol'] != '']['reference_count']) / sum(summary_df['reference_count']
        )) * 100)
        return {
            'header' : ['', 'Ontology name', 'Reference count'],
            'records' : records,
            'total_items_count' : sum(summary_df['reference_count']),
            'percent_coverage' : str(percent_coverage),
        }

    def get_summary_data_frame(self, tables, crid_pattern):
        references = []
        for tablename in ['entities', 'properties', 'values']:
            references = references + list(tables[tablename]['Definitional reference'])
        references = [extract_registry_symbol(r, crid_pattern) for r in references]
        counts = {
            value : sum([1 for r in references if r == value])
            for value in set(references)
        }
        registry_symbols = sorted(counts.keys(), key=lambda x: counts[x], reverse=True)
        registry_symbols_nonnull = [s for s in registry_symbols if s != '']
        counts_list = [counts[s] for s in registry_symbols_nonnull]
        registry_names, registry_urls = self.retrieve_registry_names_urls(registry_symbols_nonnull)

        return pd.DataFrame({
            'registry_symbol' : registry_symbols_nonnull + [''],
            'registry_name' : registry_names + ['not referenced'],
            'reference_count' : counts_list + [counts['']],
            'registry_url' : registry_urls + [''],
        })

    def retrieve_registry_names_urls(self, registry_symbols):
        known_values = {}
        known_file_urls = {}
        known_homepages = {}
        cache = '.registry_names.tsv'
        if exists(cache):
            with open(cache, 'rt') as f:
                for line in f.readlines():
                    tokens = line.split('\t')
                    known_values[tokens[0]] = tokens[1].rstrip()
                    known_homepages[tokens[0]] = tokens[2].rstrip()
                    known_file_urls[tokens[0]] = tokens[3].rstrip()
        registry_urls = []
        registry_file_urls = []
        registry_names = []
        logger.info('Throttling requests to OLS (Ontology Lookup Service) to once per 0.6 seconds.')
        for symbol in registry_symbols:
            if symbol == '':
                registry_names.append('')
            else:
                if symbol in known_values:
                    registry_names.append(known_values[symbol])
                    registry_file_urls.append(known_file_urls[symbol])
                    registry_urls.append(known_homepages[symbol])
                else:
                    time.sleep(0.6)
                    with urlopen('http://www.ebi.ac.uk/ols/api/ontologies/%s' % symbol) as response:
                        response_content = response.read()
                        json_response = json.loads(response_content)
                        title = json_response['config']['title']
                        homepage = json_response['config']['homepage']
                        file_url = json_response['config']['fileLocation']
                        if file_url is None:
                            file_url = json_response['config']['versionIRI']
                        if file_url is None:
                            file_url = '(unknown)'
                        registry_urls.append(homepage)
                        registry_file_urls.append(file_url)
                        registry_names.append(title)
                        logger.info('Looked up %s: %s', symbol, title)
        with open(cache, 'wt') as f:
            f.write('\n'.join([
                '\t'.join([str(x) for x in [symbol, name, url, file_url]])
                for symbol, name, url, file_url in zip(registry_symbols, registry_names, registry_urls, registry_file_urls)
            ]))
        symbols = {registry_names[i] : registry_symbols[i] for i in range(len(registry_names))}
        abbreviated_titles = [self.sanitize_title(name, symbols[name]) for name in registry_names]
        return abbreviated_titles, registry_urls

    def sanitize_title(self, name, symbol):
        name = re.sub('^[\w\d ]+:', '', name)
        name = re.sub('\([\w\d ]+\)', '', name)
        name = re.sub(' ?' + symbol + ' ?', '', name)
        name = re.sub('^[ \-\.]+', '', name)
        name = re.sub('[ \-\.]+$', '', name)
        return name

    def recordize(self, df):
        return df.to_dict(orient='records')


