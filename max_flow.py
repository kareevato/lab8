import csv
from collections import deque, defaultdict


class MaxFlowCalculator:
    def __init__(self):
        self.graph = defaultdict(dict)
        self.ferms = []
        self.shops = []

    def read_csv(self, filename):
        with open(filename, newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.ferms = rows[0]
        self.shops = rows[1]

        for row in rows[2:]:
            if len(row) < 3:
                continue  
            u, v, capacity = row[0].strip(), row[1].strip(), int(row[2])
            self.graph[u][v] = self.graph[u].get(v, 0) + capacity
            self.graph[v].setdefault(u, 0)

    def bfs(self, residual, source, sink, parent):
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v, capacity in residual[u].items():
                if v not in visited and capacity > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def edmonds_karp(self):
        super_source = "SUPER_SOURCE"
        super_sink = "SUPER_SINK"

        for f in self.ferms:
            self.graph[super_source][f] = float("inf")
            self.graph[f].setdefault(super_source, 0)

        for s in self.shops:
            self.graph[s][super_sink] = float("inf")
            self.graph[super_sink].setdefault(s, 0)

        residual = defaultdict(dict)
        for u in self.graph:
            for v in self.graph[u]:
                residual[u][v] = self.graph[u][v]

        max_flow = 0
        parent = {}

        while self.bfs(residual, super_source, super_sink, parent := {}):
            path_flow = float("inf")
            s = super_sink
            while s != super_source:
                path_flow = min(path_flow, residual[parent[s]][s])
                s = parent[s]

            max_flow += path_flow
            v = super_sink
            while v != super_source:
                u = parent[v]
                residual[u][v] -= path_flow
                residual[v][u] += path_flow
                v = parent[v]

        return max_flow


if __name__ == "__main__":
    calculator = MaxFlowCalculator()
    calculator.read_csv("roads.csv")
    result = calculator.edmonds_karp()
    print(f"Максимальна кількість машин, які можуть бути доставлені: {result}")
