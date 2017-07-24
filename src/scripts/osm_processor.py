import osmium as o
import geojson

from constants import *


class Member:
    """
    OSM Member with an ID and tags.
    """

    def __init__(self, m_id, tags):
        self.id = m_id
        self.tags = {tag.k: tag.v for tag in tags} if tags is not None else None


class Node(Member):
    """
    OSM Node with a location.
    """

    def __init__(self, osm_node):
        Member.__init__(self, osm_node.id, osm_node.tags)
        self.lat = osm_node.location.lat
        self.lon = osm_node.location.lon


class Way(Member):
    """
    OSM Way consisting of a list of nodes.
    """

    def __init__(self, osm_way):
        Member.__init__(self, osm_way.id, osm_way.tags)
        self.needed_nodes = []
        self.nodes = []

    def add_needed_nodes(self, n_id):
        """
        Adds a node ID to the needed nodes list for this way.

        :param n_id: ID of the node.
        """
        self.needed_nodes.append(n_id)

    def is_needed(self, n_id):
        """
        Check if the node with given ID is needed in this way.

        :param n_id: ID of the node.
        :return: True if needed, or False otherwise.
        """
        return n_id in self.needed_nodes


class Relation(Member):
    """
    OSM Relation consisting of ways or child relations
    """

    def __init__(self, osm_relation=None):
        if osm_relation is not None:
            Member.__init__(self, osm_relation.id, osm_relation.tags)
        else:
            Member.__init__(self, None, None)

        self.__needed_ways = set()
        self.ways = []
        self.child_relations = []

    def add_needed_way(self, w_id):
        """
        Adds a way ID to the needed ways for this relation.

        :param w_id: ID of the way.
        """
        self.__needed_ways.add(w_id)

    def is_needed(self, w_id):
        """
        Checks if the way with given ID is needed in this relation or its child relations.

        :param w_id: ID of the way.
        :return: True if needed, or False otherwise.
        """
        if w_id in self.__needed_ways:
            return True
        else:
            for child in self.child_relations:
                if child.is_needed(w_id):
                    return True

        return False


class CycleRouteHandler(o.SimpleHandler):
    """
    Loops over the relations in the OSM data to find the routes we need.
    """

    def __init__(self, routes):
        super(CycleRouteHandler, self).__init__()
        self.routes = routes
        self.relations = {}
        self.needed_relations = {}
        self.empty = True

    def relation(self, r):
        self.empty = False
        tags = r.tags
        self.needed_relations[r.id] = set()
        self.relations[r.id] = Relation(r)

        # Check if it's a cycling route corresponding to the reference data.
        if 'type' in tags and tags['type'] == TYPE_TAG \
                and 'route' in tags and tags['route'] == ROUTE_TAG \
                and 'network' in tags and tags['network'] == NETWORK_TAG \
                and 'operator' in tags and tags['operator'] == OPERATOR_TAG \
                and 'ref' in tags and tags['ref'] in self.routes:
            relation = Relation(r)

            for member in r.members:
                # Loop over the members to find the ways or child relations we need.

                if member.type == 'w':
                    relation.add_needed_way(member.ref)
                elif member.type == 'r':
                    self.needed_relations[r.id].add(member.ref)

            self.routes[tags['ref']] = relation


class RelationHandler(o.SimpleHandler):
    """
    Loops over the ways to find the ones we need for the relations.
    """

    def __init__(self, routes):
        super(RelationHandler, self).__init__()
        self.routes = routes

    def way(self, w):
        for route in filter(lambda x: x is not None, self.routes.values()):
            if route.is_needed(w.id):
                way = Way(w)
                route.ways.append(way)

                for member in w.nodes:
                    # Loop over the nodes to find the nodes we need.

                    way.add_needed_nodes(member.ref)


class WayHandler(o.SimpleHandler):
    """
    Loop over the nodes to find the ones we need for the ways.
    """

    def __init__(self, needed_nodes):
        super(WayHandler, self).__init__()
        self.needed_nodes = needed_nodes
        self.nodes = {}

    def node(self, n):
        if n.id in self.needed_nodes:
            self.nodes[n.id] = Node(n)


def extract_routes():
    """
    Extracts the route relations from the OSM data.

    :return: Dictionary containing the relation for each route.
    """
    # Get all the route names from the route file and make a dictionary to store the relations in.
    with open("routes") as fp:
        routes = {route.strip(): None for route in fp.readlines()}

    # Find the relations.
    cycle_handler = CycleRouteHandler(routes)
    cycle_handler.apply_file(OSM_LOCATION)

    # Check if the OSM data was empty, as it means something is wrong.
    if cycle_handler.empty:
        raise Exception("The OSM data seems to be empty. Cannot continue.")

    # Add all the child relations to the relations
    for r_id in cycle_handler.needed_relations.keys():
        route = cycle_handler.relations[r_id]
        for needed in cycle_handler.needed_relations[r_id]:
            route.child_relations.append(cycle_handler.relations[needed])

    # Find the ways.
    relation_handler = RelationHandler(cycle_handler.routes)
    relation_handler.apply_file(OSM_LOCATION)

    routes = relation_handler.routes

    # Determine the needed nodes for every relation.
    needed_nodes = set()
    for route in filter(lambda x: x is not None, routes.values()):
        for way in route.ways:
            needed_nodes = needed_nodes.union(set(way.needed_nodes))

    # Find the nodes.
    way_handler = WayHandler(needed_nodes)
    way_handler.apply_file(OSM_LOCATION, locations=True)
    nodes = way_handler.nodes

    # Add all the nodes to their corresponding relation.
    for route in filter(lambda x: x is not None, routes.values()):
        for way in route.ways:
            for id in way.needed_nodes:
                way.nodes.append(nodes[id])

    for route in routes:
        if routes[route] is None:
            routes[route] = Relation()

    return routes


def dump_geojson(route, relation):
    """
    Writes the route relation as a GeoJSON file.

    :param route: Name of the route.
    :param relation: Route relation to dump to GeoJSON.
    """
    features = []
    multi_line_string = geojson.MultiLineString([
        [
            (node.lon, node.lat) for node in way.nodes
        ]
        for way in relation.ways
    ])
    features.append(geojson.Feature(geometry=multi_line_string, properties=relation.tags))

    with open(OSM_ROUTES_LOCATION + route + ".geojson", "w") as fp:
        fp.write(geojson.dumps(geojson.FeatureCollection(features)))


def process_osm():
    """
    Extracts the cycling routes from OSM and output them as GeoJSON.
    """
    relations = extract_routes()
    for route in relations:
        dump_geojson(route, relations[route])
