""" 
test hledá lexémy, které jsou identické, ale ani jeden z nich nemá rodiče
identické ve smyslu, že první písmeno je stejně velké 
výtisk se dělí podle toho, jestli lexémy sdílí stejný slovní druh a každá kategorie má vlastní soubor
"""
import opakovane_funkce

def main(lexicon):
    videno = set()
    stejny_typ, ruzny_typ = set(), set()

    for lexeme in lexicon.iter_lexemes():
        if lexeme not in videno: #pokud už jsem to slovo testoval, tak ho přeskočím
            dalsi = lexicon.get_lexemes(lemma=lexeme.lemma)
            if len(dalsi) > 1:
                dalsi.remove(lexeme) #takhle předejdu tomu, abych zpracoval stejné slovo dvakrát 
                videno.add(lexeme)
                for lex in dalsi:
                    if lexeme.all_parents == [] and lex.all_parents == []:
                        if lexeme.pos != lex.pos: #pokud mají různé typy
                            ruzny_typ.add((lexeme.lemma, lex.lemma, lex.pos))
                            #f.write(f"{lexeme.lemma}, {lex.lemma} -  RŮZNÉ typy: {lexeme.pos}, {lex.pos} \n") #nejdříve původní, potom nalezlý
                        else:
                            stejny_typ.add((lexeme.lemma, lex.lemma, lexeme.pos, lex.pos))
                            #f.write(f"{lexeme.lemma}, {lex.lemma} - STEJNÝ typ: {lex.pos} \n")

    opakovane_funkce.vypis_identicka_slova("identická slova se stejným slovním druhem","I_DveStejnaSlovaCaseSensitiveA", stejny_typ, "chybí hrana")
    opakovane_funkce.vypis_identicka_slova("identická slova s různým slovním druhem","I_DveStejnaSlovaCaseSensitiveB", ruzny_typ, "chybí hrana")
