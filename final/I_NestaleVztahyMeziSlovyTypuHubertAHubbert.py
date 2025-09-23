""" 
test se zaměřuje na slova, která se liší pouze v tom, že chybí jedno písmeno, odpovídá to Hubbert a Hubert a jak jsou tyto slova navzájem svázaná
podle jejich navázanosti se to dělí do čtyř kategorií
    - rodičem je slovo obsahující zdvojené písmeno
    - rodičem je slovo obsahující pouze jedno písmeno
    - jsou vzdáleně příbuzní (nejsou ihned nad sebou)
    - nejsou nijak svázáni
ve výstupu je nejdříve tabulka procentuální rozdělení těchto kategorií a poté jsou tyto kategorie seřazeny od nejčastější po nejméně častou
"""

import derinet.lexicon as dlex
import os
import porovnani

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

# varianta 1: zdvojené písmeno
def kandidati_zdvojene(lemma):
    vysledky = []
    for i in range(len(lemma) - 1):
        if lemma[i] == lemma[i+1]:
            vysledky.append(lemma[:i] + lemma[i+1:])
    return vysledky

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

vypisky= {
    "h": "rodičem v tomto vztahu je slovo obsahující zdvojené písmeno",
    "bez_h": "rodičem v tomto vztahu je slovo bez zdvojeného písmene",
    "vubec": "tato dvojice slov není nijak příbuzná",
    "vzdalene": "tato dvojice slov je příbuzná, ale ne napřímo"
}# spuštění pro obě varianty

porovnani.analyzuj_vztahy(lexicon, all_lemmas, kandidati_zdvojene,

                "I_NestaleVztahyMeziSlovyTypuHubertAHubbert.tsv", vypisky)
