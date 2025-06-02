import string
import re
from load_pdf import extract_text_from_pdf
from trie import Trie
from colorama import Fore, Style, init
from graph import Graph
from graph import Vertex
from page_rank import page_rank

init(autoreset=True)  # Inicijalizacija colorama sa automatskim resetovanjem boje

def highlight_text(text, words):
    # re.IGNORECASE za ignorisanje velikih/malih slova
    for word in words:
        text = re.sub(word, f"{Fore.BLUE}{word}{Style.RESET_ALL}", text, flags=re.IGNORECASE)
    return text

def clean_text(text):
    # Uklanjanje svih specijalnih znakova osim alfanumeričkih i prostora
    return re.sub(r'[^A-Za-z0-9 ]+', '', text)

def get_page(page_num, text):
    if page_num < 0 or page_num >= len(text):
        raise IndexError(f"page_num {page_num} is out of range for extracted_text with length {len(text)}")
    return clean_text(text[page_num].replace('\n', ' ').replace('\r', ''))

def get_links(page):
    link_pattern = re.compile(r'page (\d+)', re.IGNORECASE)
    matches = link_pattern.findall(page)
    links = []
    
    for match in matches:
        target_page = int(match) 
        links.append(target_page)
    
    return links  # [p1, p2,...] redni brojevi strana na koje upućuju linkovi

def search_multiple_words(trie, words):
    results = {}
    for word in words:
        positions = trie.search(word.lower())
        for page_num, pos_list in positions.items():
            if page_num not in results:
                results[page_num] = {}
            if word not in results[page_num]:
                results[page_num][word] = []
            results[page_num][word].extend(pos_list)
    return results

if __name__ == '__main__':
    condition = True
    while(condition):
        pattern = input("Unesite jednu ili vise rijeci odvojenih zarezom, za izlazak iz programa unesi x: ")
        if pattern == 'x':
            print("Izlazak iz programa")
            condition = False
            continue
        
        words = [word.strip() for word in pattern.split(',')]
        
        page_graph = Graph()
        trie = Trie()
        extracted_text = extract_text_from_pdf('data_structures_and_algorithms_in_python.pdf')
        
        # Dodavanje riječi iz dokumenta u trie i graf
        for page_num, page in enumerate(extracted_text):
            v = Vertex(page_num, page)                        
            page_graph.insert_vertex(v)  # Dodaj stranicu kao čvor u graf
            links = get_links(page)
            page_graph.set_links(v, links)
            
            num_of_characters = 0  # Broj karaktera na svakoj strani za određivanje tačne pozicije svake riječi
            page = clean_text(page.replace('\n', ' ').replace('\r', ''))
            page = page.translate(str.maketrans('', '', string.punctuation))  # Uklanjanje interpunkcije
            words_in_page = page.lower().split()  # Sve riječi pretvorene u mala slova i splitovane po razmacima
            for word in words_in_page:
                trie.insert(page_num, word, num_of_characters)
                num_of_characters += len(word) + 1  # Sabiranje karaktera na strani za određivanje pozicije svake riječi
            num_of_characters = 0  # Resetovanje brojača za sljedeću stranicu

        # Pretraga riječi u trie
        results = search_multiple_words(trie, words)
        
        # Izračunavanje PageRank vrijednosti
        pr_values = page_rank(page_graph)  # Svaka strana ima svoj PageRank score

        # Rangiranje stranica prema PageRank-u i broju pojavljivanja riječi
        ranked_pages = sorted(results.keys(), key=lambda x: (
            -sum(len(results[x][word]) for word in results[x]),  # Veći broj pojavljivanja ima prioritet
            -len(results[x]),  # Više različitih riječi ima prioritet
            pr_values.get(page_graph.get_vertex_from_page_num(x), 0)  # PageRank kao dodatni kriterij, default na 0 ako vertex nije nađen
        ), reverse=True)
        
        # Ispis rezultata
        for page_num in ranked_pages:
            print(f"{Fore.YELLOW}BROJ STRANE {page_num + 1}{Style.RESET_ALL}")
            try:
                page = get_page(page_num, extracted_text)  # Pribavljanje teksta strane
            except IndexError as e:
                print(e)
                continue
            
            for word in results[page_num]:
                positions_list = results[page_num][word]
                for pos in positions_list:
                    snippet_length = 80  # Ukupna veličina isječka
                    start_pos = max(0, pos - snippet_length // 2)  # Osigurava da pozicija ne bude negativna
                    end_pos = min(len(page), pos + snippet_length // 2 + len(word))
                    
                    # Adjust start_pos if end_pos is near the end of the page
                    if end_pos == len(page):
                        start_pos = max(0, end_pos - snippet_length - len(word))
                    snippet_text = page[start_pos:end_pos]
                    highlighted_snippet = highlight_text(snippet_text, words)
                    print(highlighted_snippet + "...")


# def get_links(page): #vraca ekstraktovane linkove ka spoljnim stranama za svaku stranu da bi se od tih linkova formirale grane
#         link_pattern = re.compile(r'page (\d+)', re.IGNORECASE)
#         matches = link_pattern.findall(page)
#         print(matches)
#         links = []
        
#         for match in matches:
#                 target_page = int(match) - 1  # -1 zbog indeksa 0
#                 links.append(target_page)
        
#         return links


# if __name__ == '__main__':
#     page_text = """
#         This is some example text. See page 12 for more information.
#         On page 8, you will find further details.
#         """

#     links = get_links(page_text)
#     print(links)  # izlaz: [11, 7]
   