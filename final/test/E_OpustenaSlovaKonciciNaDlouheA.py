""" 
v tomto testu se hledají slova, která končí na á, ale nejsou k ničemu připojena (často jsem spadají příjmení)
"""

import opakovane_funkce

def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

    seznam = []
    bez = []
            
    all_lemmas1 = {lemma.lower() for lemma in all_lemmas}

    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma[-1] in "á":
            if lexeme.all_parents == [] and (len(lexeme.lemma) > 3 or lexeme.lemma[0].isupper()):
                rodic = ""
                dalsi = ""
                if lexeme.lemma.endswith("ová"): #and lexeme.lemma != "Nová":
                    if lexeme.lemma[0].isupper():
                        rodic = lexeme.lemma[:-3]
                        if rodic[-2] not in "aáeěiíoóuůúyý":
                            pomoc = rodic[:-1] + "e" + rodic[-1]
                            dalsi = pomoc
                    else:
                        rodic = lexeme.lemma[:-1] + "ý" 

                elif lexeme.lemma.endswith("ická"):
                    rodic = lexeme.lemma[:-2] + "e"
                else:
                    rodic = lexeme.lemma[:-1].lower()
                    rodic = rodic + "ý"

                if rodic in all_lemmas:
                    seznam.append((lexeme.lemma, rodic))
                elif dalsi in all_lemmas:
                    seznam.append((lexeme.lemma, dalsi))

                else:
                    if lexeme.lemma.endswith("ová"):
                        if rodic + "a" in all_lemmas:
                            seznam.append((lexeme.lemma, rodic + "a"))
                        else:
                            rodic = rodic.lower()
                            if rodic in all_lemmas1:
                                seznam.append((lexeme.lemma, rodic))
                            elif dalsi in all_lemmas1:
                                seznam.append((lexeme.lemma, dalsi))
                            else:
                                if lexeme.lemma.endswith("ová"):
                                    if rodic + "a" in all_lemmas1:
                                        seznam.append((lexeme.lemma, rodic + "a"))
                                    else:
                                        bez.append(lexeme.lemma)

    opakovane_funkce.vypis_dva_seznamy(seznam, bez,"E_OpustenaSlovaKonciciNaDlouheA.tsv", "opuštěná slova končící na 'á'", "chybí hrana")

