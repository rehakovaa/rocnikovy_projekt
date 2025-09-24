"""
test hledá podstatná jména končící na ření (kouření) bez rodičů 
pokud rodič není nalezen, zkontroluje se, zda to není vnímáno jako unmotivated
"""
import opakovane_funkce

def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

    seznam_dobry = []
    seznam_spatny = []
    bez = []

    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma.endswith("ření") and lexeme.pos == "NOUN" and lexeme.all_parents == []:
            if lexeme.lemma[:-2] in all_lemmas:
                seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(lexeme.lemma[:-2], lexeme, seznam_dobry, seznam_spatny, lexicon)
            elif lexeme.lemma[:-4] in all_lemmas:
                seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(lexeme.lemma[:-4], lexeme, seznam_dobry, seznam_spatny, lexicon)
            elif lexeme.lemma.startswith("sebe") and lexeme.lemma[4:] in all_lemmas:
                seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(lexeme.lemma[4:], lexeme, seznam_dobry, seznam_spatny, lexicon)
            elif lexeme.lemma[:-5] in all_lemmas:
                seznam_dobry, seznam_spatny = opakovane_funkce.muze_se_pridat(lexeme.lemma[:-5], lexeme, seznam_dobry, seznam_spatny, lexicon)
            else:
                bez.append(lexeme)
                    
    bez = opakovane_funkce.je_spravne_bez_rodice(bez)
    opakovane_funkce.vypis_tri_seznamy(seznam_dobry, seznam_spatny, bez, "E_OsamocenaNounKonciciNaReni.tsv", "osamocená nouns končící na 'ření'", "chybí hrana")
