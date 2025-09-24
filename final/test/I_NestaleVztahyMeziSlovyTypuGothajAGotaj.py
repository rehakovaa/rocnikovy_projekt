""" 
test se zaměřuje na slova, která se liší pouze v 'h', odpovídá to gothaj a gotaj nebo ethiopský a etiopský, a jak jsou tyto slova navzájem svázaná
podle jejich navázanosti se to dělí do čtyř kategorií
    - rodičem je slovo obsahující 'h'
    - rodičem je slovo bez 'h'
    - jsou vzdáleně příbuzní (nejsou ihned nad sebou)
    - nejsou nijak svázáni
ve výstupu je nejdříve tabulka procentuální rozdělení těchto kategorií a poté jsou tyto kategorie seřazeny od nejčastější po nejméně častou
"""

import porovnani

def bez_h(lemma):
    indexiky = []
    for i in range(len(lemma)):
        if lemma[i] == "h":
            indexiky.append(i)

    novotvary = []
    for j in indexiky:
        novotvary.append(lemma[:j] + lemma[j+1:])
    return novotvary

def main(lexicon):       
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    vypisky = {"h" : "rodičem v tomto vztahu je slovo obsahující 'h' navíc",
                "bez_h":"rodičem v tom vztahu je slovo neobsahující zkoumané 'h'", 
                "vubec": "tato dvojice slov není nijak příbuzná", 
                "vzdalene": "tato dvojice slov je příbuzná, ale ne napřímo"}

    porovnani.analyzuj_vztahy(lexicon, all_lemmas, bez_h,
                    "I_NestaleVztahyMeziSlovyTypuGothajAGotaj.tsv", vypisky)
