import json
from typing import List, Dict


def find_path(building_key: str, hall_index_from: str, hall_index_to: str) -> List[Dict]:
    """
    :param building_key: "main" или "gallery"
    :param hall_index: для "main" - значение из списка ["1", ..., "11"], ["14", "15", "16", "16a", "17"..., "30"]
                       для "gallery" - значение из списка ["8", ..., "26"]
    :return: список объектов, которые надо пройти, в одном из двух форматов:
        * {"type": "hall", "index": "hall_index", "floor": <number>}
        * {"type": "stairs", "direction": "up" или "down"} 
    """
    building = buildings[building_key]
    path = building.find_path(hall_index_from, hall_index_to)
    return path


class Building:
    def __init__(self, info):
        self.nodes = []
        self.edges = {}
        self.hall_to_node = {}

        def get_or_add_node(hall, floor):
            node = self.hall_to_node.get(hall)
            if node is None:
                node = len(self.hall_to_node)
                self.hall_to_node[hall] = node
                self.nodes.append({'type': 'hall', 'index': hall, 'floor': floor})
                return node
            else:
                return node

        def add_edge(node1, node2):
            self.edges.setdefault(node1, []).append(node2)
            self.edges.setdefault(node2, []).append(node1)

        for floor_info in info['floors']:
            floor = floor_info['floor']
            for hall1, hall2 in floor_info['halls_edges']:
                node1 = get_or_add_node(hall1, floor)
                node2 = get_or_add_node(hall2, floor)
                add_edge(node1, node2)

        for stairs_index, stairs_info in enumerate(info['stairs']):
            stairs_node = len(self.nodes)
            self.nodes.append({'type': 'stairs', 'index': stairs_index})
            for key in ['halls_near_bottom', 'halls_near_up']:
                for hall in stairs_info[key]:
                    add_edge(stairs_node, self.hall_to_node[hall])

    def find_path(self, hall_index_from: str, hall_index_to: str) -> List[Dict]:
        node1 = self.hall_to_node[hall_index_from]
        node2 = self.hall_to_node[hall_index_to]

        # bfs
        nodes = [node1]
        nodes_visited = {node1}
        prev_node = {}  # map (node) -> (node before that node)
        while len(nodes) > 0:
            nodes_new = []
            for node in nodes:
                if node == node2:
                    path = [node2]
                    while path[-1] != node1:
                        path.append(prev_node[path[-1]])
                    path.reverse()
                    return self.beautify_path(path)
                for node_new in self.edges[node]:
                    if node_new not in nodes_visited:
                        nodes_visited.add(node_new)
                        nodes_new.append(node_new)
                        prev_node[node_new] = node
            nodes.clear()
            nodes, nodes_new = nodes_new, nodes
        assert False

    # заменяет node на hall/stairs
    def beautify_path(self, path):
        path = [self.nodes[node].copy() for node in path]
        for node_prev, node, node_next in zip(path[:-2], path[1:-1], path[2:]):
            if node['type'] == 'stairs':
                assert node_prev['type'] == 'hall' == node_next['type']
                floor_prev = node_prev['floor']
                floor_next = node_next['floor']
                floor_difference = floor_next - floor_prev
                assert abs(floor_difference) == 1
                node['direction'] = 'up' if floor_difference == 1 else 'down'
                del node['index']
        return path


with open('halls_edges.json') as f:
    buildings_infos = json.load(f)
    buildings = {}
    for building_info in buildings_infos:
        building = Building(building_info)
        building_id = building_info['building']
        buildings[building_id] = building


def stress_test():
    halls_main = (set(str(i) for i in range(1, 30 + 1)) - {'12', '13'}) | {'16a'}
    halls_gallery = set(str(i) for i in range(8, 26 + 1))
    for building_key, building_halls in [('main', halls_main), ('gallery', halls_gallery)]:
        for hall1 in building_halls:
            for hall2 in building_halls:
                if hall1 == hall2: continue
                find_path(building_key, hall1, hall2)


if __name__ == '__main__':
    stress_test()

    # find_path('main', '28', '8')
    path = find_path('gallery', '13', '21')
    # path = find_path('gallery', '13', '13')
    print(*path, sep='\n')
