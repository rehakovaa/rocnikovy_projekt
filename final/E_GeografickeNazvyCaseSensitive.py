""" 
test hledá slova, která jsou označeny v misc Geo a začínají velkým písmenem. poté kontroluje, jestli se v databázi nachází slovo, které je stejné, jen začíná malým písmenem
pokud k sobě nejsou připojena, tak to splňuje tento test

"""

import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
seznam = []

for lexeme in lexicon.iter_lexemes():
    if 'NameType' in lexeme.feats and lexeme.feats['NameType'] == 'Geo' and lexeme.lemma[0].isupper():
        tvar = lexeme.lemma.lower()
        if tvar in all_lemmas:
            slovo = lexicon.get_lexemes(tvar)[0]
            if lexeme not in slovo.all_parents and slovo not in lexeme.all_parents:
                seznam.append((lexeme.lemma, slovo.lemma))
                
opakovane_funkce.vypis_jeden_seznam(seznam, "E_GeografickeNazvyCaseSensitive.txt", 
                                    "geografické pojmy začínající velkým písmenem, které mají identické slovo v derinetu začínající malým písmenem a nejsou k sobě připojeni")







