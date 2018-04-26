from random import randrange


class Edge(object):
    def __init__(self, s, d):   
        self.source = s
        self.destination = d

    def __repr__(self):
        return 'u: {0}, v: {1}'.format(self.source, self.destination)

class Graph(object):
    def __init__(self, v, edges = None):
        self.Vertaxes = v
        self.Edges = edges

class Subset(object):
    def __init__(self, p, r):
        self.parent = p
        self.rank = r
    
    def __repr__(self):
        return 'Parent: {0}, Rank: {1}'.format(self.parent, self.rank)

class Karger(Graph):
    
    def __init__(self, v, edges=None):
        super(Karger, self).__init__(v, edges)
        self._subsets = dict()

    def _initialize_subset(self):
        for v in range(self.Vertaxes):
            self._subsets[v] = Subset(v, 0)

    def _find(self, i):
        if self._subsets[i].parent != i:
            self._subsets[i].parent = self._find(self._subsets[i].parent)
        return self._subsets[i].parent
    
    def _union(self, x, y):
        x_root = self._find(x)
        y_root = self._find(y)

        if self._subsets[x_root].rank < self._subsets[y_root].rank:
            self._subsets[x_root].parent = self._subsets[y_root].parent
        elif self._subsets[x_root].rank > self._subsets[y_root].rank:
            self._subsets[y_root].parent = self._subsets[x_root].parent
        else:
            self._subsets[y_root].parent = x_root
            self._subsets[x_root].rank += 1
    
    def _reduce_graph(self):
        v = self.Vertaxes
        e = len(self.Edges)
        while v > 2:
            i =  randrange(e)
            subset1 = self._find(self.Edges[i].source)   
            subset2 = self._find(self.Edges[i].destination)

            if subset1 == subset2:
                continue
            v -= 1
            # print ('Connecting edge {0} - {1}'.format(subset1, subset2))
            self._union(subset1, subset2)
    
    def find_mincut(self): 
        self._initialize_subset()
        self._reduce_graph()
        
        count = 0
        for i in range(len(self.Edges)):
            subset1 = self._find(self.Edges[i].source)
            subset2 = self._find(self.Edges[i].destination)

            if subset1 != subset2:
                count += 1
        return count

if __name__ == "__main__":
    n = int(input('Number of Nodes: ').strip())
    e = int(input('Number of edges: ').strip())
    # n = 4
    # edges = [Edge(0, 1), Edge(0, 2), Edge(0, 3), Edge(1, 3), Edge(2, 3)]
    edges = []
    for i in range(e):
        u,v = [int(x) for x in input('u - v: ').strip().split()]
        edges.append(Edge(u, v))
        # edges.append(Edge(v, u))

    karger = Karger(n, edges)

    print (karger.find_mincut(), karger._subsets)




        
