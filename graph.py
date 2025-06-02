class Edge:
        def __init__(self, origin, destination, element):
            self._origin = origin
            self._destination = destination
            self._element = element

        def endpoints(self):
            return self._origin, self._destination

        def opposite(self, v):
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v mora biti instanca klase Vertex')
            if self._destination == v:
                return self._origin
            elif self._origin == v:
                return self._destination
            raise ValueError('v nije čvor ivice')

        def element(self):
            return self._element

        def __hash__(self):    
            return hash((self._origin, self._destination))

        def __str__(self):
            return '({0},{1},{2})'.format(self._origin,self._destination,self._element)


class Vertex:
        def __init__(self, page_num, page_content):  #cvor grafa je stranica
            self._page_num = page_num
            self._page_content = page_content

        def get_page_num(self):
            return self._page_num
        
        def get_page_content(self):
            return self._page_content
        
        

class Graph:
    def __init__(self, directed=False):
        self._outgoing = {} #kljuc je cvor a vrijednost je lista ulaznih grana
        self._incoming = {} #kljuc je cvor a vrijednost je lista izlaznih grana
        self.is_directed = directed
    
    def get_outgoing(self):
        return self._outgoing
    
    # def get_outgoing_for_particular_vertex(self, page_num):
    #     return self._outgoing[v.get_page_num()]  
    
    def set_links(self, v, list_of_outgoing):
        self._outgoing[v] = list_of_outgoing  # jednoj strani se dodjele svi izlazni linkovi na njoj
        for target in list_of_outgoing:  # istovremeno se ti izlazni linkovi postave za ulazne za svaku odgovarajucu stranicu
            target_vertex = self.get_vertex_from_page_num(target)
            if target_vertex not in self._incoming:
                self._incoming[target_vertex] = []
            self._incoming[target_vertex].append(v.get_page_num() + 1)
    
    def get_incoming(self):
        return self._incoming
    
    def get_vertex_from_page_num(self, page_num):    #vraca stranu sa odredjenim brojem strane
        for vertex in self._outgoing:
            if vertex.get_page_num() == page_num:
                return vertex
        return None
            
    # def set_incoming(self):
    #     if self._outgoing is not None:
    #         for vertex, list in self._outgoing.items():
    #             for link in list:
    #                 self._incoming[self.get_vertex_from_page_num(link)].append(vertex.get_page_num())
                
            
    
    def insert_vertex(self, v):
        self._outgoing[v] = []
        self._incoming[v] = []
