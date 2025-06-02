class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.positions = {}  #rjecnik u kom je kljuc redni broj strane a vrijednost je lista pozicija na toj strani gdje se nalazi rijec

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, page_num, word, position_in_page) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            
        if page_num + 1 not in node.positions: #inicijalizacija rjecnika, ako se rijec nalazi vise puta na istoj strani samo ce se nova pozicija    
                                                #te rijeci dodati u listu pozicija koja odgovara toj strani
            node.positions[page_num + 1] = []
            
        node.is_end_of_word = True  #list nosi informaciju da je to kraj rijeci
        node.positions[page_num + 1].append(position_in_page)   #kad se dodje do kraja rijeci postavi se redni broj strane na kojoj se nalazi i pozicija
                                                                #na toj strani
       
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None   #bilo je []
            node = node.children[char]
        if node.is_end_of_word:  #kad dodje do kraja te rijeci vrati sve njene pozicije
            return node.positions
        else:
            return None
     
    
    # def search_autocomplete_recursive(self, node, word = ""):
    #     if not node.is_end_of_word:
    #         for child in node.children:
    #             self.postorder(child)
    #             word += child
    #     return word
        
    # def search_autocomplete(self, word):
    #     autocomplete_results = [] #sve rijeci za autocomplete
    #     node = self.root
    #     for char in word:
    #         if char not in node.children:
    #             return None
    #         node = node.children[char]
    #     if node.is_end_of_word == True:   #kad dodje do kraja upita uzima dalje cvorove dok ne dodje do kraja rijeci iz svakog cvora i to vraca
    #         for key,node in node.children.items():
    #             node = node.children[char]
    #             autocomplete_results.append(self.search_autocomplete_recursive(node))
    #     return autocomplete_results
                
                
    def search_autocomplete_recursive(self, node, prefix, results, limit):
        if node.is_end_of_word:
            results.append(prefix)
            if len(results) >= limit:
                return
        
        for char, child_node in node.children.items():
            if len(results) >= limit:
                break
            self.search_autocomplete_recursive(child_node, prefix + char, results, limit)
    
    def search_autocomplete(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return []
            node = node.children[char]
        
        autocomplete_results = []
        self.search_autocomplete_recursive(node, word, autocomplete_results, 4)  # vraca samo 4 rezultata
        return autocomplete_results
            
        
    # def starts_with(self, prefix: str) -> bool:
    #     node = self.root
    #     for char in prefix:
    #         if char not in node.children:
    #             return False
    #         node = node.children[char]
    #     return True
