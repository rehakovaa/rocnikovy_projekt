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


def tisk_koncovky(spatny_rod, dobry_rod, spatny_nepripojeno, bez, rod, koncovka, soubor):
    with open(f"{soubor}.txt", "w", encoding="utf-8") as f:
        f.write(f"PŘÍDAVNÁ JMÉNA KONČÍCÍ NA -{koncovka}, KTERÁ NEJSOU PŘIPOJENA KE SLOVU {rod} RODU \n")
        f.write(f"{'PŘÍDAVNÉ JMÉNO'.ljust(20)}{'PODSTATNÉ JMÉNO'.ljust(20)}\n")
        f.write("\n")
        f.write(f"JE PŘIPOJENO KE SLOVU, KTERÉ NENÍ {rod} RODU\n")
        for i in spatny_rod:
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


lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)


spatny_rod, dobry_rod, spatny_nepripojeno, bez = [], [], [], []#špatný rod - předek není ženský 
#dobrý rod - není připojen, ale je ženský, spatny_nepripojeno - nepřipojený předek a ještě není ženský
# bez - bez predka
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
            volny = True
            for lex in lexicon.iter_lexemes():
                if lex.lemma[:-2] == lexeme.lemma[:-3] and lex.lemma != lexeme.lemma and lex.lemma.endswith("a"):
                    if lex.pos == "NOUN" and lex.feats["Gender"] == "Fem":
                        dobry_rod.append((lexeme.lemma, lex.lemma))
                    else:
                        spatny_nepripojeno.append((lexeme.lemma, lex.lemma))
                    volny = False
                    break
            if volny: 
                bez.append(lexeme.lemma)
             
tisk_koncovky(spatny_rod, dobry_rod, spatny_nepripojeno, bez, "ŽENSKÉHO", "ČIN", "E_OsamocenaSlovaKonciciNaCin")

                    
