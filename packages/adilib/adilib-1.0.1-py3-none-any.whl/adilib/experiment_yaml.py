import importlib.resources
import json
import oyaml as yaml
from collections import OrderedDict

import adiscstudies
import pandas as pd

from .log_formats import colorized_logger
logger = colorized_logger(__name__)

class DAGNode:
    def __init__(self):
        self.edges = []
        self.in_edges = []

    def get_short_name(self):
        return self.short_name

    def get_edges(self):
        return self.edges

    def add_edge(self, edge):
        if edge.get_source() != self:
            logger.warning('Bad edge registration, source node does not match.')
        else:
            self.edges.append(edge)

    def register_as_target_of_edge(self, edge):
        self.in_edges.append(edge)

    def get_parents(self):
        return [edge.source for edge in self.in_edges]

class DAGEdge:
    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

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

def get_schema_dataframes():
    filenames = [base + '.tsv' for base in ['tables', 'fields', 'entities', 'properties', 'values']]
    dataframes = []
    for filename in filenames:
        with importlib.resources.path('adiscstudies', filename) as path:
            dataframes.append(pd.read_csv(path, sep='\t', keep_default_na=False))
    return dataframes

class TreeResolver:
    def __init__(self, dag):
        self.dag = dag

    def resolve_trees(self):
        self.compute_root_nodes()
        self.compute_downstream_basins()
        self.compute_occurring_basin_combinations()
        self.compute_strict_intersection_graphs()
        self.compute_graph_partition()
        self.verify_parts_are_rooted_trees()
        self.create_object_serialization()

    def compute_root_nodes(self):
        self.root_nodes = [
            node for node in self.dag.get_nodes() if node.get_parents() == []
        ]
        logger.info('Found %s root nodes.', len(self.root_nodes))
        logger.info([n.name for n in self.root_nodes])

    def compute_downstream_basins(self):
        self.downstream_basins = [
            self.compute_downstream_basin(node) for node in self.root_nodes
        ]
        logger.info('Computed %s downstream basin sets. Maximum cardinality encountered is %s.', len(self.downstream_basins), max([len(b) for b in self.downstream_basins]))

    def compute_downstream_basin(self, root_node):
        return self.downstream_basin_of_node(root_node)

    def downstream_basin_of_node(self, node):
        basins = [self.downstream_basin_of_node(n) for n in [edge.get_target() for edge in node.get_edges()]]
        nodes_by_name = {}
        for basin in basins:
            for n in basin:
                nodes_by_name[n.get_short_name()] = n
        nodes_by_name[node.get_short_name()] = node
        return list(nodes_by_name.values())

    def compute_occurring_basin_combinations(self):
        basin_combinations = [
            self.get_basin_membership_vector(node)
            for node in self.dag.get_nodes()
        ]
        basin_combinations = [c for c in basin_combinations if sum(c) > 1]
        logger.info('Computed %s basin combinations, with maximum cardinality of occurring index set %s.', len(basin_combinations), max([sum(c) for c in basin_combinations]))
        basin_combinations = sorted(list(set(basin_combinations)))
        logger.info('Reduced to %s non-repeating basin combinations.', len(basin_combinations))
        singletons = len(basin_combinations[0])
        logger.info('Restored the %s singletons combinations.', len(basin_combinations[0]))
        basin_combinations = [tuple([1 if i == j else 0 for i in range(singletons)]) for j in range(singletons)] + basin_combinations
        for c in basin_combinations:
            logger.info(c)
        self.basin_combinations = basin_combinations

    def get_basin_membership_vector(self, node):
        return tuple([
            1 if node.get_short_name() in [n.get_short_name() for n in basin] else 0
            for basin in self.downstream_basins
        ])

    def compute_strict_intersection_graphs(self):
        self.intersection_graph_node_sets = {
            basin_membership_vector : self.compute_intersection_graph(basin_membership_vector)
            for basin_membership_vector in self.basin_combinations
        }
        for s in self.intersection_graph_node_sets.values():
            logger.debug('Intersection graph node set: ' + ' '.join([n.get_short_name() for n in s]))

    def compute_intersection_graph(self, basin_membership_vector):
        all_names = set([node.get_short_name() for node in self.dag.get_nodes()])
        names = all_names.intersection(*[
            [node.get_short_name() for node in basin]
            for i, basin in enumerate(self.downstream_basins) if basin_membership_vector[i] == 1
        ])
        node_set = [node for node in self.dag.get_nodes() if node.get_short_name() in names]
        return node_set

    def compute_graph_partition(self):
        self.partition = {}
        for length in sorted(list(set([sum(v) for v in self.intersection_graph_node_sets.keys()]))):
            basin_combinations_stratum = self.get_vectors_of_length(length)
            for basin_membership_vector in basin_combinations_stratum:
                logger.debug('Creating partition part for combination: %s', basin_membership_vector)
                subtractable_combinations = [higher_vector for higher_vector in self.get_vectors_of_greater_than_length(length)]
                node_set = self.intersection_graph_node_sets[basin_membership_vector]
                logger.debug('Current elements: %s', self.get_short_names_of_combination(basin_membership_vector))
                logger.debug('Removing all nodes in %s-fold (or more) intersections: %s', length+1, [self.get_short_names_of_combination(c) for c in subtractable_combinations])
                pared_down = list(set([node.get_short_name() for node in node_set]).difference(
                    set().union(*[
                        [node.get_short_name() for node in self.intersection_graph_node_sets[subtractable_combination]]
                        for subtractable_combination in subtractable_combinations
                    ])
                ))
                logger.debug('Remaining nodes: %s', pared_down)
                self.partition[basin_membership_vector] = [node for node in self.dag.get_nodes() if node.get_short_name() in pared_down]

        for vector, part in self.partition.items():
            logger.info('Partition part labelled by combination %s: %s', vector, ' '.join([node.get_short_name() for node in part]))
        if self.verify_is_partition():
            logger.info('Partition verified, parts are exhaustive and mutually exclusive.')
        logger.info('Part sizes: %s', ' '.join([str(len(part)) for part in self.partition.values()]))

    def get_short_names_of_combination(self, combination):
        return [n.get_short_name() for n in self.intersection_graph_node_sets[combination]]

    def get_vectors_of_length(self, length):
        return [v for v in self.intersection_graph_node_sets.keys() if sum(v) == length]

    def get_vectors_of_greater_than_length(self, length):
        return [v for v in self.intersection_graph_node_sets.keys() if sum(v) > length]

    def verify_is_partition(self):
        parts = self.partition.values()
        for p in parts:
            p_names = self.get_short_names(p)
            for q in parts:
                q_names = self.get_short_names(q)
                if not ((p_names == q_names) or (len(set(p_names).intersection(q_names))==0)):
                    logger.warn('Not a partition, because of these parts:')
                    logger.warn('%s', ' '.join(p_names))
                    logger.warn('%s', ' '.join(q_names))
                    return False
        all_parts_contents = set().union(*[self.get_short_names(part) for part in parts])
        all_names = set([node.get_short_name() for node in self.dag.get_nodes()])
        if all_parts_contents != all_names:
            logger.warn('Partition is possibly missing some nodes. Partition nodes: %s', ' '.join(list(all_parts_contents)))
            return False
        return True

    def get_short_names(self, nodes):
        return sorted([n.get_short_name() for n in nodes])

    def verify_parts_are_rooted_trees(self):
        self.roots = {}
        for combination, part in self.partition.items():
            root = self.get_root(part)
            if not root is None:
                self.roots[combination] = root
        for combination in self.partition.keys():
            if combination in self.roots:
                root = self.roots[combination]
                part = self.partition[combination]
                part_node_names = [node.get_short_name() for node in part]
                logger.info('Maximal node "%s" is a directed root of "%s".', root.get_short_name(), ' '.join(part_node_names))
            else:
                logger.error('Root not found for part: %s', ' '.join(part_node_names))

    def get_root(self, part):
        root = None
        part_node_names = [node.get_short_name() for node in part]
        maximal_nodes = []
        for node in part:
            parents = [parent for parent in node.get_parents() if parent.get_short_name() in part_node_names]
            if len(parents) == 0:
                maximal_nodes.append(node)
        if len(maximal_nodes) > 1:
            logger.error('Component %s has multiple maximal nodes.', part_node_names)
        if len(maximal_nodes) == 0:
            logger.error('Component %s has no maximal nodes?', part_node_names)
        if len(maximal_nodes) == 1:
            maximal_node = maximal_nodes[0]
            logger.info('One maximal node: %s  (for %s)', maximal_node.get_short_name(), ' '.join(part_node_names))
        basin = sorted(list(self.get_downstream_basin_names(maximal_node, part_node_names)))
        if basin != sorted(part_node_names):
            logger.error('Unique maximal node %s is not a root of %s.', maximal_node.get_short_name(), part_node_names)
        else:
            root = maximal_node
        return root

    def get_downstream_basin_names(self, node, relative_context_node_names):
        basins = [self.get_downstream_basin_names(n, relative_context_node_names) for n in [edge.get_target() for edge in node.get_edges()] if n.get_short_name() in relative_context_node_names]
        return set([node.get_short_name()]).union(*basins)

    def create_object_serialization(self):
        self.dag.clear_serialization_visitation_states()

        serializable_components = []
        used_components = []
        while not self.dag.all_nodes_serialized():
            remaining = set(self.partition.keys()).difference(used_components)
            if len(remaining) == 0:
                break
            combination = max(remaining, key=lambda combination: self.evaluate_size(self.compute_root_objectification(combination)))
            logger.debug('Largest part is sized: %s', self.evaluate_size(self.compute_root_objectification(combination)))
            serializable_components.append(self.compute_root_objectification(combination, mark_nodes_visited=True))
            used_components.append(combination)

        serializations = [yaml.safe_dump(c, width=1200, indent=2) for c in serializable_components]
        print('\n'.join(serializations))
        self.serializable_components = serializable_components

    def compute_root_objectification(self, combination, mark_nodes_visited=False):
        root = self.roots[combination]
        return self.compute_objectification(root, mark_nodes_visited=mark_nodes_visited)

    def compute_objectification(self, node, mark_nodes_visited=False):
        if node.was_used_in_serialization():
            return OrderedDict({'ref' : node.get_name()})
        subobjects = OrderedDict()
        subobjects['def'] = node.get_definition()

        for primitive in node.get_primitives():
            subobjects[primitive.get_name()] = primitive.get_definition()

        for edge in node.get_edges():
            property_section = OrderedDict()
            if not edge.is_entitylike():
                property_section['def'] = edge.get_definition()
                o = self.compute_objectification(edge.get_target(), mark_nodes_visited=mark_nodes_visited)
                property_section.update(o)
                subobjects[edge.get_name()] = property_section
            else:
                o = self.compute_objectification(edge.get_target(), mark_nodes_visited=mark_nodes_visited)
                if 'ref' in o.keys():
                    subobjects[o['ref']] = '(ref)'
                else:
                    subobjects.update(o)

        if mark_nodes_visited:
            node.declare_used_in_serialization()

        return OrderedDict({node.get_name() : subobjects})

    def evaluate_size(self, objectification):
        values = list(objectification.values())[0]
        if type(values) == str:
            return 1
        return len(values)

