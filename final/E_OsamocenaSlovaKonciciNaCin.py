""" 
test se věnuje přídavným jménům přivlastňovacím, které končí na 'čin'
jelikož je to dobře popsatelná skupina, v testu se kontroluje několik možností 
    - slovo má předchůdce, ale to podstatné jméno není rodu ženského
    - slovo nemá předchůdce, který by odpovídal vzoru (matčin -> matka)
        - existuje takové slovo a je rodu ženského
        - existuje takové slovo, ale není rodu ženského
        - takové slovo neexistuje 
"""
import derinet.lexicon as dlex
import os

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

def tisk_koncovky(spatny_rod, dobry_rod, spatny_nepripojeno, bez, rod, koncovka, soubor, vzdalene):
    with open(f"{soubor}.txt", "w", encoding="utf-8") as f:
        f.write(f"PŘÍDAVNÁ JMÉNA KONČÍCÍ NA -{koncovka}, KTERÁ NEJSOU PŘIPOJENA KE SLOVU {rod} RODU \n")
        f.write(f"{'PŘÍDAVNÉ JMÉNO'.ljust(20)}{'PODSTATNÉ JMÉNO'.ljust(20)}\n")
        f.write("\n")
        f.write(f"JE PŘIPOJENO KE SLOVU, KTERÉ NENÍ {rod} RODU\n")
        for i in spatny_rod:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")
        f.write("\n")
        f.write("JSOU VZDÁLENĚ PŘÍBUZNÍ\n")
        f.write(f"{'VZDÁLENÝ SYN'.ljust(20)}{'VZDÁLENÝ PŘEDEK'.ljust(20)}\n")
        for i in vzdalene:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")
        f.write("\n")
        f.write(f"NENÍ PŘIPOJENO K PŘEDKOVI, KTERÝ JE {rod} RODU \n")
        for i in dobry_rod:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")
        f.write(f"EXISTUJE NEPŘIPOJENÝ PŘEDEK, KTERÝ NENÍ {rod} RODU\n")
        for i in spatny_nepripojeno:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")
        f.write("NEBYL NALEZEN PŘEDEK \n")
        for i in bez:
            f.write(f"{i} \n")

def vzdalene_pribuzny(dite, rodic):
    daleko = False
    if dite.all_parents != []:
        for i in dite.all_parents:
            if lezeme_nahoru(i, rodic):
                daleko = True
    if daleko:
        return True
    return False

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


spatny_rod, dobry_rod, spatny_nepripojeno, bez = [], [], [], []#špatný rod - předek není ženský 
#dobrý rod - není připojen, ale je ženský, spatny_nepripojeno - nepřipojený předek a ještě není ženský
# bez - bez predka
vzdalene = [] #pokud nejsou hned nad sebou, ale vzdaleně příbuzní

for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma.endswith("čin") and lexeme.pos == "ADJ":
        #tady je to dobře, protože to má být hned nad dítětem
        rodice = lexeme.all_parents
        jeden = False # jestli jsme našli nějakou předkyni
        jiny = False # pokud jsme ale nasli predka, co neni zensky, ale sedí do popisu
        slovo = None
        for r in rodice:
            if r.lemma[:-2] == lexeme.lemma[:-3]:
                jiny = True 
                if r.pos == "NOUN" and r.feats["Gender"] == "Fem":
                    jeden = True
                else: 
                    slovo = r.lemma

        if not jeden and jiny: #máme rodiče, ale není to ženský rod
            spatny_rod.append((lexeme.lemma, slovo))

        elif not jeden and not jiny:
            rodic = lexeme.lemma[:-3] + "ka"
            if rodic in all_lemmas:
                predek = lexicon.get_lexemes(rodic)[0]
                if vzdalene_pribuzny(lexeme, predek):
                    vzdalene.append((lexeme.lemma, predek.lemma))
                elif vzdalene_pribuzny(predek, lexeme):
                    vzdalene.append((predek.lemma, lexeme.lemma))
                elif predek.pos == "NOUN" and predek.feats["Gender"] == "Fem":
                    dobry_rod.append((lexeme.lemma, predek.lemma))
                else:
                    spatny_nepripojeno.append((lexeme.lemma, predek.lemma))
            else:
                bez.append(lexeme.lemma)
            
tisk_koncovky(spatny_rod, dobry_rod, spatny_nepripojeno, bez, "ŽENSKÉHO", "ČIN", "E_OsamocenaSlovaKonciciNaCin", vzdalene)
                    




