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

def vypis(neexistuje, existuje, bez):
    with open("E_OsamocenaCislovkovaPrislovce.tsv", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("*osamocená číslovková příslovce\n")
        f.write("*existuje jeden možný rodič\n")
        f.write(f"*zkoumané slovo\tnalezené slovo'\n")
        for i in sorted(existuje): 
            f.write(f"{i[0]}\t{i[1]}\n")
        f.write("*\n")
        f.write("*víc možných rodičů\n")
        for lemma, rodice in sorted(neexistuje):
            for i in rodice:
                f.write(f"{lemma}\t{i}\n")
        f.write("*\n")
        f.write("*nenalezen předek")
        for i in bez:
            f.write(f"{i[0]}\n")

existuje_delsi = set()
neexistuje = []
bez = []
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

                if kandidat != []:
                    neexistuje.append((lexeme.lemma, kandidat))
                else:
                    bez.append(lexeme.lemma)
                    
vypis(neexistuje,existuje_delsi, bez)


            

