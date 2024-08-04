
from .log_formats import colorized_logger
logger = colorized_logger(__name__)

from .dag import DAGNode
from .dag import DAGEdge

class TableNode(DAGNode):
    def __init__(self, row, entities):
        super(TableNode, self).__init__()
        self.name = row['Label']
        self.full_name = row['Entity']
        self.definition = self.retrieve_definition(row, entities)
        self.edges = []
        self.primitives = []

    def get_name(self):
        return self.name

    def get_definition(self):
        return self.definition

    def get_primitives(self):
        return self.primitives

    def retrieve_definition(self, row, entities):
        for i, entity in entities.iterrows():
            if row['Entity'] == entity['Label']:
                return entity['Definition']
        logger.warning('Could not retrieve entity definition. Table row: %s', str(row))

    def set_short_name(self, short_name):
        self.short_name = short_name

    def add_primitive(self, primitive):
        self.primitives.append(primitive)

    def declare_used_in_serialization(self):
        self.used_in_serialization = True

    def clear_serialization_visitation_state(self):
        self.used_in_serialization = False

    def was_used_in_serialization(self):
        return self.used_in_serialization

class LinkEdge(DAGEdge):
    def __init__(self, row, properties, entities, nodes):
        if not LinkEdge.is_link_edge(row, properties, entities, nodes):
            logger.warning('Row is not a table-link edge: ', str(row))
        self.name = row['Label']
        self.full_name = row['Property']
        self.definition = LinkEdge.retrieve_propertylike_definition(row, properties, entities)
        self.source = LinkEdge.select_node_named(row['Table'], nodes)
        self.target = LinkEdge.select_node_named(row['Foreign table'], nodes)
        self.target_field_name = row['Foreign key']
        self.source.add_edge(self)
        self.target.register_as_target_of_edge(self)
        self.entitylike = str(row['Property']) in list(entities['Label'])

    def get_name(self):
        return self.name

    def get_definition(self):
        return self.definition

    def is_entitylike(self):
        return self.entitylike

    @staticmethod
    def is_link_edge(row, properties, entities, nodes):
        if row['Foreign table'] != '':
            return True
        else:
            return False

    @staticmethod
    def select_node_named(name, nodes):
        for node in nodes:
            if node.name == name:
                return node

    @staticmethod
    def retrieve_propertylike_definition(row, properties, entities):
        if str(row['Property']) in list(properties['Label']):
            for i, prop in properties.iterrows():
                if prop['Label'] == row['Property']:
                    return prop['Definition']
        if str(row['Property']) in list(entities['Label']):
            for i, entity in entities.iterrows():
                if entity['Label'] == row['Property']:
                    return entity['Definition']
        logger.warning('Could not look up propertylike definition for item name: %s', row['Property'])

class PrimitiveProperty:
    def __init__(self, row, properties, entities):
        if not PrimitiveProperty.is_primitive_property(row, properties, entities):
            logger.warning('Not a primitive property: %s', str(row))
        self.name = row['Label']
        self.full_name = row['Property']
        self.definition = LinkEdge.retrieve_propertylike_definition(row, properties, entities)
        self.value_type = PrimitiveProperty.get_value_type(row, properties, entities)

    def get_name(self):
        return self.name

    def get_definition(self):
        return self.definition

    @staticmethod
    def is_primitive_property(row, properties, entities):
        if (str(row['Property']) in list(entities['Label'])) and (row['Foreign table'] == ''):
            return True
        if (str(row['Property']) in list(entities['Label'])) and (row['Foreign table'] != ''):
            return False
        if str(row['Property']) in list(properties['Label']):
            for i, prop in properties.iterrows():
                if prop['Label'] == row['Property']:
                    value_type = prop['Value type']
            value_type = PrimitiveProperty.get_value_type(row, properties, entities)
        if value_type in ['String', 'Float', 'Entity']:
            return True
        else:
            return False

    @staticmethod
    def get_value_type(row, properties, entities):
        for i, prop in properties.iterrows():
            if prop['Label'] == row['Property']:
                return str(prop['Value type'])

class EntityGraph:
    def __init__(self, tables, fields, entities, properties, values):
        self.nodes = [TableNode(row, entities) for i, row in tables.iterrows()]
        self.edges = []
        for i, row in fields.iterrows():
            if LinkEdge.is_link_edge(row, properties, entities, self.nodes):
                self.edges.append(LinkEdge(row, properties, entities, self.nodes))
            elif PrimitiveProperty.is_primitive_property(row, properties, entities):
                LinkEdge.select_node_named(row['Table'], self.nodes).add_primitive(
                    PrimitiveProperty(row, properties, entities)
                )
            else:
                logger.warning('Field row is neither a link edge nor a primitive property: %s', row)
        self.assign_short_names()

    def get_nodes(self):
        return self.nodes

    def assign_short_names(self):
        short_names = []
        for node in self.nodes:
            short_name = self.create_short_name(node.name)
            if not short_name in short_names:
                short_names.append(short_name)
            else:
                short_name = self.create_short_name(node.name, alternative=True)
                if not short_name in short_names:
                    short_names.append(short_name)
                else:
                    logger.debug('Error: Need more sophisticated short names. Duplicates not removed properly.')
            node.set_short_name(short_name)

    def create_short_name(self, name, alternative=False):
        tokens = name.split(' ')
        if alternative:
            return ''.join([token[0].lower() for token in tokens]) + tokens[-1][-1]
        else:
            return ''.join([token[0].lower() for token in tokens])

    def clear_serialization_visitation_states(self):
        for node in self.get_nodes():
            node.clear_serialization_visitation_state()

    def all_nodes_serialized(self):
        return all([node.was_used_in_serialization() for node in self.get_nodes()])

    def are_linked(self, node1, node2):
        for node in node1.get_edges():
            if node.get_short_name() == node2.get_short_name():
                return True
        for node in node2.get_edges():
            if node.get_short_name() == node1.get_short_name():
                return True
        return False
