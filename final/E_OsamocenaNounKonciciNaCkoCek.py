"""
test hledá podstatná jména, kterou jsou zdrobnělinami a k nim rodiče
pokud rodič není nalezen, zkontroluje se, zda slovo není v derinetu vnímáno jako unmotivated
"""

import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
adresar = os.getcwd()  # aktuální adresář
cesta_k_souboru = os.path.join(adresar, "./derinet-2-3.tsv")  #sestavení cesty
lexicon.load(cesta_k_souboru)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

def tvorba_moznych_variant(slovicko, all_lemmas, vzorkar, dite, pismeno):
    moznosti = []
    if vzorkar == 1:
        for i in "aeio":
            slovo = slovicko + i + pismeno

            if slovo in all_lemmas and slovo != dite:
                moznosti.append(slovo)

    elif vzorkar == 0:
        for i in "aeio":
            slovo = slovicko + i 

            if slovo in all_lemmas and slovo != dite:
                moznosti.append(slovo)
    
    else:
        for i in "aeio":
            slovo = slovicko + "k" + i 

            if slovo in all_lemmas and slovo != dite:
                moznosti.append(slovo)
    
    return opakovane_funkce.seradit_moznosti(moznosti)

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
                mezikrok = tvorba_moznych_variant(lexeme.lemma[:-4], all_lemmas, 0, lexeme.lemma, None)
                if mezikrok == []:
                    if len(lexeme.lemma) > 6:
                        mezikrok = tvorba_moznych_variant(lexeme.lemma[:-5], all_lemmas, 1, lexeme.lemma, lexeme.lemma[-5])
                        if mezikrok == []:
                            mezikrok = tvorba_moznych_variant(lexeme.lemma[:-4], all_lemmas, 2, lexeme.lemma, None)
                    
            if mezikrok != []:
                rodic = mezikrok[0]
            else:
                bez.append(lexeme)
            
        if rodic is not None:
            seznam.append((lexeme.lemma, rodic))

bez = opakovane_funkce.je_spravne_bez_rodice(bez)
opakovane_funkce.vypis_dva_seznamy(seznam, bez,"E_OsamocenaNounKonciciNaCkoCek.tsv", "opuštěná slova končící na 'čko' nebo 'ček'")