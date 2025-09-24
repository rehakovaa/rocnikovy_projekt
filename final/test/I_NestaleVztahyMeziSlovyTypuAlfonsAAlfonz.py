""" 
test se zaměřuje na slova, která se liší pouze v s/z, odpovídá to slovům jako Alfons a Alfonz a jak jsou tyto slova navzájem svázaná
podle jejich navázanosti se to dělí do čtyř kategorií
    - rodičem je slovo obsahující 'z'
    - rodičem je slovo bez 's'
    - jsou vzdáleně příbuzní (nejsou ihned nad sebou)
    - nejsou nijak svázáni
ve výstupu je nejdříve tabulka procentuální rozdělení těchto kategorií a poté jsou tyto kategorie seřazeny od nejčastější po nejméně častou
"""
import porovnani

def zmena_z(lemma):
    novotvary = []
    if "z" in lemma:
        for i in range(len(lemma)):
            if lemma[i] == "z":
                nove = lemma[:i] + "s" + lemma[i+1:]
                novotvary.append(nove)
    return novotvary

def main(lexicon):

    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

    vypisky = {"h" : "rodičem v tomto vztahu je slovo obsahující 'z' místo 's' ",
                "bez_h": "rodičem v tom vztahu je slovo obsahující 's' místo 'z'", 
                "vubec": "tato dvojice slov není nijak příbuzná", 
                "vzdalene": "tato dvojice slov je příbuzná, ale ne napřímo"}

    porovnani.analyzuj_vztahy(lexicon, all_lemmas, zmena_z,
                    "I_NestaleVztahyMeziSlovyTypuAlfonsAAlfonz.tsv", vypisky)
