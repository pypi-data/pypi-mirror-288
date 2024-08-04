import re
import importlib.resources
from urllib.parse import quote
from os.path import exists
from os.path import join

import jinja2
from jinja2 import Environment
from jinja2 import BaseLoader

from .log_formats import colorized_logger
logger = colorized_logger(__name__)

jinja_environment = Environment(loader=BaseLoader)
jinja_environment.filters['quote'] = quote
jinja_environment.filters['lowercase'] = lambda x: x.lower()

with importlib.resources.path('adilib.templates', 'schema.owl.jinja') as file:
    with open(file, 'rt') as f:
        ontology_template = f.read()


class OWLGenerator:
    def __init__(self, tables, domain_token, domain_prefix, version):
        self.domain_token = domain_token
        self.domain_prefix = domain_prefix
        self.version = version
        self.mint_integer_identifiers(tables)
        self.create_template_parameters(tables)

    def get_ontology(self):
        template = jinja_environment.from_string(ontology_template)
        rendering = template.render(
            entities=self.entities,
            properties=self.properties,
            entity_like_properties=self.entity_like_properties,
            tables=self.tables,
            domain_token = self.domain_token,
            domain_prefix = self.domain_prefix,
            version = self.version,
        )
        return re.sub('\n\n\n+', '\n\n', rendering)

    def mint_integer_identifiers(self, tables):
        self.entity_names = list(set(tables['entities']['Label']))
        self.synonyms = {}
        self.identifier_integers_by_name = {}
        index = 1
        for i, entity in tables['entities'].iterrows():
            normal_name = entity['Label']
            self.synonyms[entity['Name']] = normal_name
            self.identifier_integers_by_name[normal_name] = index
            index = index + 1

        for i, property_row in tables['properties'].iterrows():
            normal_name = property_row['Label']
            self.synonyms[property_row['Name']] = normal_name
            self.identifier_integers_by_name[normal_name] = index
            index = index + 1

        for i, entity in tables['entities'].iterrows():
            normal_name = self.name_of_has(entity['Label'])
            self.identifier_integers_by_name[normal_name] = index
            index = index + 1

        for i, table in tables['tables'].iterrows():
            normal_name = table['Entity']
            self.synonyms[table['Label']] = normal_name

    def name_of_has(self, entity_name):
        return 'has %s' % entity_name.lower()

    def is_an_entity(self, name):
        return name in self.entity_names

    def create_template_parameters(self, tables):
        self.entities = [
            self.create_structured_record_of_element(entity)
            for i, entity in tables['entities'].iterrows()
        ]

        self.properties = [
            self.create_structured_record_of_element(property_row)
            for i, property_row in tables['properties'].iterrows()
        ]

        self.entity_like_properties = [
            {
                'iri' : self.get_iri_of_local_element(self.name_of_has(entity['Label'])),
                'textual_name' : self.name_of_has(entity['Label'])
            }
            for i, entity in tables['entities'].iterrows()
        ]

        self.tables = [
            self.create_structured_axioms_bundle(table_name, tables['fields'], tables['properties'])
            for table_name in set(tables['tables']['Label'])
        ]
        self.tables = [
            bundle
            for bundle in self.tables
            if len(bundle['implied_functional_relations']) > 0
        ]

    def create_structured_record_of_element(self, element):
        name = element['Label']
        definition = element['Definition']
        record = {
            'iri' : self.get_iri_of_local_element(name),
            'textual_name' : name,
            'definitional_annotation' : definition,
        }
        external_iri = self.get_iri_of_obo_external_element(element['Definitional reference'])
        if external_iri:
            record['known_type'] = {'iri' : external_iri}
        return record

    def create_structured_axioms_bundle(self, table_name, fields_table, properties_table):
        foreign_fields = [
            field
            for i, field in fields_table.iterrows()
            if field['Table'] == table_name and field['Foreign table'] != '' and field['Foreign key'] != '' and not field['Property'] in ['Identifier', 'Name']
        ]
        non_foreign_fields = [
            field
            for i, field in fields_table.iterrows()
            if field['Table'] == table_name and (field['Foreign table'] == '' or field['Foreign key'] == '') and not field['Property'] in ['Identifier', 'Name']
        ]
        return {
            'entity' : {
                'iri' : self.get_iri_of_local_element(table_name)
            },
            'implied_functional_relations' : [
                {
                    'property' : { 'iri' : self.get_iri_of_property_like_element(field['Property']) },
                    'target_iri' : self.get_iri_of_local_element(field['Foreign table']),
                }
                for field in foreign_fields
            ] + [
                {
                    'property' : { 'iri' : self.get_iri_of_property_like_element(field['Property']) },
                    'target_iri' : self.get_iri_of_property_target(field['Property'], properties_table),
                }
                for field in non_foreign_fields
            ]
        }

    def get_iri_of_property_like_element(self, name):
        if self.is_an_entity(name):
            explicit_property_like_name = self.name_of_has(name)
        else:
            explicit_property_like_name = name
        return self.get_iri_of_local_element(explicit_property_like_name)

    def get_iri_of_property_target(self, property_name, properties_table):
        if self.is_an_entity(property_name):
            return self.get_iri_of_local_element(property_name)
        property_rows = [
            row
            for i, row in properties_table.iterrows()
            if row['Label'] == property_name
        ]
        if len(property_rows) == 0:
            logger.error('Could not lookup target type for property "%s".' % property_name)
        property_row = property_rows[0]
        if property_row['Related entity'] != '':
            return self.get_iri_of_local_element(property_row['Related entity'])
        else:
            return self.get_generic_thing_iri()

    def get_iri_of_local_element(self, name):
        identifier = self.get_integer_identifier(name)
        if identifier:
            return ''.join([
                self.get_prefix(),
                self.render_integer_identifier(identifier),
            ])
        else:
            logger.error('No ontology-local integer identifier minted for "%s".' % name)

    def get_generic_thing_iri(self):
        return '&owl;%s' % 'Thing'

    def get_prefix(self):
        return '&%s;' % self.domain_prefix

    def render_integer_identifier(self, identifier):
        return str(identifier).rjust(7, '0')

    def get_integer_identifier(self, name):
        if name in self.synonyms:
            normal_name = self.synonyms[name]
        else:
            normal_name = name
        if normal_name in self.identifier_integers_by_name:
            return self.identifier_integers_by_name[normal_name]
        else:
            return None

    def get_iri_of_obo_external_element(self, crid_style_reference_string):
        crid = crid_style_reference_string
        if crid == '':
            return None
        pattern = '^([A-Z]{2,12})(:|_)[\dA-Z]+$'
        if re.match(pattern, crid):
            return 'http://purl.obolibrary.org/obo/' + re.sub(':', '_', crid)
        return None

