
from .parse_reference import ADISchemaImporter
from .html import ADIHTMLDocGenerator
from .sql import ADISQLGenerator
from .owl import OWLGenerator
from .yaml import YAMLGenerator
from .d2 import D2Generator

class ADISchemaConverter:
    def __init__(self, schema_source_dir, unique_rows: bool=False):
        self.importer = ADISchemaImporter(schema_source_dir)
        self.unique_rows = unique_rows

    def generate_export_formats(self):
        tables = self.importer.get_tables()
        token = self.get_domain_token()
        prefix = self.get_domain_prefix()
        version = self.get_version_string()
        html_generator = ADIHTMLDocGenerator(tables, token)
        sql_generator = ADISQLGenerator(tables, token, version, unique_rows=self.unique_rows)
        owl_generator = OWLGenerator(tables, token, prefix, version)
        yaml_generator = YAMLGenerator(tables)
        d2_generator = D2Generator(tables, token, prefix, version)

        return {
            'HTML' : html_generator.get_html_fragments(),
            'OWL' : owl_generator.get_ontology(),
            'SQL' : sql_generator.get_creation_script(),
            'SQL with labels' : sql_generator.get_creation_script(readable_labels=True),
            'YAML' : yaml_generator.get_hierarchical_format(),
            'YAML def' : yaml_generator.get_hierarchical_format(key_definition_feature=True),
            'D2 diagram source' : d2_generator.get_source(),
            'Frictionless Data' : {
                'data_package.json' : '',
                'other.tsv' : '',
            }
        }

    def generate_sql(self):
        tables = self.importer.get_tables()
        token = self.get_domain_token()
        version = self.get_version_string()
        sql_generator = ADISQLGenerator(tables, token, version, unique_rows=self.unique_rows)
        return {
            'SQL' : sql_generator.get_creation_script(),
            'SQL with labels' : sql_generator.get_creation_script(readable_labels=True),
        }

    def get_domain_token(self):
        return self.importer.get_domain_token()

    def get_domain_prefix(self):
        return self.importer.get_domain_prefix()

    def get_version_string(self):
        return self.importer.get_version_string()
