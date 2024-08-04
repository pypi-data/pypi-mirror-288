import re

import oyaml as yaml

from .entity_dag import EntityGraph
from .tree_resolver import TreeResolver

from .log_formats import colorized_logger
logger = colorized_logger(__name__)


def get_schema_dataframes(tables):
    keys = ['tables', 'fields', 'entities', 'properties', 'values']
    return [tables[key] for key in keys]

class YAMLGenerator:
    def __init__(self, tables):
        G = EntityGraph(*get_schema_dataframes(tables))
        resolver = TreeResolver(G)
        resolver.resolve_trees()
        self.objectification = resolver.get_objectification()

    def get_hierarchical_format(self, key_definition_feature=False):
        serialization = yaml.safe_dump(self.objectification, width=2500, indent=2)
        if key_definition_feature:
            serialization = re.sub('\n +def:', '', serialization)
        return serialization
