import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
adresar = os.getcwd()  # aktuální adresář
cesta_k_souboru = os.path.join(adresar, "./derinet-2-3.tsv")  #sestavení cesty
lexicon.load(cesta_k_souboru)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}


#je McAlister pod Alisterem??
seznam = []
for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma.startswith("Mc") and lexeme.all_parents == []:
        rodic = []
        if lexeme.lemma.endswith("ová") and lexeme.lemma[:-2] in all_lemmas:
            rodic = lexeme.lemma[:-2]
        if rodic == []:
            if lexeme.lemma[2:] in all_lemmas:
                rodic = lexeme.lemma[2:]
            elif lexeme.lemma[2:-3] in all_lemmas:
                rodic = lexeme.lemma[2:-3]

        if rodic != []:
            seznam.append((lexeme.lemma, rodic))

opakovane_funkce.vypis_jeden_seznam(seznam,"I_SlovaTypuMcAlisterBezRodicu.tsv", "slova začínající na 'Mc, která by mohla mít v derinetu rodiče") 
                    