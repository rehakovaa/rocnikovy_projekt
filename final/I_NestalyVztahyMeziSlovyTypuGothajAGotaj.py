""" 
test se zaměřuje na slova, která se liší pouze v 'h', odpovídá to gothaj a gotaj nebo ethiopský a etiopský, a jak jsou tyto slova navzájem svázaná
podle jejich navázanosti se to dělí do čtyř kategorií
    - rodičem je slovo obsahující 'h'
    - rodičem je slovo bez 'h'
    - jsou vzdáleně příbuzní (nejsou ihned nad sebou)
    - nejsou nijak svázáni
ve výstupu je nejdříve tabulka procentuální rozdělení těchto kategorií a poté jsou tyto kategorie seřazeny od nejčastější po nejméně častou
"""

import derinet.lexicon as dlex
import os


def vzdalene_pribuzni(dite, rodic):
    daleko = False
    if dite.all_parents != []:
        for i in dite.all_parents:
            if lezeme_nahoru(i, rodic):
                daleko = True
    if daleko:
        return True
    return False

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)


all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

def lezeme_nahoru(dite, hledany): #podívám se, jestli nejsou nějak propojené
    rodice = dite.all_parents
    if not rodice:
        return False  # nedošli jsme k hledanému
    if hledany in rodice:
        return True  # hledaný je přímo rodičem
    for r in rodice:
        if lezeme_nahoru(r, hledany):  # rekurzivně jdeme dál
            return True
    return False  # pokud jsme ho nikdy nenašli

#chci zjistit, jestli jsou ta slova k sobě nějak navázaná, i když ne napřimo
def jsou_pribuzni(bez_h, h):
    otec_h = lexicon.get_lexemes(h)[0]
    rodice_h = otec_h.all_parents
    otec_bez = lexicon.get_lexemes(bez_h)[0]
    rodice_bez_h = otec_bez.all_parents

    #jestli je gotaj otcem gothaje
    if any(parent.lemma == bez_h for parent in rodice_h):
        return 0
    #jestli je gothaj otcem gotaje
    elif any(parent.lemma == h for parent in rodice_bez_h):
        return 1
    else:
        #pokud to není ani jedno, tak se podíváme, jestli nejsou příbuzní oklikou
        #je gotaj nějak dítětem gothaje?
        etiopie = vzdalene_pribuzni(otec_bez, otec_h)
        #je gothaj nějak dítětem gotaje?
        gothaj = vzdalene_pribuzni(otec_h, otec_bez)

        if etiopie or gothaj:
            return 2
        else:
            return 3
        
def pomery(celkove, h, bez_h, vzdalene, vubec, dohromady):
    seznam = { "h": h/celkove*100, "bez_h" : bez_h/celkove*100, "vubec" : vubec/celkove*100,  "vzdalene" : vzdalene/celkove*100}
    vypis = {"h" : "rodičem v tomto vztahu je slovo obsahující 'h' navíc", "bez_h":"rodičem v tom vztahu je slovo neobsahující zkoumané 'h'", 
             "vubec": "tato dvojice slov není nijak příbuzná", "vzdalene": "tato dvojice slov je příbuzná, ale ne napřímo"}

    #chci nejdriv vypsat všechny četnosti a poté je vypsat jejich pořadí  
    with open("I_NestalyVztahyMeziSlovyTypuGothajAGotaj.txt", "w", encoding="utf-8") as f:
        f.write("S JAKOU ČETNOSTÍ SE V DERINETU NACHÁZÍ SPOJENÍ SLOV, KTERÉ SE LIŠÍ JEDNÍM H \n")
        f.write("TABULKA ČETNOSTÍ OD NEJČASTĚJŠÍHO VZTAHU DO NEJMÉNĚ ČASTÉHO: \n")
        sortovano = sorted(seznam.items(), key=lambda x: x[1], reverse=True)
        f.write(f"{'TYP VZTAHU'.ljust(70)}{'ČETNOST V PROCENTECH'.ljust(30)}\n")
        for k, v in sortovano:
            f.write(f"{vypis[k].ljust(70)}{str(v).ljust(30)} \n")

        for k, v in sortovano: #kdyz tam dodam with, tak se mi to samo zavre
            f.write("\n")
            f.write(f"{vypis[k].upper()} \n")
            if k == "h" or k == "bez_h":
                f.write(f"  {'OTEC'.ljust(30)}{'SYN'.ljust(30)}\n")
            seznamik = dohromady[k]
            for i in sorted(seznamik, key=lambda x: x[0]):
                f.write(f"      {i[0].ljust(30)}{i[1].ljust(30)}\n")

celkove = 0

#jestli je jeden z nich otcem druhého, jestli jsou nějak příbuzní a jestli nejsou vůbec příbuzní
h_ne, h_ano, vzdalene, vubec = 0, 0, 0, 0 
h_ne_seznam, h_ano_seznam, vzdalene_seznam, vubec_seznam = set(), set(), set(), set()

for lexeme in lexicon.iter_lexemes():
    if "h" in lexeme.lemma and not lexeme.lemma.startswith("-"):

        #poodstraňuju všechna h, která se v tom slově nachází
        indexiky = []
        for i in range(len(lexeme.lemma)):
            if lexeme.lemma[i] == "h":
                indexiky.append(i)

        novotvary = []
        for j in indexiky:
            novotvary.append(lexeme.lemma[:j] + lexeme.lemma[j+1:])

        for k in novotvary:
            if k in all_lemmas:
                #print(k)
                stav = jsou_pribuzni(k, lexeme.lemma)
                celkove += 1

                if stav == 0: #znamená to, že etiopský je rodičem ethiopský
                    h_ano += 1
                    h_ano_seznam.add((k, lexeme.lemma))
                elif stav == 1: #gothaj je rodičem gotaj
                    h_ne += 1 
                    #je to vždycky (rodič, syn)
                    h_ne_seznam.add((lexeme.lemma, k))
                elif stav == 2:
                    vzdalene += 1
                    vzdalene_seznam.add((lexeme.lemma, k))
                else:
                    vubec += 1
                    vubec_seznam.add((lexeme.lemma, k))

dohromady = {"h": h_ano_seznam, "bez_h" : h_ne_seznam, "vubec" : vubec_seznam,  "vzdalene" : vzdalene_seznam}
print(celkove, h_ano, h_ne, vzdalene, vubec)
pomery(celkove, h_ano, h_ne, vzdalene, vubec, dohromady)





