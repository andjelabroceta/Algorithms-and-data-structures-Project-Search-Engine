
def page_rank(graph, damping_factor=0.85, max_iterations=100, tolerance=1.0e-6): #tolerance je unaprijed definisana vrijednost koja određuje 
                        #koliko male promjene u PageRank vrijednostima su prihvatljive da bi se algoritam smatrao konvergentnim (stabilizovanim). 
   
    num_vertices = len(graph.get_outgoing())  #ukupan broj cvorova
    pr_values = {}  #rjecnik pocetnih page rank vrijednosti
    for vertex in graph.get_outgoing():     #dodjeljivanje pocetne vrijednosti svakom cvoru
        pr_values[vertex] = 1/num_vertices
    #pr_values = {vertex: 1 / num_vertices for vertex in graph.get_outgoing()}
    
    
    for i in range(max_iterations):
        new_pr_values = {}  # rječnik za nove page rank vrijednosti u svakoj novoj iteraciji
        for vertex in graph.get_outgoing():
            rank_sum = 0  # suma PageRank vrijednosti svih čvorova koji upućuju na trenutni čvor.
            for incoming_vertex in graph.get_incoming().get(vertex, []):  # pristupa svim čvorovima koji upućuju na taj čvor
                incoming_vertex_obj = graph.get_vertex_from_page_num(incoming_vertex)
                outgoing_links = graph.get_outgoing().get(incoming_vertex_obj, [])
                if not outgoing_links:
                    continue  # preskoči ovaj čvor ako nema izlaznih linkova
                rank_sum += pr_values[incoming_vertex_obj] / len(outgoing_links)
            new_pr_values[vertex] = (1 - damping_factor) / num_vertices + damping_factor * rank_sum
    # for i in range(max_iterations):
    #     new_pr_values = {}   #rjecnik za nove page rank vrijednosti u svakoj novoj iteraciji
    #     for vertex in graph.get_outgoing():
    #         rank_sum = 0  #suma PageRank vrijednosti svih čvorova koji upućuju na trenutni čvor.
    #         for incoming_vertex in graph.get_incoming().get(vertex, []):#pristupa svim cvorovima koji upucuju na taj cvor, [] je podrazumijevana
    #                                                                     #vrijednost ako taj cvor nema nijedan ulazni link nece izazivati gresku
    #             incoming_vertex = graph.get_vertex_from_page_num(incoming_vertex)
    #             if incoming_vertex not in pr_values:
    #                 print(f"incoming_vertex {incoming_vertex} not in pr_values")
    #                 continue  # preskoci ovaj cvor ako nije prisutan u pr_values
    #             rank_sum += pr_values[incoming_vertex] / len(graph.get_outgoing()[incoming_vertex]) #po formuli 
    #         new_pr_values[vertex] = (1 - damping_factor) / num_vertices + damping_factor * rank_sum
        
        # provjera da li je algoritam dovoljno stabilan da se petlja moze prekinuti
        diff = 0
        for vertex in new_pr_values:
            diff  += abs(new_pr_values[vertex] - pr_values[vertex])
            
        if diff < tolerance: #ako je ukupna promjena manja od zadate tolerancije, znaci da se algoritam stabilizovao dovoljno i da se moze prekinuti petlja
            break
        pr_values = new_pr_values #ako ne, nastavlja se
    
    return pr_values  #vraca rjecnik sa page rank vrijednostima za svaki cvor(stranicu)

