""" 
test hledá slova končící na 'istický', která jsou bez rodiče a snaží se ho dohledat

"""
import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)


vysledek = []
neexistuje = []
all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

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

opakovane_funkce.vypis_dva_seznamy(vysledek, neexistuje, "E_OsamocenaSlovaKonciciNaIsticky.tsv", "osamocená přídavná jména končící na 'istický'")

