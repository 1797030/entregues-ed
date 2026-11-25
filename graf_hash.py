class GrafHash:

    def __init__(self, ln=None, lv=None, lp=None):
        self.hash_graf = {}
        self.nombre_arestes = 0
        self.nombre_nodes = 0
        if ln is not None:
            for vertex in ln:
                self.insert_vertex(vertex)
        if lv is not None:
            if lp is not None:
                for aresta, pes in zip(lv, lp):
                    self.insert_edge(aresta[0], aresta[1], pes)
            else:
                for aresta in lv:
                    self.insert_edge(aresta[0], aresta[1])

    def insert_vertex(self, x) -> None:
        if x not in self.hash_graf:
            self.hash_graf[x] = {}
            self.nombre_nodes +=1

    def insert_edge(self, n1, n2, p=1) -> None:
        if n1 in self.hash_graf and n2 in self.hash_graf:
            if not self.has_edge(n1, n2):
                self.hash_graf[n1][n2] = p
                self.hash_graf[n2][n1] = p
                self.nombre_arestes +=1

    def remove_edge(self, n1, n2) -> None:
        if self.has_edge(n1, n2):
            del self.hash_graf[n1][n2]
            del self.hash_graf[n2][n1]
            self.nombre_arestes -=1

    def remove_vertex(self, x) -> None:
        if x in self.hash_graf:
            for aresta in self.hash_graf[x].keys():
                del self.hash_graf[aresta][x]
                self.nombre_arestes -=1
            del self.hash_graf[x]
            self.nombre_nodes -=1
                
    def has_edge(self, n1, n2) -> bool:
        return n1 in self.hash_graf and n2 in self.hash_graf[n1]

    def weight(self, n1, n2):
        if self.has_edge(n1, n2):
            return self.hash_graf[n1][n2]
        else:
            return None

    def degree(self, x) -> int:
        return len(self.hash_graf[x])

    def num_vertices(self) -> int:
        return self.nombre_nodes

    def num_edges(self) -> int:
        return self.nombre_arestes
        
    def vertices(self):
        return self.hash_graf.keys()

    def edges(self, x):
        return self.hash_graf[x].keys()


