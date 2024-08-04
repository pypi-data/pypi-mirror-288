from collections import OrderedDict

from .log_formats import colorized_logger
logger = colorized_logger(__name__)


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
        if len(basin_combinations) > 0:
            mvalue = max([sum(c) for c in basin_combinations])
        else:
            mvalue = ''
        logger.info('Computed %s basin combinations, with maximum cardinality of occurring index set %s.', len(basin_combinations), mvalue)
        basin_combinations = sorted(list(set(basin_combinations)))
        logger.info('Reduced to %s non-repeating basin combinations.', len(basin_combinations))
        if len(basin_combinations) > 0:
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
                if isinstance(root, list):
                    for j, element in enumerate(root[1:]):
                        special_key = (combination, j)
                        self.roots[special_key] = element
                else:
                    self.roots[combination] = root
        for combination in self.partition.keys():
            if combination in self.roots:
                root = self.roots[combination]
                part = self.partition[combination]
                part_node_names = [node.get_short_name() for node in part]
                logger.info('Maximal node "%s" (%s) is a directed root of "%s".', root.get_short_name(), combination, ' '.join(part_node_names))
            else:
                logger.warning('Root not found for (%s) part.', combination)
        for combination in self.roots:
            if not combination in self.partition.keys():
                root = self.roots[combination]
                special_key = combination
                key_base = combination[0]
                if not key_base in self.partition.keys():
                    logger.error('Dangling combination: %s', combination)
                part = self.partition[key_base]
                part_node_names = [node.get_short_name() for node in part]
                logger.info('Maximal node "%s" (one of multiple) found for part "%s".', root.get_short_name(), ' '.join(part_node_names))

    def get_root(self, part):
        root = None
        part_node_names = [node.get_short_name() for node in part]
        maximal_nodes = []
        for node in part:
            parents = [parent for parent in node.get_parents() if parent.get_short_name() in part_node_names]
            if len(parents) == 0:
                maximal_nodes.append(node)
        if len(maximal_nodes) > 1:
            logger.warn('Component %s has multiple maximal nodes.', part_node_names)
            if len(maximal_nodes) == 2:
                if not self.dag.are_linked(maximal_nodes[0], maximal_nodes[1]):
                    logger.info('Component %s has 2 maximal nodes, but they are not connected, so these are being split. You should check that their basins are disjoint.', part_node_names)
                    return maximal_nodes
                else:
                    logger.error('Cannot identify maximal node(s) for component %s.', part_node_names)
            else:
                logger.error('Cannot identify maximal node(s) for component %s.', part_node_names)
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

    def get_objectification(self):
        self.dag.clear_serialization_visitation_states()
        object_components = []
        used_components = []
        while not self.dag.all_nodes_serialized():
            remaining = set(self.roots.keys()).difference(used_components)
            if len(remaining) == 0:
                break
            combination = max(remaining, key=lambda combination: self.evaluate_size(self.compute_root_objectification(combination)))
            logger.debug('Largest part is sized: %s', self.evaluate_size(self.compute_root_objectification(combination)))
            object_components.append(self.compute_root_objectification(combination, mark_nodes_visited=True))
            used_components.append(combination)

        objectification = OrderedDict()
        for c in object_components:
            objectification.update(c)
        self.dag.clear_serialization_visitation_states()
        return objectification

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
            o = self.compute_objectification(edge.get_target(), mark_nodes_visited=mark_nodes_visited)
            if edge.is_entitylike():
                if 'ref' in o.keys():
                    subobjects[o['ref']] = '(ref)'
                else:
                    subobjects.update(o)
            else:
                property_section['def'] = edge.get_definition()
                property_section.update(o)
                subobjects[edge.get_name()] = property_section

        if mark_nodes_visited:
            node.declare_used_in_serialization()

        return OrderedDict({node.get_name() : subobjects})

    def evaluate_size(self, objectification):
        values = list(objectification.values())[0]
        if type(values) == str:
            return 1
        return len(values)
