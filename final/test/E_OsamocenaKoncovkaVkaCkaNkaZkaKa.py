""" 
test míří na slova končící na 'ka' bez rodiče
kvůli tomu, že podobných slov je velké množství a ne všechny vznikly změnou podstatného jména mužského rodu a dodání dané koncovky,
test se soustředí hlavně na koncovky 'vka', 'čka', 'nka' a 'žka'
"""

import opakovane_funkce

def mozny_predek(predchudce, all_lemmas, lexicon):
    kand = None
    kand1 = None
    if predchudce in all_lemmas:
        kand = predchudce
    if predchudce[-1] not in "aáeěiíoóuůúyý":
        dalsi = opakovane_funkce.tvorba_novych_variant_kratke(predchudce, all_lemmas)
        if len(dalsi) > 1:
            kand1 = opakovane_funkce.nejlepsi(dalsi, lexicon)
        elif len(dalsi) == 1:
            kand1 = dalsi.pop()
    
    if kand is None and kand1 is None:
        return None
    elif kand is not None and kand1 is None:
        return kand
    elif kand is None and kand1 is not None:
        return kand1
    else:
        celek = lexicon.get_lexemes(kand1)[0]
        navrat = opakovane_funkce.kontrola_rodice(kand, celek, lexicon)
        if navrat:
            return kand
        else:
            return kand1
        
def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    seznam = []
    bez = []

    for lexeme in lexicon.iter_lexemes():
        if lexeme.pos == "NOUN" and lexeme.lemma.endswith("ka"):
            if 'unmotivated' in lexeme.misc.keys() and lexeme.misc['unmotivated']:
                continue
            elif lexeme.all_parents == []:
                if 'Gender' in lexeme.feats and lexeme.feats['Gender'] == 'Fem':
                    predchudce = lexeme.lemma[:-2]
                    hotovo = False
                    #veci jako profesorka a profesor
                    #ale ne veci jako matka a mat
                    if predchudce in all_lemmas:
                        slovo = lexicon.get_lexemes(predchudce)[0]
                        casto_pred = slovo.misc['corpus_stats']['absolute_count']
                        casto_po = lexeme.misc['corpus_stats']['absolute_count']

                        if casto_po < casto_pred:
                            hotovo = True
                            seznam.append((lexeme.lemma, slovo.lemma))
                    
                    if not hotovo:

                        if lexeme.lemma.endswith(("vka", "čka", "nka")):
                            predchudce = lexeme.lemma[:-2]
                            vysledek = mozny_predek(predchudce, all_lemmas, lexicon)
                            if vysledek is not None:
                                seznam.append((lexeme.lemma, vysledek))
                                hotovo = True
                        
                            if not hotovo:
                                bez.append(lexeme)
                        

                        #pedagožka a pedagog
                        elif lexeme.lemma.endswith("žka"):
                            predchudce = predchudce + "g"

                            if predchudce in all_lemmas:
                                seznam.append((lexeme.lemma, predchudce))
                            else:
                                bez.append(lexeme)
                            
                        else: #teď pořešit skandinavistka a skandinavista
                            vysledek = mozny_predek(predchudce, all_lemmas, lexicon)
                            if vysledek is not None:
                                seznam.append((lexeme.lemma, vysledek))
                            else:
                                bez.append(lexeme)

    bez = opakovane_funkce.je_spravne_bez_rodice(bez)

    opakovane_funkce.vypis_dva_seznamy(seznam, bez,"E_OsamocenaKoncovkaVkaCkaNkaZkaKa.tsv", "opuštěná slova končící na 'vka', 'čka', 'nka', 'žka', 'ka'", "chybí hrana")
