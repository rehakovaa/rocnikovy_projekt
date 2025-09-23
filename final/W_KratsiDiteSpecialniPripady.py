"""
test hledá slova, jejichž rodiče jsou kratší a méně časté a vyhazuju ta slova, která končí na ismus a ika
ostatní slova mě zajímají
"""

import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

seznam = []
for lexeme in lexicon.iter_lexemes():
    for i in lexeme.all_parents:
        if len(i.lemma) > len(lexeme.lemma) + 2 and lexeme.pos == i.pos:
            casto_i = i.misc["corpus_stats"]["absolute_count"]
            casto_lemma = lexeme.misc["corpus_stats"]["absolute_count"]

            if casto_i < casto_lemma:
                if lexeme.lemma.endswith(("ismus", "izmus")) and opakovane_funkce.levenhstein(lexeme.lemma[:-5], i.lemma) < 2:
                    continue
                elif lexeme.lemma.endswith(("ika")) and opakovane_funkce.levenhstein(lexeme.lemma[:-3], i.lemma) < 2:
                    continue
                else:
                    seznam.append((lexeme.lemma, i.lemma, opakovane_funkce.levenhstein(lexeme.lemma, i.lemma)))

opakovane_funkce.vypis_jeden_seznam(sorted(seznam,  key=lambda x: x[2], reverse=True), "W_KratsiDiteSpecialniPripady.tsv", "slova s kratšími a méně častými rodiči")
