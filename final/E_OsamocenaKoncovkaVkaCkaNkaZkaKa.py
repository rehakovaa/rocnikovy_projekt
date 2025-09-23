""" 
test míří na slova končící na 'ka' bez rodiče
kvůli tomu, že podobných slov je velké množství a ne všechny vznikly změnou podstatného jména mužského rodu a dodání dané koncovky,
test se soustředí hlavně na koncovky 'vka', 'čka', 'nka' a 'žka'
"""
import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

def mozny_predek(predchudce):
    if predchudce in all_lemmas:
        return predchudce
    else:
        if predchudce[-1] not in "aáeěiíoóuůúyý":
            dalsi = opakovane_funkce.test(predchudce)
            if len(dalsi) > 1:
                return opakovane_funkce.nejlepsi(dalsi, lexicon)
            elif len(dalsi) == 1:
                return dalsi.pop()
            else:
                return None

seznam = []
bez = []

def hledani_predka(predek, dite):
    kandidati = {lemma for lemma in all_lemmas if predek in lemma and len(predek) < len(lemma) and lemma != dite and len(dite) > len(lemma)}
    vysledny = opakovane_funkce.nejlepsi(kandidati, lexicon)
    return vysledny

for lexeme in lexicon.iter_lexemes():
    if lexeme.pos == "NOUN" and lexeme.lemma.endswith("ka"):
        if lexeme.all_parents == []:
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
                        predchudce = lexeme.lemma[:-4]
                        vysledek = mozny_predek(predchudce)
                        if vysledek is not None:
                            seznam.append((lexeme.lemma, predchudce))
                            hotovo = True

                        else:
                            predchudce = lexeme.lemma[:-2]
                            vysledek = mozny_predek(predchudce)
                            if vysledek is not None:
                                seznam.append((lexeme.lemma, slovo.lemma))
                                hotovo = True
                        
                        if not hotovo:
                            predchudce = lexeme.lemma[:-4]
                            cil = hledani_predka(predchudce, lexeme.lemma)
                            if cil is not None:
                                seznam.append((lexeme.lemma, cil))
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
                        vysledek = mozny_predek(predchudce)
                        if vysledek is not None:
                            seznam.append((lexeme.lemma, predchudce))
                        else:
                            bez.append(lexeme)

bez = opakovane_funkce.je_spravne_bez_rodice(bez)

opakovane_funkce.vypis_dva_seznamy(seznam, bez,"E_OsamocenaKoncovkaVkaCkaNkaZkaKa.tsv", "opuštěná slova končící na 'vka', 'čka', 'nka', 'žka', 'ka'")
