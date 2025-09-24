""" 
test hledá slova končící na 'istický', která jsou bez rodiče a snaží se ho dohledat

"""
import opakovane_funkce

def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

    vysledek = []
    neexistuje = []

    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma.endswith("istický") and lexeme.parent is None:
            if not lexeme.lemma.endswith("statistický") and not lexeme.lemma.startswith("proti"):
                nove = lexeme.lemma[:-6]
                nove = nove + "smus"
                if nove in all_lemmas:
                    vysledek.append((lexeme.lemma, nove))
                else:
                    neexistuje.append(lexeme.lemma)

            if lexeme.lemma.endswith("statistický"):
                vysledek.append((lexeme.lemma, "statistika"))
            
            if lexeme.lemma.startswith("proti"):

                nove = lexeme.lemma[:-6][5:]
                nove = nove + "smus"
                if nove in all_lemmas:
                    vysledek.append((lexeme.lemma, nove))
                else:
                    neexistuje.append(lexeme.lemma)

    opakovane_funkce.vypis_dva_seznamy(vysledek, neexistuje, "E_OsamocenaSlovaKonciciNaIsticky.tsv", "osamocená přídavná jména končící na 'istický'", "chybí hrana")

