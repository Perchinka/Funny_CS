# Graph

# a -> b, c
# B a, d, e
# c -> a, f, g
# d -> b, e
# e -> b, d
# f -> c, g
# g -> c, f, h, i
# h -> g, i
# i -> g, h, x
# x -> i

from termcolor import colored

class Node:
    def __init__(self, name):
        self.name = name
        self.adjacent = []
        self.visited = False

class Graph:
    def __init__(self):
        self.nodes = {}

    def from_dict(self, graph_dict):
        for key in graph_dict:
            node = Node(key)
            self.addNode(node)
        for key in graph_dict:
            for n in graph_dict[key]:
                self.addEdge(self.nodes[key], self.nodes[n])

    def addNode(self, node):
        self.nodes[node.name] = node

    def addEdge(self, node1, node2):
        node1.adjacent.append(node2)

    def dfs(self, node):
        node.visited = True
        print(self)
        for n in node.adjacent:
            if not n.visited:
                self.dfs(n)

    def bfs(self, node):
        queue = []
        queue.append(node)
        node.visited = True
        while queue:
            node = queue.pop(0)
            print(self)
            for n in node.adjacent:
                if not n.visited:
                    n.visited = True
                    queue.append(n)

    def reset(self):
        for node in self.nodes.values():
            node.visited = False

    def __str__ (self):
        output = "Graph: \n"
        for node in self.nodes.values():
            output += colored(node.name, 'red') + ': ' if not node.visited else colored(node.name, 'green') + ': '
            for n in node.adjacent:
                output += colored(n.name, 'blue') + ', '
            output += '\n'
        return output


graph_dict = {
    'm': ['h', 'n'],
    'h': ['d', 'l', 'm'],
    'd': ['a', 'h'],
    'l': ['j', 'h'],
    'n': ['p', 'm'],
    'p': ['n', 'o', 't'],
    'o': ['p'],
    't': ['p'],
    'a': ['d'],
    'j': ['l']
}

graph = Graph()
graph.from_dict(graph_dict)


print(graph)

print(colored("\nDFS:", 'green'))
graph.dfs(graph.nodes['m'])

graph.reset()

print(colored("\nBFS:", 'green'))
graph.bfs(graph.nodes['m'])
