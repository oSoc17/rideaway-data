import osmium as o
import geojson

OSM_LOCATION = "../data/map.osm"
OUTPUT_LOCATION = "../data/"

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

    def add_needed_way(self, w_id):
        self.__needed_ways.add(w_id)

    def is_needed(self, w_id):
        return w_id in self.__needed_ways


class CycleRouteHandler(o.SimpleHandler):
    def __init__(self, relations):
        super(CycleRouteHandler, self).__init__()
        self.relations = relations

    def relation(self, r):
        tags = r.tags

        if 'type' in tags and tags['type'] == 'route' \
                and 'route' in tags and tags['route'] == 'bicycle' \
                and 'network' in tags and tags['network'] == 'lcn'\
                and 'ref' in tags and self.relations.has_key(tags['ref']):
            relation = Relation(r)

            for member in r.members:
                relation.add_needed_way(member.ref)

            self.relations[tags['ref']] = relation


class RelationHandler(o.SimpleHandler):
    def __init__(self, relations):
        super(RelationHandler, self).__init__()
        self.relations = relations

    def way(self, w):
        for relation in filter(lambda x: x is not None, self.relations.values()):
            if relation.is_needed(w.id):
                way = Way(w)
                relation.ways.append(way)

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


def extract_relations():
    with open("routes") as fp:
        relations = {route.strip(): None for route in fp.readlines()}

    cycle_handler = CycleRouteHandler(relations)
    cycle_handler.apply_file(OSM_LOCATION)

    relation_handler = RelationHandler(cycle_handler.relations)
    relation_handler.apply_file(OSM_LOCATION)

    relations = relation_handler.relations

    needed_nodes = set()
    for relation in filter(lambda x: x is not None, relations.values()):
        for way in relation.ways:
            needed_nodes = needed_nodes.union(set(way.needed_nodes))

    way_handler = WayHandler(needed_nodes)
    way_handler.apply_file(OSM_LOCATION, locations=True)
    nodes = way_handler.nodes

    for relation in filter(lambda x: x is not None, relations.values()):
        for way in relation.ways:
            for id in way.needed_nodes:
                way.nodes.append(nodes[id])

    for route in relations:
        if relations[route] is None:
            relations[route] = Relation()

    return relations


def dump_geojson(route, relation):
    features = []
    multi_line_string = geojson.MultiLineString([
        [
            (node.lon, node.lat) for node in way.nodes
        ]
        for way in relation.ways
    ])
    features.append(geojson.Feature(geometry=multi_line_string, properties=relation.tags))

    with open(OUTPUT_LOCATION + route + ".geojson", "w") as fp:
        fp.write(geojson.dumps(geojson.FeatureCollection(features)))


if __name__ == '__main__':
    relations = extract_relations()
    for route in relations:
        dump_geojson(route, relations[route])
