""" 
hledají se slova, která jsou příslovci, jejichž rodičem by měla být číslovka, ale v databázi žádného rodiče nemají 
pro zjednodušení vyhledávání se hledají pouze ty příslovce končící na 'é'
"""

import derinet.lexicon as dlex
import os
lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

prirazeni = {
    "osedm" : "sedm",
    "pátnáct" : "patnáct",
    "šedesátédevát" : "šedesátýdevátý",
    "tisícát": "tisíc",
}

def tisk(neexistuje, existuje_delsi):
    with open("E_OsamocenaCislovkovaPrislovce.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("ČÍSLOVKOVÁ PŘÍSLOVCE, KTERÁ NEJSOU K NIČEMU PŘIPOJENA")
        f.write("\n")
        f.write("EXISTUJE PŘÍDAVNÉ JMÉNO, KE KTERÉMU SE MOHOU PŘIPOJIT:\n")
        f.write(f"{'PŘÍSLOVCE'.ljust(20)}{'PŘÍDAVNÉ JMÉNO'.ljust(20)}\n")
        f.write("\n")
        for adv, adj in sorted(existuje_delsi):
            f.write(f"{adv.ljust(20)}{adj.ljust(20)}\n")
        
        f.write("\n")
        f.write("NEEXISTUJE JEDNO PŘÍDAVNÉ JMÉNO, KE KTERÉMU BY SE TO DALO PŘIPOJIT \n")
        for lemma, rodice in sorted(neexistuje):
            f.write(f"{lemma.ljust(20)}")
            if rodice:
                f.write("\n   možní rodiče: ")
                f.write(", ".join(rodice))
                f.write("\n")
            else:
                f.write(f"nezařazeno \n")

existuje_delsi = set()
neexistuje = []
all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

for lexeme in lexicon.iter_lexemes():
    if lexeme.pos == "ADV" and lexeme.parent is None and "unmotivated" not in lexeme.misc and lexeme.lemma.endswith("é"):
        #a teď mám několik verzí, co by to mohlo být 
        if lexeme.lemma.startswith("propo"):
            slovo = lexeme.lemma[3:]
        elif lexeme.lemma.startswith(("napo", "po", "za", "na")):
            slovo = lexeme.lemma[2:]
        else:
            slovo = lexeme.lemma

        if slovo[:-1] + "ý" in all_lemmas:
                existuje_delsi.add((lexeme.lemma, slovo[:-1] + "ý"))
        elif slovo in all_lemmas and slovo != lexeme.lemma:
             existuje_delsi.add((lexeme.lemma, slovo))
        else:
                if lexeme.lemma.startswith("propo"):
                    slovo = lexeme.lemma[5:]
                elif lexeme.lemma.startswith("napo"):
                    slovo = lexeme.lemma[4:]
                    
                kandidat = []
                volny = []
                for k in prirazeni.keys():
                    if slovo[:-1] == k:
                        kandidat.append(prirazeni[k])

                
                neexistuje.append((lexeme.lemma, kandidat))
                    
print(len(neexistuje), len(existuje_delsi))
tisk(neexistuje,existuje_delsi)



            
