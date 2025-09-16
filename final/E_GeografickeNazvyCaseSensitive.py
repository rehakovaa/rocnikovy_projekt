""" 
test hledá slova, která jsou označeny v misc Geo a začínají velkým písmenem. poté kontroluje, jestli se v databázi nachází slovo, které je stejné, jen začíná malým písmenem
pokud k sobě nejsou připojena, tak to splňuje tento test

"""

import derinet.lexicon as dlex
import os

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

#absurdistán by měl být odvozen od Absurdistánu?? nebo nějak naopak 
def tisk(seznam):
    with open("E_GeografickeNazvyCaseSensitive.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("GEOGRAFICKÉ POJMY, KTERÉ MAJÍ IDENTICKÉ SLOVO ZAČÍNAJÍCÍ MALÝM PÍSMENEM A NEJSOU K SOBĚ PŘIPOJENI \n")
        f.write(f"{'GEOGRAFICKÝ POJEM'.ljust(20)}{'ODVOZENÉ SLOVO'.ljust(20)}\n")
        f.write("\n")
        for i in seznam: 
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")

seznam = []

for lexeme in lexicon.iter_lexemes():
    if 'NameType' in lexeme.feats and lexeme.feats['NameType'] == 'Geo' and lexeme.lemma[0].isupper():
        tvar = lexeme.lemma.lower()
        if tvar in all_lemmas:
            slovo = lexicon.get_lexemes(tvar)[0]
            if lexeme not in slovo.all_parents and slovo not in lexeme.all_parents:
                seznam.append((lexeme.lemma, slovo.lemma))
                
tisk(seznam)



