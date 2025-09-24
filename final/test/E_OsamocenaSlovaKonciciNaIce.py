import opakovane_funkce

def main(lexicon):
    seznam = []
    bez = []
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma.endswith("ice") and lexeme.lemma[0].islower():
            if 'Gender' in lexeme.feats and lexeme.feats['Gender'] == 'Fem' and lexeme.all_parents == []: #and lexeme.lemma == "polyadice":
                if 'unmotivated' in lexeme.misc.keys() and lexeme.misc['unmotivated']:
                    continue
                else:

                    if lexeme.lemma[3:] in all_lemmas and lexeme.lemma.startswith(("tří", "bio")):
                        seznam.append((lexeme.lemma, lexeme.lemma[3:]))
                    elif lexeme.lemma[4:] in all_lemmas and lexeme.lemma.startswith(("mezi", "pěti", "čtyř", "troj", "dvoj", "dvou", "poly")):
                        seznam.append((lexeme.lemma, lexeme.lemma[4:]))
                    elif lexeme.lemma[5:] in all_lemmas and lexeme.lemma.startswith(("velko", "ultra", "čtvrt","video", "cyklo", "šesti", "rychlo")):
                        seznam.append((lexeme.lemma, lexeme.lemma[5:]))
                    elif lexeme.lemma[2:] in all_lemmas and lexeme.lemma.startswith(("re")):
                        seznam.append((lexeme.lemma, lexeme.lemma[2:]))
                    elif lexeme.lemma[:-6] in all_lemmas and lexeme.lemma.endswith(("ovnice")):
                        seznam.append((lexeme.lemma, lexeme.lemma[:-6]))
                    
                    else:
                        #tygřice -> tygr
                        if lexeme.lemma[:-3].endswith("ř"):
                            rodic = lexeme.lemma[:-3] + "r"
                            if rodic in all_lemmas:
                                seznam.append((lexeme.lemma, rodic))
                        
                        elif lexeme.lemma[:-4] + "t" in all_lemmas:
                            seznam.append((lexeme.lemma, lexeme.lemma[:-4] + "t"))

                        else:
                            kandidat = []
                            #šakalice -> šakal    
                            if lexeme.lemma[:-3] in all_lemmas:
                                kandidat.append(lexeme.lemma[:-3])

                            #dubovice -> dub    
                            if lexeme.lemma[:-5] in all_lemmas and len(lexeme.lemma) > 7:
                                kandidat.append(lexeme.lemma[:-5])

                            #jelenice -> jelen
                            if lexeme.lemma[:-4] in all_lemmas and len(lexeme.lemma) > 7:
                                kandidat.append(lexeme.lemma[:-4])

                            #řízkovnice -> řízek
                            if len(lexeme.lemma) > 8: 
                                neco = opakovane_funkce.tvorba_moznych_variant_tri(lexeme.lemma[:-7], all_lemmas, 1, lexeme.lemma, lexeme.lemma[-7], lexicon)
                                if neco != []:
                                    kandidat.append(neco[0])
                            
                            #zmetkovice -> zmetek
                            if len(lexeme.lemma) > 8: 
                                neco = opakovane_funkce.tvorba_moznych_variant_tri(lexeme.lemma[:-6], all_lemmas, 1, lexeme.lemma, lexeme.lemma[-6], lexicon)
                                if neco != []:
                                    kandidat.append(neco[0]) 
                        
                            #borůvkovice
                            if len(lexeme.lemma) > 8: 
                                neco = (opakovane_funkce.tvorba_moznych_variant_tri(lexeme.lemma[:-5], all_lemmas, 0, lexeme.lemma, lexeme.lemma[-7], lexicon))
                                if neco != []:
                                    kandidat.append(neco[0])

                            #tykvice -> tykev
                            if len(lexeme.lemma) > 5: 
                                neco = (opakovane_funkce.tvorba_moznych_variant_tri(lexeme.lemma[:-4], all_lemmas, 1, lexeme.lemma, lexeme.lemma[-4], lexicon))
                                if neco != []:
                                    kandidat.append(neco[0]) 

                            if len(lexeme.lemma) > 6:
                                neco =(opakovane_funkce.tvorba_moznych_variant(lexeme.lemma[:-3], all_lemmas, False, lexeme.lemma, lexicon))
                                if neco != []:
                                    kandidat.append(neco[0])

                            nej = opakovane_funkce.nejlepsi_noun(kandidat, lexicon)
                            
                            if nej is not None:
                                seznam.append((lexeme.lemma, nej))
                            else:
                                bez.append(lexeme)

    bez = opakovane_funkce.je_spravne_bez_rodice(bez)
    opakovane_funkce.vypis_dva_seznamy(seznam, bez, "E_OsamocenaSlovaKonciciNaIce.tsv", "slova rodu ženského končící na 'ice', která jsou bez rodiče", "chybí hrana")
