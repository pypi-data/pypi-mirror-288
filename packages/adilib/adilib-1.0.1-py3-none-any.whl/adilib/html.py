import importlib.resources
import re

import jinja2
from jinja2 import Environment
from jinja2 import BaseLoader

jinja_environment = Environment(loader=BaseLoader)

with importlib.resources.path('adilib.templates', 'main_overview_docs.html.jinja') as file:
    with open(file, 'rt') as f:
        main_overview_template = f.read()

with importlib.resources.path('adilib.templates', 'entities_alphabetical.html.jinja') as file:
    with open(file, 'rt') as f:
        entities_alphabetical_template = f.read()

with importlib.resources.path('adilib.templates', 'properties_alphabetical.html.jinja') as file:
    with open(file, 'rt') as f:
        properties_alphabetical_template = f.read()

with importlib.resources.path('adilib.templates', 'values.html.jinja') as file:
    with open(file, 'rt') as f:
        values_alphabetical_template = f.read()

from .reference_count_summary import OntologyReferenceSummaryGenerator


class ADIHTMLDocGenerator:
    def __init__(self, tables, domain_token):
        self.tables = tables
        self.domain_token = domain_token
        self.crid_pattern = '^([A-Z\d]{2,12})(:|_)[\dA-Z]+$'
        self.overview = self.generate_main_overview()
        self.entities = self.generate_entities_table()
        self.properties = self.generate_properties_table()
        self.values = self.generate_values_table()

    def get_definition(self, token):
        return self.get_attribute(token, 'Definition')

    def get_label(self, token):
        return self.get_attribute(token, 'Label')

    def get_tag(self, token):
        return self.get_attribute(token, 'Name')

    def get_table_tag(self, token):
        t = self.tables['tables']
        if token in (list(t['Label']) + list(t['Name'])):
            table = t[(t['Label'] == token) | (t['Name'] == token)]
            return list(table['Name'])[0]
        return None

    def get_attribute(self, token, attribute):
        e = self.tables['entities']
        if token in (list(e['Label']) + list(e['Name'])):
            entity = e[(e['Label'] == token) | (e['Name'] == token)]
            return list(entity[attribute])[0]
        t = self.tables['tables']
        if token in (list(t['Label']) + list(t['Name'])):
            table = t[(t['Label'] == token) | (t['Name'] == token)]
            return self.get_attribute(list(table['Entity'])[0], attribute)
        p = self.tables['properties']
        if token in (list(p['Label']) + list(p['Name'])):
            prop = p[(p['Label'] == token) | (p['Name'] == token)]
            return list(prop[attribute])[0]
        return None

    def get_structure_designation(self, token):
        e = self.tables['entities']
        p = self.tables['properties']
        v = self.tables['values']
        if token in (list(e['Label']) + list(e['Name'])):
            return 'entities'
        if token in (list(p['Label']) + list(p['Name'])):
            return 'properties'
        if token in (list(v['Label']) + list(v['Name'])):
            return 'values'
        return None

    def get_crid_url(self, crid):
        if re.match(self.crid_pattern, crid):
            crid_url = 'http://purl.obolibrary.org/obo/' + re.sub(':', '_', crid)
        else:
            crid_url = ''
        return crid_url

    def has_known_values(self, prop):
        l = str(prop['Label']) in list(self.tables['values']['Parent property'])
        n = str(prop['Name']) in list(self.tables['values']['Parent property'])
        if l or n:
            return True
        else:
            return False

    def generate_main_overview(self):
        verbalizations = self.get_verbalizations()
        table_specifications = []
        for i, table in self.tables['tables'].iterrows():
            f = self.tables['fields']
            ft = f[(f['Table'] == table['Label']) | (f['Table'] == table['Name'])]
            fields = ft.sort_values(by='Ordinality')
            specification = [{
                'label' : table['Label'],
                'tag' : table['Name'],
                'definition' : self.get_definition(table['Entity']),
                'entity_type_label' : self.get_label(table['Entity']),
                'entity_type_tag' : self.get_tag(table['Entity']),
                'verbalization' : verbalizations[table['Label']],
            }]
            for j, field in fields.iterrows():
                if field['Foreign table'] != '':
                    foreign_key_anchor = self.get_table_tag(field['Foreign table'])
                else:
                    foreign_key_anchor = ''
                specification.append({
                    'label' : field['Label'],
                    'definition' : self.get_definition(field['Property']),
                    'property_type_label' : self.get_label(field['Property']),
                    'property_type_tag' : self.get_tag(field['Property']),
                    'target_page' : self.get_structure_designation(field['Property']) + '_alphabetical',
                    'foreign_key_anchor' : foreign_key_anchor,
                })
            table_specifications.append(specification)
        return table_specifications

    def generate_entities_table(self):
        entities_list = []
        for i, entity in self.tables['entities'].sort_values(by='Label').iterrows():
            entities_list.append({
                'label' : entity['Label'],
                'tag' : entity['Name'],
                'definition' : entity['Definition'],
                'definition_reference' : entity['Definitional reference'],
                'crid_url' : self.get_crid_url(entity['Definitional reference']),
            })
        return entities_list

    def generate_properties_table(self):
        properties_list = []
        for i, prop in self.tables['properties'].sort_values(by='Label').iterrows():
            values_tag = ''
            if self.has_known_values(prop):
                values_tag = prop['Name']
            properties_list.append({
                'label' : prop['Label'],
                'tag' : prop['Name'],
                'definition' : prop['Definition'],
                'definition_reference' : prop['Definitional reference'],
                'values_type' : prop['Value type'],
                'applies_to_entity' : self.get_label(prop['Entity']),
                'applies_to_entity_tag' : self.get_tag(prop['Entity']),
                'related_entity' : prop['Related entity'],
                'related_entity_tag' : self.get_tag(prop['Related entity']),
                'crid_url' : self.get_crid_url(prop['Definitional reference']),
                'values_tag' : values_tag,
            })
        return properties_list

    def generate_values_table(self):
        properties_values = []
        for i, values in self.tables['values'].sort_values(by=['Parent property', 'Enumeration']).groupby('Parent property'):
            tag = self.get_tag(list(values['Parent property'])[0])
            values_list = [{
                'parent_property_label' : self.get_label(list(values['Parent property'])[0]),
                'parent_property_tag' : tag,
            }]
            for j, value in values.iterrows():
                values_list.append({
                    'label' : value['Label'],
                    'tag' : value['Name'],
                    'definition' : value['Definition'],
                    'definition_reference' : value['Definitional reference'],
                    'crid_url' : self.get_crid_url(value['Definitional reference']),
                })
            properties_values.append({
                'property_tag' : tag,
                'value_items' : values_list,
            })
        return properties_values

    def get_verbalizations(self):
        verbalization_forms = {}
        decaptitalize = lambda x: x.lower()
        for tablename, verbalization_template in self.tables['verbalizations'].items():
            template = jinja_environment.from_string(verbalization_template)
            all_fields = self.tables['fields']
            fields = all_fields[all_fields['Table'] == tablename]            
            args = {
                field['Name'] : '<code>&lt;' + decaptitalize(field['Label']) + '&gt;</code>'
                for j, field in fields.iterrows()
            }
            verbalization_forms[tablename] = '<i>' + template.render(**args) + '</i>'
        return verbalization_forms

    def get_html_fragments(self):
        template = jinja_environment.from_string(main_overview_template)
        generator = OntologyReferenceSummaryGenerator(
            self.tables,
            self.crid_pattern,
        )
        doc_ontology_summary = generator.get_doc_ontology_summary()
        overview_html = template.render(
            table_specifications=self.overview,
            ontology_summary=doc_ontology_summary,
            domain_token=self.domain_token,
        )

        template = jinja_environment.from_string(entities_alphabetical_template)
        entities_alphabetical_html = template.render(
            entities=self.entities,
            domain_token=self.domain_token,
        )

        template = jinja_environment.from_string(properties_alphabetical_template)
        properties_alphabetical_html = template.render(
            properties=self.properties,
            domain_token=self.domain_token,
        )

        template = jinja_environment.from_string(values_alphabetical_template)
        values_html = template.render(
            values=self.values,
            domain_token=self.domain_token,
        )

        return {
            'main overview': overview_html,
            'entities' : entities_alphabetical_html,
            'properties' : properties_alphabetical_html,
            'values' : values_html,
        }
