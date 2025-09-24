"""
test hledá slova, jejichž rodiče jsou delší a méně časté a vyhazuju ta slova, která končí na ismus a ika
ostatní slova mě zajímají
"""
import opakovane_funkce

def main(lexicon):
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

    sorted(seznam,  key=lambda x: x[2], reverse=True)
    seznam1 = []
    for i in seznam: 
        seznam1.append((i[0], i[1]))

    opakovane_funkce.vypis_jeden_seznam(seznam1, "W_KratsiDiteSpecialniPripady.tsv", "slova s delšími a méně častými rodiči", "přebývá hrana")
