import re
import importlib.resources

from jinja2 import Environment
from jinja2 import BaseLoader
from pandas import DataFrame
from pandas.io.sql import get_schema

from .log_formats import colorized_logger
logger = colorized_logger(__name__)

jinja_environment = Environment(loader=BaseLoader)

with importlib.resources.path('adilib.templates', 'create_db.sql.jinja') as file:
    with open(file, 'rt') as f:
        create_db_template = f.read()

def normalize(token):
    return re.sub('[ \-]', '_', token).lower()

def aggressive_quote(string):
    if isinstance(string, str):
        return re.sub(r'''[\'\"]''', '', str(string))
    else:
        return string


class ADISQLGenerator:
    def __init__(self, tables, domain_token, version, unique_rows: bool=False):
        self.doc_tables, self.doc_fields = self.get_document_objects(tables)
        self.doc_tables_labels, self.doc_fields_labels = self.get_document_objects(tables, readable_labels=True)

        self.reference_table_statements = []
        for table_name, table in tables.items():
            if isinstance(table, DataFrame):
                table_name = 'reference_' + table_name
                self.reference_table_statements.append(get_schema(table, table_name) + ';\n' + self.batch_insert(table, table_name))

        self.version = version
        self.unique_rows = unique_rows

    def get_document_objects(self, tables, readable_labels=False):
        entities = self.recordize(tables['entities'])
        properties = self.recordize(tables['properties'])
        values = self.recordize(tables['values'])
        fields = self.recordize(tables['fields'])

        for i, field in enumerate(fields):
            matches = { **{
                'property' :
                p for p in properties
                if normalize(field['property']) == p['name']
            }, **{
                'entity' :
                e for e in entities
                if normalize(field['property']) == e['name']
            } }
            entity_or_property = list(matches.keys())[0]
            property_info = list(matches.values())[0]
            fields[i]['entity_or_property'] = entity_or_property
            if entity_or_property == 'entity':
                fields[i]['entity_name'] = property_info['name']
                fields[i]['definition'] = aggressive_quote(property_info['definition'])
                fields[i]['definitional_reference'] = property_info['definitional_reference']
            if entity_or_property == 'property':
                fields[i]['value_type'] = property_info['value_type']
                if normalize(field['property']) in [normalize(v) for v in tables['values']['Parent property']]:
                    fields[i]['has_predefined_values'] = True
                else:
                    fields[i]['has_predefined_values'] = False
                fields[i]['definition'] = aggressive_quote(property_info['definition'])
                fields[i]['definitional_reference'] = property_info['definitional_reference']
            if field['foreign_table'] != '':
                fields[i]['is_foreign_key'] = True
                fields[i]['foreign_table_normalized'] = normalize(field['foreign_table'])
                fields[i]['foreign_key_normalized'] = normalize(field['foreign_key'])
            else:
                fields[i]['is_foreign_key'] = False
            if field['primary_key_group'] in ['1', 1]:
                fields[i]['is_primary_key'] = True
            else:
                fields[i]['is_primary_key'] = False

        for i in range(len(entities)):
            definition = aggressive_quote(entities[i]['definition'])
            entities[i]['definition'] = definition

        doc_tables = self.recordize(tables['tables'])

        if readable_labels:
            for i in range(len(fields)):
                if 'foreign_table_normalized' in fields[i]:
                    label = self.retrieve_field_label(fields[i]['foreign_key_normalized'], fields[i]['foreign_table_normalized'], fields)
                    fields[i]['foreign_key_normalized'] = label
                    label = self.retrieve_table_label(fields[i]['foreign_table_normalized'], doc_tables)
                    fields[i]['foreign_table_normalized'] = label
            for i in range(len(fields)):
                label = self.retrieve_field_label(fields[i]['name'], fields[i]['table'], fields)
                fields[i]['name'] = label
        
        entities_by_label = {e['label']: e for e in entities}

        for i, table_record in enumerate(doc_tables):
            doc_tables[i]['fields'] = [
                f for f in fields
                if normalize(f['table']) == doc_tables[i]['name']
            ]
            doc_tables[i]['entity'] = entities_by_label[doc_tables[i]['entity']]

        if readable_labels:
            for i in range(len(doc_tables)):
                label = self.retrieve_table_label(doc_tables[i]['name'], doc_tables)
                doc_tables[i]['name'] = label

        return [doc_tables, fields]

    def retrieve_table_label(self, name, tables):
        matches = [record for record in tables if name in [record['name'], normalize(record['name'])]]
        if len(matches) == 1:
            return '"' + matches[0]['label'] + '"'
        else:
            logger.error('Can not lookup label for table name "%s".', name)
            raise ValueError

    def retrieve_field_label(self, name, tablename, fields):
        matches = [
            record for record in fields
            if name in [record['name'], normalize(record['name'])] and tablename in [record['table'], normalize(record['table'])]
        ]
        if len(matches) == 1:
            return '"' + matches[0]['label'] + '"'
        else:
            logger.error('Can not lookup label for field name "%s" from table "%s".', name, tablename)
            raise ValueError

    def recordize(self, df):
        new_columns = {c : normalize(c) for c in df.columns}
        return df.rename(columns = new_columns).to_dict(orient='records')

    def batch_insert(self, df, table):
        aggressive_tuples = [[aggressive_quote(entry) for entry in row] for row in list(df.itertuples(index=False, name=None))]
        quote = lambda _tuple: '(%s)' % ', '.join(["'%s'" % value if isinstance(value, str) else str(value) for value in list(_tuple)])
        quoted_tuples = [quote(t) for t in aggressive_tuples]
        values = re.sub(r"(?<=\W)(nan|None)(?=\W)", "NULL", (",\n" + " " * 7).join(quoted_tuples))
        return f"INSERT INTO {table} VALUES {values};"
    
    def get_tables(self, readable_labels=False):
        if not readable_labels:
            return self.doc_tables
        else:
            return self.doc_tables_labels

    def get_fields(self, readable_labels=False):
        if not readable_labels:
            return self.doc_fields
        else:
            return self.doc_fields_labels

    def get_creation_script(self, readable_labels=False):
        template = jinja_environment.from_string(create_db_template)
        sql_create = template.render(
            tables = self.get_tables(readable_labels=readable_labels),
            fields = self.get_fields(readable_labels=readable_labels),
            reference_table_statements = self.reference_table_statements,
            unique_rows = self.unique_rows,
        )
        return sql_create
