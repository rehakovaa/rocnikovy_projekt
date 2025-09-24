""" 
test hledá přídavná jména končící na 'ův' a kontroluje několik vlastností: 
    - slovo má předchůdce odpovídající tvaru (srncův -> srnec anebo tesařův -> tesař anebo antinacistův -> antinacista), ale není mužského rodu
    - slovo nemá předchůdce odpovídající tomuto tvaru
        - existuje takové slovo
        - existuje takové slovo, ale není mužského rodu
        - neexistuje takové slovo

upozornění:
existují případy, kdy je antinacistův pod nacistův
"""

import opakovane_funkce

def tvorba_predka(slovo):
    temp = slovo[:-2]
    nove = temp[0:-1]
    nove2 = temp[-1]
    slovicko = nove + "e" + nove2
    slovo3 = temp + "a"
    return slovicko, slovo3
    

def hledani_predka(lexeme):
    rodice = lexeme.all_parents
    pomocnik = tvorba_predka(lexeme.lemma)
    jeden = False # jestli jsme našli nějakou předkyni
    jiny = False # pokud jsme ale nasli predka, co neni muzsky, ale sedí do popisu
    slovo = None
    for r in rodice:
        re = r.lemma
        if r.lemma[-1] in "aeiouyáéíóúůý" and r.lemma[-2] not in "aeiouyáéíóúůý":
            re = r.lemma[:-1]
        if re.endswith("os"):
            re = r.lemma[:-2]
        if r and (re == pomocnik or re == lexeme.lemma[:-2]):
            jiny = True 
            if r.pos == "NOUN" and "Gender" in r.feats.keys() and r.feats["Gender"] == "Masc":
                jeden = True
                break
            else: 
                slovo = r.lemma

    return jeden, jiny, slovo


def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    spatny_rod, dobry_rod, spatny_nepripojeno, bez = [], [], [], []#špatný rod - předek není ženský 
    #dobrý rod - není připojen, ale je ženský, spatny_nepripojeno - nepřipojený předek a ještě není ženský
    # bez - bez predka
    vzdalene = []
    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma.endswith("ův") and lexeme.pos == "ADJ": #and not test_samohlasek(lexeme.lemma[:-3]):
            #tady je to dobře, protože to má být hned nad dítětem
            #teď mám posichrováno, pokud je to tvaru 'aristokrat > aristokratův'
            jeden, jiny, slovo = hledani_predka(lexeme)
        
            if not jeden and jiny:
                spatny_rod.append((lexeme.lemma, slovo))
            elif not jeden and not jiny:

                pomocnik1, pomocnik2 = tvorba_predka(lexeme.lemma)
                lex = None
                if pomocnik1 in all_lemmas:
                    lex = lexicon.get_lexemes(pomocnik1)[0]
                elif pomocnik2 in all_lemmas:
                    lex = lexicon.get_lexemes(pomocnik2)[0]
                elif lexeme.lemma[:-2] in all_lemmas:
                    lex = lexicon.get_lexemes(lexeme.lemma[:-2])[0]

                if lex is not None: 
                    if opakovane_funkce.vzdalene_pribuzny(lexeme, lex):
                        vzdalene.append((lexeme.lemma, lex.lemma))
                    elif opakovane_funkce.vzdalene_pribuzny(lex, lexeme):
                        vzdalene.append((lexeme.lemma, lex.lemma))
                        
                    else:
                        if 'Gender' in lex.feats.keys() and lex.feats["Gender"] == "Masc":
                            dobry_rod.append((lexeme.lemma, lex.lemma))
                        else:
                            spatny_nepripojeno.append((lexeme.lemma, lex.lemma))
                else:
                    bez.append(lexeme.lemma)

    opakovane_funkce.vypis_matcin_otcuv(spatny_rod, dobry_rod, spatny_nepripojeno, bez, "mužského", "ův", "E_SlovaKonciciNaUv", vzdalene, "špatný rod rodiče", "chybí hrana")
