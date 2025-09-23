""" 
test se zaměřuje na lexémy, kde lemma je naprosto identická, liší se pouze velikostí prvního písmena. tyto lexémy také nesmí mít žádného rodiče a navzájem k sobě nejsou připojena
ve výstupu se dělí podle toho, jestli mají stejný slovní druh anebo se v něm liší
pro přehlednost se každá z těchto dvou kategorií vytiskne do vlastního souboru
"""
import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

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

opakovane_funkce.vypis_identicka_slova("identická slova se stejným slovním druhem","I_DveStejnaSlovaCaseSensitiveA", stejny_typ)
opakovane_funkce.vypis_identicka_slova("identická slova s různým slovním druhem","I_DveStejnaSlovaCaseSensitiveB", ruzny_typ)
