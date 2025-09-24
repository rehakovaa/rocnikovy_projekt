"""
test hledá podstatná jména, kterou jsou zdrobnělinami a k nim rodiče
pokud rodič není nalezen, zkontroluje se, zda slovo není v derinetu vnímáno jako unmotivated
"""

import opakovane_funkce

def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

    seznam = []
    bez = []

    for lexeme in lexicon.iter_lexemes():
        if lexeme.pos == "NOUN" and lexeme.lemma.endswith(("čko", "ček")) and lexeme.all_parents == [] and lexeme.lemma[0].islower():
            rodic = None
            if lexeme.lemma[:-3] in all_lemmas:
                rodic = lexeme.lemma[:-3]
            elif lexeme.lemma[:-4] in all_lemmas:
                rodic = lexeme.lemma[:-4]
            elif lexeme.lemma[:-3] + "k" in all_lemmas:
                rodic = lexeme.lemma[:-3] + "k"
            elif lexeme.lemma[:-2] in all_lemmas:
                rodic = lexeme.lemma[:-2]
            else:
                mezikrok = []
                if len(lexeme.lemma) > 5:
                    mezikrok = opakovane_funkce.tvorba_moznych_variant_tri(lexeme.lemma[:-4], all_lemmas, 0, lexeme.lemma, None, lexicon)
                    if mezikrok == []:
                        if len(lexeme.lemma) > 6:
                            mezikrok = opakovane_funkce.tvorba_moznych_variant_tri(lexeme.lemma[:-5], all_lemmas, 1, lexeme.lemma, lexeme.lemma[-5], lexicon)
                            if mezikrok == []:
                                mezikrok = opakovane_funkce.tvorba_moznych_variant_tri(lexeme.lemma[:-4], all_lemmas, 2, lexeme.lemma, None, lexicon)
                        
                if mezikrok != []:
                    rodic = mezikrok[0]
                else:
                    bez.append(lexeme)
                
            if rodic is not None:
                seznam.append((lexeme.lemma, rodic))

    bez = opakovane_funkce.je_spravne_bez_rodice(bez)
    opakovane_funkce.vypis_dva_seznamy(seznam, bez,"E_OsamocenaNounKonciciNaCkoCek.tsv", "opuštěná slova končící na 'čko' nebo 'ček'", "chybí hrana")
