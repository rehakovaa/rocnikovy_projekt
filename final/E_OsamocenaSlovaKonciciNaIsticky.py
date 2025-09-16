""" 
test hledá slova končící na 'istický', která jsou bez rodiče a snaží se ho dohledat

"""

import derinet.lexicon as dlex
import os

def tisk(vysledek, neexistuje):
    with open("E_OsamocenaSlovaKonciciNaIsticky.txt", "w", encoding="utf-8") as f:
        f.write("PŘÍDAVNÁ JMÉNA KONČÍCÍ NA -ISTICKÝ, KTERÁ NEJSOU K NIČEMU PŘIPOJENA \n")
        f.write("PŘÍDAVNÉ JMÉNO A K ČEMU BY TO MĚLO BÝT PŘIPOJENO\n")
        f.write(f"{'PŘÍDAVJNÉ JMÉNO'.ljust(30)}{'PODSTATNÉ JMÉNO'.ljust(30)}\n")
        f.write("\n")

        for i in vysledek:
            f.write(f"{i[0].ljust(30)}{i[1].ljust(30)}\n")     

        f.write("\n")
        f.write("PŘÍDAVNÉ JMÉNO, K NIMŽ NEBYL NALEZEN PŘEDEK\n")
        f.write(f"PŘÍDAVNÉ JMÉNO \n")
        for i in neexistuje:
            f.write(f"{i} \n")


lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)


vysledek = []
neexistuje = []
all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma.endswith("istický") and lexeme.parent is None:
       for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma.endswith("istický") and lexeme.parent is None:
        if not lexeme.lemma.endswith("statistický") and not lexeme.lemma.startswith("proti"):
            nove = lexeme.lemma[:-6]
            nove = nove + "smus"
        elif lexeme.lemma.startswith("proti"):
            nove = lexeme.lemma[:-6][5:]
            nove = nove + "smus"

        if nove in all_lemmas:
            vysledek.append((lexeme.lemma, nove))
        else:
            neexistuje.append(lexeme.lemma)

tisk(vysledek, neexistuje)


