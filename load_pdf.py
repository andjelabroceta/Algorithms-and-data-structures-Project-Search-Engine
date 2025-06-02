import PyPDF2
import pickle
#ekstraktuje pdf file u stranice  i vraca listu stranica
def extract_text_from_pdf(pdf_file: str):  #vraca niz stranica u tekstu tipa string
    with open(pdf_file, 'rb') as pdf:  #otvara ga u bajtovima
        reader = PyPDF2.PdfReader(pdf, strict = False)
        pdf_text = []
      
        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
            
        #return pdf_text
        with open('pdf_document.pickle', 'wb') as file:
            pickle.dump(pdf_text, file)
        