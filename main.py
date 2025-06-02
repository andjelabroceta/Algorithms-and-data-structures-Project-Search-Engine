import string
import re
from load_pdf import extract_text_from_pdf
from trie import Trie
from colorama import Fore, Style, init
from graph import Graph
from graph import Vertex
from page_rank import page_rank
import pickle
from fpdf import FPDF  #za konvertovanje teksta u PDF

init(autoreset=True)  # Inicijalizacija colorama sa automatskim resetovanjem boje

def highlight_text(text, pattern):
        if '"' in pattern:
                pattern_splited = pattern.split('"')[1]
                words = pattern_splited.split(" ")  
        elif " AND " in pattern:
                words = pattern.split(" AND ")
        elif " OR " in pattern:
                words = pattern.split(" OR ")
        elif " NOT " in pattern:
                words = pattern.split(" NOT ")
        else:
                words = pattern.split(",")
        # Kreiranje regularnog izraza koji traži bilo koju od riječi
        regex_pattern = r'(' + '|'.join(re.escape(word.strip()) for word in words) + r')'
        highlighted = re.sub(regex_pattern, lambda match: f"{Fore.BLUE}{match.group(0)}{Style.RESET_ALL}", text, flags=re.IGNORECASE)
    
        return highlighted

def clean_text(text):
    # Uklanjanje svih specijalnih znakova osim alfanumeričkih i prostora
    return re.sub(r'[^A-Za-z0-9 ]+', '', text)

def get_page(page_num, text):
        return clean_text(text[page_num].replace('\n', ' ').replace('\r', ''))

def get_links(page): #vraca ekstraktovane linkove ka spoljnim stranama za svaku stranu da bi se od tih linkova formirale grane
        link_pattern = re.compile(r'page (\d+)', re.IGNORECASE)
        matches = link_pattern.findall(page)
        links = []
        
        for match in matches:
                target_page = int(match) 
                links.append(target_page)
        
        return links  # [p1, p2,...] redni brojevi strana na koje upucuju linkovi

def is_before(word1, word2, text):  #provjerava da li se NOT nalazi ispred rijeci da bi tu rijec eliminisala iz pretrage
        for i, el in enumerate(text):
                if el == word2 and text[i-1] == word1:
                        return True
        return False

def search_phrase(text, phrase):
    phrase = phrase.lower()
    positions = []
    index = text.find(phrase)  #prvi indeks pronadjene fraze na stranici
    while index != -1: #dok god fraza postoji na strani
        positions.append(index)
        index = text.find(phrase, index + 1) #sledeca pozicija fraze
    return positions

       
if __name__ == '__main__':
        condition = True
        while(condition):
                pattern = input("Unesite jednu ili vise rijeci razdvojenih razmakom," + "\n" + 
                                "za izlazak iz programa unesi x, " + "\n" +
                                "za pretragu sa AND,OR ili NOT, unesi kljucne rijeci velikim slovom " + "\n" +
                                "za opciju autocomplete unesi * , " + "\n" +
                                "a ako zelis pretragu fraze navedi je pod navodnicima " + "\n")
                if pattern == 'x':
                        print("Izlazak iz programa")
                        condition = False
                        continue
                
                words = pattern.split(",")
                # page_graph = Graph()
                # trie = Trie()
                #serijalizacija ekstraktovanog fajla
                #extract_text_from_pdf('data_structures_and_algorithms_in_python.pdf')
                with open('graph.pickle', 'rb') as file:
                        page_graph: Graph = pickle.load(file)
                with open('trie.pickle', 'rb') as file1:
                        trie: Trie = pickle.load(file1)
                with open('pdf_document.pickle', 'rb') as file3:
                        extracted_text = pickle.load(file3)
                        
                
                #dodavanje rijeci iz dokumenta u trie
                for page_num, page in enumerate(extracted_text):#Funkcija enumerate uzima bilo koji iterabilni objekat (kao što je lista) i 
                                                #vraća iterabilni objekat koji generiše tuple. Svaki tuple sadrži par (indeks, vrijednost)
                         
                        v = Vertex(page_num, page)                        
                        page_graph.insert_vertex(v) #dodam stranicu kao cvor u grafu
                        #ekstraktovanje linkova sa stranica
                        links = get_links(page)
                        page_graph.set_links(v, links)
                        
                        
                        num_of_characters = 0 #broj karaktera na svakoj strani za odredjivanje tacne pozicije svake rijeci
                
                        page = clean_text(page.replace('\n', ' ').replace('\r', ''))
                        page = page.translate(str.maketrans('', '', string.punctuation))  # Uklanjanje interpunkcije
                        words_in_page = page.lower().split()  # Sve reči pretvorene u mala slova i splitovane po razmacima
                        for word in words_in_page:
                                trie.insert(page_num, word, num_of_characters)
                                num_of_characters += len(word) + 1 #koristi se za sabiranje karaktera na strani da bi se mogla odrediti pozicija svake rijeci na odredjenoj strani
                        num_of_characters = 0  # Resetovanje brojača za sledeću stranicu
                        
                #serijalizacija kreiranog grafa koriscenjem pickle modula
                # with open('graph.pickle','wb') as file:
                #         pickle.dump(page_graph, file)
                #serijalizacija kreiranog trie koriscenjem pickle modula
                # with open('trie.pickle', 'wb') as file1:
                #         pickle.dump(trie, file1)
                        

                #formiranje outcoming linkova
                # outcoming = page_graph.get_outgoing()
                # for strana, lista_linkova in outcoming.items():
                #         print("na strani " + str(strana.get_page_num() + 1))
                #         for link in lista_linkova:
                #                 print(str(link))
                # #formiranje incoming linkova
                # print("-----------------------------------------------")
                
                # incoming = page_graph.get_incoming()
                # for vertex, list in incoming.items():
                #         print(str(vertex.get_page_num()) + ":")
                #         for el in list:
                #                 print(str(el))
                                
                #positions = trie.search(pattern.lower())  # Pretraga uz obraćanje paznje na mala slova
                
                pr_values = page_rank(page_graph) #svaka strana ima svoj page rank score i na osnovu toga ce se prikazivati
              
                if "*" in pattern: #naglasavanje opcije za autocomplete
                        word = pattern[1:]
                        results = trie.search_autocomplete(word.lower())
                        print(f"{Fore.BLUE}Ponudjene rijeci su: {', '.join(results)}")
                
                if '"' in pattern: #naglasavanje opcije za fraze
                        combined_positions = {}
                        phrase = pattern.strip('"')
                        #print(phrase)
                        for page_num, page in enumerate(extracted_text):
                                page = clean_text(page.replace('\n', ' ').replace('\r', ''))
                                positions = search_phrase(page, phrase)
                                #print(positions)
                                if positions:
                                        combined_positions[page_num + 1] = positions
                                        # print(str(page_num ) + ": ")
                                        # for pos in positions:
                                        #         print(str(pos) + ",")
                elif " AND " in pattern:
                        positions_of_each_word = {}  # Ključ je riječ, a vrijednost je rječnik pozicija
                        words = pattern.split(" AND ")
                        
                        # Pretraži pozicije za svaku reč
                        for word in words:
                                word = word.strip()  # Ukloni razmake sa početka i kraja reči
                                positions = trie.search(word.lower())  # Pozicije svake reči
                                if positions:
                                        positions_of_each_word[word] = positions
                                else:
                                        print(f"Riječ '{word}' nije pronađena u dokumentu.")
                                        positions_of_each_word = {}  # Praznimo rečnik jer neka reč nije pronađena
                                        break
                        
                        if positions_of_each_word:
                                # Početni skup zajedničkih ključeva je skup ključeva prvog rečnika
                                common_keys = set(next(iter(positions_of_each_word.values())).keys())

                                # Iteriraj kroz ostale rečnike i ažuriraj skup zajedničkih ključeva
                                for positions in positions_of_each_word.values():
                                        common_keys.intersection_update(positions.keys())

                        else:
                                 break
                        combined_positions = {}  #postavi kljuceve(zajednicke strane) u rjecnik, value je None za svaki kljuc
                        for key in common_keys:
                                combined_positions[key] = [] 
                        for word in words:
                                positions = trie.search(word.lower())  #uzme pozicije svake rijeci
                                if positions != None: #ako rijec nije nadjena preskocice se
                                        for page_num, pos_list in positions.items():
                                                if page_num in combined_positions:
                                                        combined_positions[page_num].extend(pos_list)
                        list_for_removing_duplicates = []  #uklanjanje duplih vrijednosti iz rjecnika
                        for page,list in combined_positions.items():
                                for el in list:
                                        if el not in list_for_removing_duplicates:
                                                list_for_removing_duplicates.append(el)
                                combined_positions[page] = list_for_removing_duplicates
                                list_for_removing_duplicates = []
                        
                
                elif " NOT " in pattern:
                        words = pattern.split(" NOT ")
                        combined_positions = {}
                        for word in words:
                                positions = trie.search(word.lower())  #uzme pozicije svake rijeci
                                if positions != None: #ako rijec nije nadjena preskocice se
                                        for page_num, pos_list in positions.items():
                                                combined_positions[page_num] = (pos_list)
                        words = pattern.split(" ")
                        for word in words:
                                if is_before("NOT", word, words) == True:#za rijeci koje dolaze poslije NOT uklanjaju se strane na kojima se one prikazuju
                                        positions = trie.search(word.lower())
                                        for page_num, pos_list in positions.items():
                                                combined_positions.pop(page_num)
                                                
                        list_for_removing_duplicates = []  #uklanjanje duplih vrijednosti iz rjecnika
                        for page,list in combined_positions.items():
                                for el in list:
                                        if el not in list_for_removing_duplicates:
                                                list_for_removing_duplicates.append(el)
                                combined_positions[page] = list_for_removing_duplicates
                                list_for_removing_duplicates = []
                
                else:   
                        if " OR " in pattern:
                                words = pattern.split(" OR ")
                        else:
                                words = pattern.split(",")  
                        combined_positions = {}
                        for word in words:
                                positions = trie.search(word.lower())  #uzme pozicije svake rijeci
                                if positions != None: #ako rijec nije nadjena preskocice se
                                        for page_num, pos_list in positions.items():
                                                if page_num not in combined_positions:
                                                        combined_positions[page_num] = []
                                                combined_positions[page_num].extend(pos_list)  #rjecnik koji za kljuc ima br strane a za vr listu svih pozicija svake
                                                                                                #rijeci koja se pojavljuje na toj strani
                        list_for_removing_duplicates = []  #uklanjanje duplih vrijednosti iz rjecnika
                        for page,list in combined_positions.items():
                                for el in list:
                                        if el not in list_for_removing_duplicates:
                                                list_for_removing_duplicates.append(el)
                                combined_positions[page] = list_for_removing_duplicates
                                list_for_removing_duplicates = []
                
                #provjera page rank algoritma
                # for vertex, value in pr_values.items():
                #         print(" strana " + str(vertex.get_page_num()) + " value: " + str(value))
                #ranked_pages = sorted(positions.keys(), key=lambda x: pr_values[page_graph.get_vertex_from_page_num(x)], reverse=True)
                # ranked_pages = sorted(
                # (page_num for page_num in combined_positions.keys() if page_graph.get_vertex_from_page_num(page_num) is not None),
                # key=lambda x: (len(set(combined_positions[x])), pr_values[page_graph.get_vertex_from_page_num(x)]),
                # reverse=True
                # )
                ranked_pages_with_keys = []
                for page_num in combined_positions.keys():
                        vertex = page_graph.get_vertex_from_page_num(page_num)
                        if vertex is not None:                                                  #set omogucava da nema duplikata
                                unique_positions_count = len(set(combined_positions[page_num])) #broj pojavljivanja svih rijeci na svakoj strani
                                page_rank_value = pr_values.get(vertex, 0) #0 u slucaju da nije pronadjen
                                ranked_pages_with_keys.append((unique_positions_count, page_rank_value, page_num))

                        # sortiranje liste tuple-ova
                ranked_pages_with_keys.sort(key=lambda x: (x[0], x[1]), reverse=True)  #sortira se prvo prema  x[0] sto je broj pojavljivanja rijeci
                                                                                        # pa onda i po page_rank vrijednosti

                        # ekstrakcija brojeva stranica iz sortiranih tuple-ova
                ranked_pages = [x[2] for x in ranked_pages_with_keys]
                        
                #pretraga i ispis rezultata
                num_of_pages_for_pdf = 0  #prvih 10 rezultata se smjesta u pdf fajl
                result_num = 1
                num_of_pages_to_show = 20
                num_of_results_on_page = 10  #broj maks prikazanih rezultata pretrage na svakoj strani, korisnik moze prosiriti ako zeli
                ind = -1  #indikator da li je korisnik odabrao da zeli prikaz dodatnih strana
                ind2 = -1  #indikator da li je korisnik odabrao da zeli prikaz dodatnih rezultata na strani
                content_for_pdf = ""  #sadrzaj za pdf fajl
                for page_num in ranked_pages:
                        if num_of_pages_for_pdf == 10: #prvih 10 rezultata smjesta u pdf fajl
                                
                                #prvo se kreira text file
                                with open('first_10_results.txt', 'w') as file:
                                        file.write(content_for_pdf)
                                
                                
                                pdf = FPDF()
                                pdf.add_page()
                                pdf.set_font("Times", size = 10)
                               
                                with open("first_10_results.txt", "r") as fd:
                                        for i in fd:
                                                pdf.cell(200, 10, txt=i, ln=1, align='C')
        
                                pdf.output("first_10_results.pdf")
                                
                        if num_of_pages_to_show == 0:  #ogranicava ispis na prvih 20 strana
                                if ind == -1:
                                        choice = input(f"{Fore.RED}Da li zelis prikaz jos rezultata? Unesi da ili ne.{Style.RESET_ALL}")
                                        if choice == "da":
                                                ind = 0    #nece vise ulaziti u ovo pitanje
                                                continue
                                        elif choice == "ne":
                                                break
                                        else:
                                                print(f"{Fore.RED}Nedozvoljen unos{Style.RESET_ALL}")
                                                break
                        print(f"{Fore.GREEN}BROJ REZULTATA:{result_num}, {Fore.YELLOW}BROJ STRANE {page_num}{Style.RESET_ALL}")
                        page = get_page(page_num-1, extracted_text)  # Pribavljanje teksta strane
                        #positions_list = positions[page_num]
                        positions_list = combined_positions[page_num]
                        for pos in positions_list:
                                if num_of_results_on_page <= 0:
                                        if ind2 == -1:
                                                choice = input(f"{Fore.RED}Da li zelis da prikazes jos rezultata na ovoj strani? Unesi da ili ne.{Style.RESET_ALL}")
                                                if choice == "da":
                                                        ind2 = 0
                                                        continue
                                                elif choice == "ne":
                                                        break
                                                else:
                                                        print(f"{Fore.RED}Nedozvoljen unos{Style.RESET_ALL}")
                                                        break
                                        
                                snippet_length = 80  # Ukupna veličina isječka
                                start_pos = max(0, pos - snippet_length // 2)  # Osigurava da pozicija ne bude negativna
                                end_pos = min(len(page), pos + snippet_length // 2 + len(pattern)) #osigurava da pozicija ne bude veca od duzine strane
                                        
                                if end_pos == len(page):  #osigurava da ne predje na drugu stranu
                                        start_pos = max(0, end_pos - snippet_length - len(pattern))
                                snippet_text = page[start_pos:end_pos]
                                highlighted_snippet = highlight_text(snippet_text, pattern) #oznaci korisnikov unos unutar isjecka
                                print(highlighted_snippet + "...")
                                
                                if num_of_pages_for_pdf < 10:
                                        content_for_pdf += snippet_text + "..." +  "\n"
                                        
                                num_of_results_on_page -= 1
                                        
                        num_of_pages_to_show-= 1
                        result_num += 1
                        num_of_results_on_page = 10 #resetovanje za sledecu stranu
                        ind2 = -1
                        num_of_pages_for_pdf += 1

               