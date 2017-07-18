import osmium as o
import geojson
from constants import *


class Member:
    def __init__(self, m_id, tags):
        self.id = m_id
        self.tags = {tag.k: tag.v for tag in tags} if tags is not None else None


class Node(Member):
    def __init__(self, osm_node):
        Member.__init__(self, osm_node.id, osm_node.tags)
        self.lat = osm_node.location.lat
        self.lon = osm_node.location.lon


class Way(Member):
    def __init__(self, osm_way):
        Member.__init__(self, osm_way.id, osm_way.tags)
        self.needed_nodes = []
        self.nodes = []

    def add_needed_nodes(self, n_id):
        self.needed_nodes.append(n_id)

    def is_needed(self, n_id):
        return n_id in self.needed_nodes


class Relation(Member):
    def __init__(self, osm_relation=None):
        if osm_relation is not None:
            Member.__init__(self, osm_relation.id, osm_relation.tags)
        else:
            Member.__init__(self, None, None)

        self.__needed_ways = set()
        self.ways = []
        self.child_relations = []

    def add_needed_way(self, w_id):
        self.__needed_ways.add(w_id)

    def is_needed(self, w_id):
        if w_id in self.__needed_ways:
            return True
        else:
            for child in self.child_relations:
                if child.is_needed(w_id):
                    return True

        return False


class CycleRouteHandler(o.SimpleHandler):
    def __init__(self, routes):
        super(CycleRouteHandler, self).__init__()
        self.routes = routes
        self.relations = {}
        self.needed_relations = {}

    def relation(self, r):
        tags = r.tags
        self.needed_relations[r.id] = set()
        self.relations[r.id] = Relation(r)

        if 'type' in tags and tags['type'] == TYPE_TAG \
                and 'route' in tags and tags['route'] == ROUTE_TAG \
                and 'network' in tags and tags['network'] == NETWORK_TAG \
                and 'operator' in tags and tags['operator'] == OPERATOR_TAG \
                and 'ref' in tags and tags['ref'] in self.routes:
            relation = Relation(r)

            for member in r.members:
                if member.type == 'w':
                    relation.add_needed_way(member.ref)
                elif member.type == 'r':
                    self.needed_relations[r.id].add(member.ref)

            self.routes[tags['ref']] = relation


class RelationHandler(o.SimpleHandler):
    def __init__(self, routes):
        super(RelationHandler, self).__init__()
        self.routes = routes

    def way(self, w):
        for route in filter(lambda x: x is not None, self.routes.values()):
            if route.is_needed(w.id):
                way = Way(w)
                route.ways.append(way)

                for member in w.nodes:
                    way.add_needed_nodes(member.ref)


class WayHandler(o.SimpleHandler):
    def __init__(self, needed_nodes):
        super(WayHandler, self).__init__()
        self.needed_nodes = needed_nodes
        self.nodes = {}

    def node(self, n):
        if n.id in self.needed_nodes:
            self.nodes[n.id] = Node(n)


def extract_routes():
    with open("routes") as fp:
        routes = {route.strip(): None for route in fp.readlines()}

    cycle_handler = CycleRouteHandler(routes)
    cycle_handler.apply_file(OSM_LOCATION)

    for r_id in cycle_handler.needed_relations.keys():
        route = cycle_handler.relations[r_id]
        for needed in cycle_handler.needed_relations[r_id]:
            route.child_relations.append(cycle_handler.relations[needed])

    relation_handler = RelationHandler(cycle_handler.routes)
    relation_handler.apply_file(OSM_LOCATION)

    routes = relation_handler.routes

    needed_nodes = set()
    for route in filter(lambda x: x is not None, routes.values()):
        for way in route.ways:
            needed_nodes = needed_nodes.union(set(way.needed_nodes))

    way_handler = WayHandler(needed_nodes)
    way_handler.apply_file(OSM_LOCATION, locations=True)
    nodes = way_handler.nodes

    for route in filter(lambda x: x is not None, routes.values()):
        for way in route.ways:
            for id in way.needed_nodes:
                way.nodes.append(nodes[id])

    for route in routes:
        if routes[route] is None:
            routes[route] = Relation()

    return routes


def dump_geojson(route, relation):
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
    relations = extract_routes()
    for route in relations:
        dump_geojson(route, relations[route])
