""" 
test hledá jména začínající na 'Mc', která jsou k ničemu nepřipojena a pokud najdě nějakého rodiče, přidá ho na seznam
"""
import opakovane_funkce

def main(lexicon):
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
                elif lexeme.lemma[2:-3] in all_lemmas and lexeme.lemma.endswith("ová"):
                    rodic = lexeme.lemma[2:-3]

            if rodic != []:
                seznam.append((lexeme.lemma, rodic))

    opakovane_funkce.vypis_jeden_seznam(seznam,"I_SlovaTypuMcAlisterBezRodicu.tsv", "slova začínající na 'Mc, která by mohla mít v derinetu rodiče", "chybí hrana") 
                    
