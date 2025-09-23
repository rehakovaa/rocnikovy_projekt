"""
test hledá osamocená slova končící na ař, a pokud jsou i po hledání rodičů bez rodičů, zkontroluje se, jestli
je derinet nebere jako unmotivated
"""

import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
adresar = os.getcwd()  # aktuální adresář
cesta_k_souboru = os.path.join(adresar, "./derinet-2-3.tsv")  #sestavení cesty
lexicon.load(cesta_k_souboru)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

seznam_dobry = []
seznam_spatny = []
bez = []

for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma.endswith("ař") and lexeme.pos == "NOUN" and lexeme.all_parents == []:

        #běžka -> běžkař
        if lexeme.lemma[:-1] in all_lemmas: 
            rodic = lexeme.lemma[:-1]
            seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny)

        #Hrobař -> hrob
        elif lexeme.lemma[0].isupper() and lexeme.lemma[:-1].lower() in all_lemmas:
            rodic = lexeme.lemma[:-1].lower()
            seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny)

        #vrchař -> vrch
        elif lexeme.lemma[:-2] in all_lemmas:
            rodic = lexeme.lemma[:-2]
            seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny)
        elif lexeme.lemma[:-2].lower() in all_lemmas: 
            rodic = lexeme.lemma[:-2].lower()
            seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny)
        
        else: 
            hotovo = False 
            #vzorkař -> vzorek
            if not (lexeme.lemma[-3] in "aeiouyáéíóúůý") and not (lexeme.lemma[-4] in "aeiouyáéíóúůý"):
                rodic = lexeme.lemma[:-3]
                moznosti = opakovane_funkce.tvorba_moznych_variant(rodic, all_lemmas, True, lexeme.lemma)
                if moznosti != []:
                    seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(moznosti[0], lexeme, seznam_dobry, seznam_spatny)
                    hotovo = True

            #zmijař -> zmije
            if lexeme.lemma[0].islower() and not hotovo:
                rodic = lexeme.lemma[:-2]
                moznosti = opakovane_funkce.tvorba_moznych_variant(rodic, all_lemmas, False, lexeme.lemma)
                if moznosti != []:
                    seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(moznosti[0], lexeme, seznam_dobry, seznam_spatny)
                else: 
                    bez.append(lexeme)
            #Zmijař -> zmije
            elif lexeme.lemma[0].isupper() and not hotovo: 
                rodic = lexeme.lemma[:-2].lower()
                moznosti = opakovane_funkce.tvorba_moznych_variant(rodic, all_lemmas, False, lexeme.lemma)
                if moznosti != []:
                    seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(moznosti[0], lexeme, seznam_dobry, seznam_spatny)
                else: 
                    bez.append(lexeme)

bez = opakovane_funkce.je_spravne_bez_rodice(bez)
opakovane_funkce.vypis_tri_seznamy(seznam_dobry, seznam_spatny, bez,"E_OsamocenaNounKonciciNaAr.tsv", "opuštěná slova končící na 'ař'")

 
