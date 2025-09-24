""" 
test hledá slovesa končící na 'řit' (běžkařit) bez rodiče
pokud rodič nebyl nalezen, zkontroluje se, zda slovo není unmotivated, pokud je, vyřadí se z testu
"""

import opakovane_funkce

def koncovky(lexeme, slovo, all_lemmas, lexicon): 
    seznamik_dobry = []
    seznamik_spatny = []
    if slovo[:-2] in all_lemmas: 
        rodic = slovo[:-2]
        seznamik_dobry, seznamik_spatny = opakovane_funkce.muze_se_pridat(rodic, lexeme, [], [], lexicon)
    elif slovo[:-3] in all_lemmas:
        rodic = slovo[:-3]
        seznamik_dobry, seznamik_spatny = opakovane_funkce.muze_se_pridat(rodic, lexeme, [], [], lexicon)

    zmena = not seznamik_dobry == [] or not seznamik_spatny == []
    
    return seznamik_dobry, seznamik_spatny, zmena

def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    seznam_dobry, seznam_spatny = [], []
    bez = []

    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma.endswith("řit") and lexeme.pos == "VERB" and lexeme.all_parents == []:
            hotovo = False
            pomocnik_dobry = []
            pomocnik_spatny = []
            pomocnik_dobry, pomocnik_spatny, hotovo = koncovky(lexeme, lexeme.lemma, all_lemmas, lexicon)

            if not hotovo:
                if lexeme.lemma[1:] in all_lemmas:
                    rodic = lexeme.lemma[1:]
                    pomocnik_dobry, pomocnik_spatny = opakovane_funkce.muze_se_pridat(rodic, lexeme, [], [], lexicon)
                    hotovo = True

                elif lexeme.lemma[2:] in all_lemmas:
                    rodic = lexeme.lemma[2:]
                    pomocnik_dobry, pomocnik_spatny = opakovane_funkce.muze_se_pridat(rodic, lexeme, [], [], lexicon)
                    hotovo = True
                
                if not hotovo:
                    slovo = lexeme.lemma[2:]
                    pomocnik_dobry, pomocnik_spatny, hotovo = koncovky(lexeme, slovo, all_lemmas, lexicon)

                if not hotovo:
                    slovo = lexeme.lemma[1:]
                    pomocnik_dobry, pomocnik_spatny, hotovo = koncovky(lexeme, slovo, all_lemmas, lexicon)
                
                if not hotovo:
                    if lexeme.lemma[:-4] in all_lemmas:
                        rodic = lexeme.lemma[:-4]
                        pomocnik_dobry, pomocnik_spatny = opakovane_funkce.muze_se_pridat(rodic, lexeme, [], [], lexicon)
                        hotovo = True

                if not hotovo:
                    bez.append(lexeme)

            seznam_dobry.extend(pomocnik_dobry)
            seznam_spatny.extend(pomocnik_spatny)

    bez = opakovane_funkce.je_spravne_bez_rodice(bez)
    opakovane_funkce.vypis_tri_seznamy(seznam_dobry, seznam_spatny, bez,"E_OsamocenaSlovesaKonciciNaRit.tsv", "osamocená slovesa končící na 'řit' (běžkařit)", "chybí hrana")
            #bezka -> bezkar -> bezkarit
