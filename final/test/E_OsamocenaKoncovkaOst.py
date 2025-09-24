""" 
tento test hledá podstatná jména končící na 'ost', která nemají rodiče. jelikož tento test míří na podstatná jména, která vznikla od přídavného jména, je dodáno omezení
že takovéto slova musí být delší než čtyři písmena (aby se předešlo slovům jako je most)
"""
import opakovane_funkce

def hledani(slovo, all_lemmas):
    rodic = slovo + 'ý'
    dalsi = slovo + 'í'

    if rodic in all_lemmas:
        return rodic
    elif dalsi in all_lemmas:
        return dalsi
    else:
        return None
    
def main(lexicon):    
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    seznam = []
    bez = []
    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma.endswith("ost") and lexeme.all_parents == []:
            if len(lexeme.lemma[:-3]) > 3:
            #nejdřív se podíváme, jestli má rodiče, pokud ne, tak je to problém 
                predchudce = lexeme.lemma[:-3]
                vysledek = hledani(predchudce, all_lemmas)

                if vysledek is not None:
                    seznam.append((lexeme.lemma, vysledek))
                else:
                    predchudce = lexeme.lemma[:-4]
                    vysledek = hledani(predchudce, all_lemmas)

                    if vysledek is not None: 
                        seznam.append((lexeme.lemma, vysledek))
                    else:
                        hodnota = lexeme.misc.get("corpus_stats", {}).get("absolute_count", 0)
                        bez.append((lexeme.lemma, hodnota))

    bez = sorted(bez, key=lambda x: x[1])
    bez1 = []
    for i in bez:
        bez1.append(i[0])
        
    opakovane_funkce.vypis_dva_seznamy(seznam,bez1,"E_OsamocenaKoncovkaOst.tsv", "opuštěná slova končící na 'ost'", "chybí hrana")



