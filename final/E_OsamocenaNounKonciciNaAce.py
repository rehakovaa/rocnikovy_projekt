"""
test hledá podstatná slova končící na 'ace' bez rodičů a hledá k nim možné rodiče
pokud rodič nebyl nalezen, ještě se zkontroluje, zda slovo není vnímáno jako unmotivated v derinetu
"""


import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
adresar = os.getcwd()  # aktuální adresář
cesta_k_souboru = os.path.join(adresar, "./derinet-2-3.tsv")  #sestavení cesty
lexicon.load(cesta_k_souboru)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

seznam = []
bez = []

for lexeme in lexicon.iter_lexemes():
    #berluskonizace
    if lexeme.pos == "NOUN" and lexeme.lemma.endswith("ace") and lexeme.all_parents == []:
        rodic = None
        if lexeme.lemma[:-3] + "ovat" in all_lemmas:
            rodic = lexeme.lemma[:-3] + "ovat"

        elif lexeme.lemma[7:] in all_lemmas and lexeme.lemma.startswith(("elektro")):
            rodic = lexeme.lemma[7:]
        elif lexeme.lemma[5:] in all_lemmas and lexeme.lemma.startswith(("video", "trans", "termo", "retro", "imuno", "hydro", "cyklo")):
            rodic = lexeme.lemma[5:]
        elif lexeme.lemma[4:] in all_lemmas and lexeme.lemma.startswith(("auto", "sebe", "troj", "poly", "foto", "dvoj")):
            rodic = lexeme.lemma[4:]
        elif lexeme.lemma[3:] in all_lemmas and lexeme.lemma.startswith("bio"):
            rodic = lexeme.lemma[3:]
        elif lexeme.lemma[2:] in all_lemmas and lexeme.lemma.startswith(("ex", "de")):
            rodic = lexeme.lemma[2:]
        else:
            bez.append(lexeme)

        if rodic is not None: 
            seznam.append((lexeme.lemma, rodic))
    
bez = opakovane_funkce.je_spravne_bez_rodice(bez)
opakovane_funkce.vypis_dva_seznamy(seznam, bez,"E_OsamocenaNounKonciciNaAce.tsv", "opuštěná slova končící na 'ace'")
         